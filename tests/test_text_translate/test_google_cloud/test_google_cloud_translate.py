import json
import os.path
import unittest
from dataclasses import asdict
from types import SimpleNamespace

from tests.helper import get_test_path_of_file, copy_file, afsc
from text_translate.google_cloud.google_cloud_translate import GoogleCloudTranslate
from text_translate.google_cloud.google_cloud_translate_data import GoogleCloudTranslateData


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


if __name__ == '__main__':
    unittest.main()
