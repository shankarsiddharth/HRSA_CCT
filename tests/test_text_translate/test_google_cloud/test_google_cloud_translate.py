import json
import os.path
import unittest
from dataclasses import asdict
from types import SimpleNamespace

from tests.helper import get_test_path_of_file, copy_file, afsc
from tests.settings import SKIP_CLOUD_CONNECT_TESTS, SKIP_CLOUD_CONNECT_TESTS_WITH_NEGLIGIBLE_COST, SKIP_CLOUD_CONNECT_TESTS_WITH_HIGH_COST
from text_translate.google_cloud.google_cloud_translate import GoogleCloudTranslate
from text_translate.google_cloud.google_cloud_translate_data import GoogleCloudTranslateData
from text_translate.google_cloud.google_cloud_translate_response_data import GoogleCloudTranslateResponseData


class TestGoogleCloudTranslate(unittest.TestCase):
    file_to_create = os.path.join(get_test_path_of_file(__file__), 'new_google_cloud_translate_data.json')
    file_to_test = os.path.join(get_test_path_of_file(__file__), 'google_cloud_voice_translate_test.json')

    def setUp(self):
        self.gc_translate: GoogleCloudTranslate = GoogleCloudTranslate()

    def process_google_cloud_voice_data(self, google_cloud_translate_data: GoogleCloudTranslateData):
        # voice_data_dict = google_cloud_voice_data.voice_data.__dict__
        language_data_dict = vars(google_cloud_translate_data.language_data)
        if 'en' in language_data_dict:
            self.assertEqual(language_data_dict['en'].language_code, 'en')
        else:
            self.fail('en not in google_cloud_translate_data.language_data')

        if 'es' in language_data_dict:
            self.assertEqual(language_data_dict['es'].language_code, 'es')
        else:
            self.fail('es not in google_cloud_translate_data.language_data')

        self.assertNotIn('ex', language_data_dict)

        self.assertEqual(language_data_dict['mi'].language_name, 'Māori')

        self.assertNotEqual(language_data_dict['mi'].language_name, 'Maori')

        self.assertNotEqual(language_data_dict['mi'].language_name, r"M\u0101ori")

        # if 'ex' in language_data_dict:
        #     self.assertEqual(language_data_dict['ex'].language_code, 'ex')
        # else:
        #     self.fail('ex not in google_cloud_translate_data.language_data')

    def test_create_new_file(self):
        self.gc_translate.cache_translate_language_data()
        google_cloud_translate_data: GoogleCloudTranslateData = self.gc_translate.get_translate_language_data()
        with open(self.file_to_create, 'w', encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            json.dump(asdict(google_cloud_translate_data), f, indent=4, sort_keys=True, ensure_ascii=False)

        copy_file(self.file_to_create, self.file_to_test)

    def test_load_from_string(self):
        with open(self.file_to_test, encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            text = f.read()
            # Parse JSON into an object with attributes corresponding to dict keys.
            google_cloud_translate_data: GoogleCloudTranslateData = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
            self.process_google_cloud_voice_data(google_cloud_translate_data)

    @unittest.skipIf(SKIP_CLOUD_CONNECT_TESTS or SKIP_CLOUD_CONNECT_TESTS_WITH_HIGH_COST,
                     "Skipping test that requires cloud connection")
    def test_translate_list_length(self):
        string_to_repeat = "This is a test."
        input_text = list()
        for i in range(1, 1026):
            input_text.append(string_to_repeat)
        print(len(input_text))
        gc_rd: GoogleCloudTranslateResponseData = self.gc_translate.translate_text(text=input_text, target_language_code='es', source_language_code='en-US')
        self.assertEqual(gc_rd.response_data[0].translated_text, 'Esta es una prueba para traducir contenido de texto grande.')

    @unittest.skipIf(SKIP_CLOUD_CONNECT_TESTS or SKIP_CLOUD_CONNECT_TESTS_WITH_HIGH_COST,
                     "Skipping test that requires cloud connection")
    def test_translate_codepoint_length(self):
        string_to_repeat = "This is a test for translating large text content."
        input_text = list()
        input_text_length = 0
        for i in range(1, 1025):
            input_text.append(string_to_repeat)
            input_text_length += len(string_to_repeat.encode('utf-8'))
        print(input_text_length)
        gc_rd: GoogleCloudTranslateResponseData = self.gc_translate.translate_text(text=input_text, target_language_code='es', source_language_code='en-US')
        self.assertEqual(gc_rd.response_data[0].translated_text, 'Esta es una prueba para traducir contenido de texto grande.')

    @unittest.skipIf(SKIP_CLOUD_CONNECT_TESTS or SKIP_CLOUD_CONNECT_TESTS_WITH_NEGLIGIBLE_COST,
                     "Skipping test that requires cloud connection")
    def test_translate_simple(self):
        input_text = ["This is a test."]
        gc_rd: GoogleCloudTranslateResponseData = self.gc_translate.translate_text(text=input_text, target_language_code='es', source_language_code='en-US')
        self.assertEqual(gc_rd.response_data[0].translated_text, 'Esto es una prueba.')


if __name__ == '__main__':
    unittest.main()
