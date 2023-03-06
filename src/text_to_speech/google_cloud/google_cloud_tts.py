import sys
import threading

from google.cloud import texttospeech
from langcodes import Language

from app_file_system.app_file_system import AppFileSystem
from service_providers.google_cloud import GoogleCloudServiceProvider
from .google_cloud_voice_data import GoogleCloudVoiceData
from .google_cloud_voice_language_data import GoogleCloudVoiceLanguageData


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
