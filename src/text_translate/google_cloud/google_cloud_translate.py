import sys
import threading

import langcodes
from google.cloud import translate

from app_file_system.app_file_system import AppFileSystem
from service_providers.google_cloud import GoogleCloudServiceProvider
from .google_cloud_translate_data import GoogleCloudTranslateData
from .google_cloud_translate_language_data import GoogleCloudTranslateLanguageData


class GoogleCloudTranslate(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(GoogleCloudTranslate, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if sys.flags.dev_mode:
                        print("GoogleCloudTranslate.__new__()")
        return cls._instance

    def __initialize__(self):
        self.afs: AppFileSystem = AppFileSystem()
        self.gc_sp: GoogleCloudServiceProvider = GoogleCloudServiceProvider()
        self.google_cloud_translate_data: GoogleCloudTranslateData = GoogleCloudTranslateData()
        self.translate_client = translate.TranslationServiceClient(credentials=self.gc_sp.credentials)
        self.is_data_cached = False

    def get_translate_language_data(self) -> GoogleCloudTranslateData:
        if not self.is_data_cached:
            self.cache_translate_language_data()
        return self.google_cloud_translate_data

    def cache_translate_language_data(self):
        self.google_cloud_translate_data: GoogleCloudTranslateData = GoogleCloudTranslateData()

        # TODO: Implement proper error handling for network operations, possibly UI notification
        """Cache all available languages."""

        response = self.translate_client.get_supported_languages(parent=self.gc_sp.parent)

        for language in response.languages:
            if language.language_code not in self.google_cloud_translate_data.language_data:
                self.google_cloud_translate_data.language_data[language.language_code]: GoogleCloudTranslateLanguageData = GoogleCloudTranslateLanguageData()
            self.google_cloud_translate_data.language_data[language.language_code].language_code = language.language_code
            language_name = langcodes.Language.get(language.language_code).display_name()
            self.google_cloud_translate_data.language_data[language.language_code].language_name = language_name

        self.is_data_cached = True
