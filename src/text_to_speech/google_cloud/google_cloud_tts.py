import sys

from google.cloud import texttospeech
from langcodes import Language

from app_file_system.app_file_system import AppFileSystem
from classes.singleton import Singleton
from hrsa_data.scenario_data.scenario_voice_config.charater_voice_config import CharacterVoiceConfig
from hrsa_data.scenario_data.scenario_voice_config.scenario_voice_config import ScenarioVoiceConfig
from service_providers.google_cloud import GoogleCloudServiceProvider
from .google_cloud_voice_data import GoogleCloudVoiceData
from .google_cloud_voice_language_data import GoogleCloudVoiceLanguageData
from ..tts_dialogue_data.audio_dialogue_data import AudioDialogueData
from ..tts_dialogue_data.room_dialogue_data import RoomDialogueData
from ..tts_dialogue_data.tts_dialogue_data import TTSDialogueData


class GoogleCloudTTS(metaclass=Singleton):
    
    def __init__(self):
        self.afs: AppFileSystem = AppFileSystem()
        self.gc_sp: GoogleCloudServiceProvider = GoogleCloudServiceProvider()
        self.google_cloud_voice_data: GoogleCloudVoiceData = GoogleCloudVoiceData()
        self.tts_client = texttospeech.TextToSpeechClient(credentials=self.gc_sp.credentials)
        self.is_data_cached = False

    def get_voice_data(self) -> GoogleCloudVoiceData:
        if not self.is_data_cached:
            self.cache_voice_data()
        return self.google_cloud_voice_data

    def cache_voice_data(self):
        self.google_cloud_voice_data: GoogleCloudVoiceData = GoogleCloudVoiceData()

        # TODO: Implement proper error handling for network operations, possibly UI notification
        # Performs the list voices request
        voices = self.tts_client.list_voices()

        for voice in voices.voices:
            voice_name = voice.name
            ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)
            ssml_gender_name: str = ssml_gender.name
            ssml_gender_name = ssml_gender_name.upper()
            natural_sample_rate_hertz = voice.natural_sample_rate_hertz

            # Display the supported language codes for this voice. Example: "en-US"
            for language_code in voice.language_codes:
                language_name = Language.get(language_code).display_name()
                if language_name == 'Unknown language':
                    print(f"Error: Language Code: {language_code}", file=sys.stderr)
                    continue

                if language_code not in self.google_cloud_voice_data.voice_data:
                    self.google_cloud_voice_data.voice_data[language_code]: GoogleCloudVoiceLanguageData = GoogleCloudVoiceLanguageData()

                self.google_cloud_voice_data.voice_data[language_code].language_code = language_code
                self.google_cloud_voice_data.voice_data[language_code].language_name = language_name
                if ssml_gender_name == "MALE":
                    self.google_cloud_voice_data.voice_data[language_code].gender_data.MALE.append(voice_name)
                elif ssml_gender_name == "FEMALE":
                    self.google_cloud_voice_data.voice_data[language_code].gender_data.FEMALE.append(voice_name)
                elif ssml_gender_name == "NEUTRAL":
                    self.google_cloud_voice_data.voice_data[language_code].gender_data.NEUTRAL.append(voice_name)
                else:
                    continue

        for key in self.google_cloud_voice_data.voice_data:
            self.google_cloud_voice_data.voice_data[key].gender_data.MALE.sort()
            self.google_cloud_voice_data.voice_data[key].gender_data.FEMALE.sort()
            self.google_cloud_voice_data.voice_data[key].gender_data.NEUTRAL.sort()

        self.is_data_cached = True

    def generate_audio(self, tts_dialogue_data: TTSDialogueData, scenario_voice_config: ScenarioVoiceConfig):
        # TODO: Add Logs and Error Handling and Progress Update to UI
        self.generate_audio_for_room(tts_dialogue_data.break_room_dialogue_data, scenario_voice_config)
        self.generate_audio_for_room(tts_dialogue_data.patient_room_dialogue_data, scenario_voice_config)
        self.generate_audio_for_room(tts_dialogue_data.break_room_feedback_dialogue_data, scenario_voice_config)
        self.generate_audio_for_room(tts_dialogue_data.patient_room_feedback_dialogue_data, scenario_voice_config)
        pass

    def generate_audio_for_room(self, room_dialogue_data: RoomDialogueData, scenario_voice_config: ScenarioVoiceConfig):
        # TODO: Add Logs and Error Handling and Progress Update to UI
        audio_dialogue_data_dict: dict = room_dialogue_data.audio_dialogue_data_dict
        audio_dialogue_data: AudioDialogueData
        for audio_dialogue_data in audio_dialogue_data_dict.values():
            self.generate_audio_for_dialogue(audio_dialogue_data, scenario_voice_config)
        pass

    def generate_audio_for_dialogue(self, audio_dialogue_data: AudioDialogueData, scenario_voice_config: ScenarioVoiceConfig):
        # TODO: Add Logs and Error Handling and Progress Update to UI

        input_text = audio_dialogue_data.text

        # TODO: Potentially add type enum to check for character types instead of string checks
        # Get the voice config data for the character type
        character_type = audio_dialogue_data.character_type.lower()
        character_voice_config: CharacterVoiceConfig = scenario_voice_config.player
        if character_type == "medicalstudent":
            character_voice_config = scenario_voice_config.medicalstudent
        elif character_type == "patient":
            character_voice_config = scenario_voice_config.patient
        elif character_type == "trainer":
            character_voice_config = scenario_voice_config.trainer

        # Get the gender data
        gender_text: str = character_voice_config.gender.upper()
        ssml_gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.FEMALE
        if gender_text == "MALE":
            ssml_gender = texttospeech.SsmlVoiceGender.MALE
        elif gender_text == "NEUTRAL":
            ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL

        # Set the voice parameters
        # noinspection PyTypeChecker
        voice: texttospeech.VoiceSelectionParams = texttospeech.VoiceSelectionParams(
            language_code=character_voice_config.language_code,
            name=character_voice_config.voice_name,
            ssml_gender=ssml_gender
        )

        # Set the audio file type
        # noinspection PyTypeChecker
        audio_config: texttospeech.AudioConfig = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )

        audio_content_in_bytes = self.synthesize_speech(input_text, voice, audio_config)

        self.write_audio_to_file(audio_content_in_bytes, audio_dialogue_data.audio_file_path)

    def write_audio_to_file(self, audio_content_in_bytes: bytes, file_path: str):
        # TODO: Add Logs and Error Handling and Progress Update to UI
        # The response's audio_content is binary.
        with open(file_path, "wb") as output_audio_file:
            # Write the response to the output file.
            output_audio_file.write(audio_content_in_bytes)
            print(f'Audio content written to file "{file_path}"')

    def synthesize_speech(self, input_text: str, voice: texttospeech.VoiceSelectionParams, audio_config: texttospeech.AudioConfig) -> bytes:
        # TODO: Add Logs and Error Handling and Progress Update to UI
        # Set the text input to be synthesized
        # noinspection PyTypeChecker
        synthesis_input = texttospeech.SynthesisInput(text=input_text)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = self.tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        return response.audio_content

# if __name__ == "__main__":
#     scenario_config = ScenarioVoiceConfig.load_from_json_file(r"C:\GAppLab\hrsa_cct\HRSAData_Old\Scenario1\en-US\scenario_voice_config.json")
#     tts: GoogleCloudTTS = GoogleCloudTTS()
#     audio_dialogue_data: AudioDialogueData = AudioDialogueData()
#     audio_dialogue_data.text = "Hello. This is a good opportunity for us to discuss the patient\u2019s history and physical exam findings."
#     audio_dialogue_data.character_type = "PLAYER"
#     audio_dialogue_data.audio_file_path = r"C:\GAppLab\hrsa_cct\src\__misc\misc_data\\test.mp3"
#     tts.generate_audio_for_dialogue(audio_dialogue_data, scenario_config)
