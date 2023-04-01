import langcodes
from google.cloud import translate

from app_file_system.app_file_system import AppFileSystem
from classes.singleton import Singleton
from service_providers.google_cloud import GoogleCloudServiceProvider
from .google_cloud_translate_data import GoogleCloudTranslateData
from .google_cloud_translate_language_data import GoogleCloudTranslateLanguageData
from .google_cloud_translate_response_data import GoogleCloudTranslateResponseData
from .google_cloud_translate_response_element_data import GoogleCloudTranslateResponseElementData


class GoogleCloudTranslate(metaclass=Singleton):

    def __init__(self):
        # Reference: https://cloud.google.com/translate/docs/reference/rest/v3/projects.locations/translateText
        self.MAX_TEXT_LIST_LENGTH = 1024
        self.MAX_CODEPOINTS_PER_REQUEST = 30000  # 30k codepoints per request

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

        """Cache all available languages."""
        # TODO: Implement proper error handling for network operations, possibly UI notification
        response = self.translate_client.get_supported_languages(parent=self.gc_sp.translate_language_parent)

        for language in response.languages:
            if language.language_code not in self.google_cloud_translate_data.language_data:
                self.google_cloud_translate_data.language_data[language.language_code]: GoogleCloudTranslateLanguageData = GoogleCloudTranslateLanguageData()
            self.google_cloud_translate_data.language_data[language.language_code].language_code = language.language_code
            language_name = langcodes.Language.get(language.language_code).display_name()
            self.google_cloud_translate_data.language_data[language.language_code].language_name = language_name

        self.is_data_cached = True

    def _translate_text_list_element(self, text="", target_language_code="es", source_language_code="en-US"):
        # TODO: Implement proper error handling for network operations, possibly UI notification
        response = self.translate_client.translate_text(
            request={
                "parent": self.gc_sp.translate_text_parent,
                "contents": [text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )
        # There is only one element in the 'contents' list
        # so, we only need the first element of the 'translations' response, if the network request was successful
        translated_text = response.translations[0].translated_text
        return translated_text

    def _translate_text_list_elements(self, text_content_list: list, target_language_code="es", source_language_code="en-US") -> GoogleCloudTranslateResponseData:
        gc_rd: GoogleCloudTranslateResponseData = GoogleCloudTranslateResponseData()

        for index in range(0, len(text_content_list)):
            response_element_data: GoogleCloudTranslateResponseElementData = GoogleCloudTranslateResponseElementData()
            response_element_data.original_text = text_content_list[index]
            # TODO: Implement proper error handling for network operations, possibly UI notification
            if len(text_content_list[index]) <= 0:
                response_element_data.original_text = ""
                response_element_data.translated_text = ""
            else:
                response_element_data.translated_text = self._translate_text_list_element(response_element_data.original_text, target_language_code, source_language_code)

            gc_rd.response_data[index] = response_element_data

        return gc_rd

    def _translate_text_list(self, text_content_list: list, target_language_code="es", source_language_code="en-US") -> GoogleCloudTranslateResponseData:
        # TODO: Implement proper error handling for network operations, possibly UI notification
        response = self.translate_client.translate_text(
            request={
                "parent": self.gc_sp.translate_text_parent,
                "contents": text_content_list,
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": source_language_code,
                "target_language_code": target_language_code,
            }
        )

        gc_rd: GoogleCloudTranslateResponseData = GoogleCloudTranslateResponseData()

        index = 0
        for translation in response.translations:
            response_element_data: GoogleCloudTranslateResponseElementData = GoogleCloudTranslateResponseElementData()
            response_element_data.original_text = text_content_list[index]
            response_element_data.translated_text = translation.translated_text
            gc_rd.response_data[index] = response_element_data
            index += 1

        return gc_rd

    def translate_text(self, text_content_list: list, target_language_code="es", source_language_code="en-US") -> GoogleCloudTranslateResponseData:
        # Reference: https://cloud.google.com/translate/docs/reference/rest/v3/projects.locations/translateText

        # Remove empty strings from the list
        text_content_list_without_empty_string = list(filter(None, text_content_list))

        # Check if the list is empty
        if len(text_content_list_without_empty_string) <= 0:
            return GoogleCloudTranslateResponseData()

        # Check if the length of the text list is greater than 1024
        if len(text_content_list_without_empty_string) > 1024:
            return self._translate_text_list_elements(text_content_list_without_empty_string, target_language_code, source_language_code)

        # Check if the length of the codepoints is greater than 30k
        codepoints_length = 0
        for index in range(0, len(text_content_list_without_empty_string)):
            codepoints_length += len(text_content_list_without_empty_string[index].encode('utf-8'))  # Get the length of the text in bytes

        if codepoints_length > 30000:
            return self._translate_text_list_elements(text_content_list_without_empty_string, target_language_code, source_language_code)

        return self._translate_text_list(text_content_list_without_empty_string, target_language_code, source_language_code)
