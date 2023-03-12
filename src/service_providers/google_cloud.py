import json
import threading

from google.oauth2 import service_account

from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_debug.app_debug import IS_DEBUG_MODE_ENABLED


class GoogleCloudServiceProvider(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GoogleCloudServiceProvider, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if IS_DEBUG_MODE_ENABLED:
                        print("GoogleCloudServiceProvider.__new__()")
        return cls._instance

    def __initialize__(self):
        self.afs: AppFileSystem = AppFileSystem()
        self.afsc: AppFileSystemConstants = AppFileSystemConstants()
        self.credentials_file_path = self.afs.get_google_cloud_credentials_file_path()
        self.project_id = 'YOUR_PROJECT_ID'
        self.translate_language_parent = 'YOUR_PARENT_PROJECT_ID'
        self.location = "global"
        self.translate_text_parent = "YOUR_PARENT_PROJECT_ID_FOR_TRANSLATE_TEXT"
        self.private_key_id = 'YOUR_PRIVATE_KEY_ID'
        if self.credentials_file_path is None:
            # TODO: Implement proper error handling, possibly UI notification
            raise FileNotFoundError("Google Cloud credentials file not found")
        self.credentials = service_account.Credentials.from_service_account_file(self.credentials_file_path)
        self.__read_data_from_service_account_private_key_json_file__()

    def __read_data_from_service_account_private_key_json_file__(self):
        with open(self.credentials_file_path, 'r', encoding=self.afsc.DEFAULT_FILE_ENCODING) as json_file:
            data = json.load(json_file)
            self.private_key_id = data['private_key_id']
            self.project_id = data['project_id']
            self.translate_language_parent = f"projects/{self.project_id}"
            self.translate_text_parent = f"projects/{self.project_id}/locations/{self.location}"
