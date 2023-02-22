import sys
import threading

from google.cloud import texttospeech
from google.oauth2 import service_account

from app_file_system.app_file_system import AppFileSystem


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
        if self.credentials_file_path is None:
            # TODO: Implement proper error handling, possibly UI notification
            raise FileNotFoundError("Google Cloud credentials file not found")
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file_path)
        tts_client = texttospeech.TextToSpeechClient(credentials=self.credentials)

        pass
