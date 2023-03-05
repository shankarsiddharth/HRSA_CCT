import sys
import threading

from google.cloud import texttospeech
from google.oauth2 import service_account
from langcodes import Language

from app_file_system.app_file_system import AppFileSystem
from text_to_speech.google_cloud_voice_data import GoogleCloudVoiceData
from text_to_speech.google_cloud_voice_language_data import GoogleCloudVoiceLanguageData


class GoogleCloudTTS(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GoogleCloudTTS, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if sys.flags.dev_mode:
                        print("GoogleCloudTTS.__new__()")
        return cls._instance

    def __initialize__(self):
        self.afs: AppFileSystem = AppFileSystem()
        self.credentials_file_path = self.afs.get_google_cloud_credentials_file_path()
        self.google_cloud_voice_data: GoogleCloudVoiceData = GoogleCloudVoiceData()
        if self.credentials_file_path is None:
            # TODO: Implement proper error handling, possibly UI notification
            raise FileNotFoundError("Google Cloud credentials file not found")
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file_path)
        self.tts_client = texttospeech.TextToSpeechClient(credentials=self.credentials)
        pass

    def get_voice_data(self) -> GoogleCloudVoiceData:
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

        print(f"Google Cloud Voice Data: {self.google_cloud_voice_data}")
