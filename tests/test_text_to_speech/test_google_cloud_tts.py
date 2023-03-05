import json
import os.path
import unittest
from dataclasses import asdict
from types import SimpleNamespace

from tests.helper import get_test_path_of_file, copy_file
from text_to_speech.google_cloud_tts import GoogleCloudTTS
from text_to_speech.google_cloud_voice_data import GoogleCloudVoiceData


class TestGoogleCloudTTS(unittest.TestCase):
    file_to_create = os.path.join(get_test_path_of_file(__file__), 'new_google_cloud_voice_data.json')
    file_to_test = os.path.join(get_test_path_of_file(__file__), 'google_cloud_voice_data_test.json')

    def setUp(self):
        self.gctts: GoogleCloudTTS = GoogleCloudTTS()

    def process_google_cloud_voice_data(self, google_cloud_voice_data: GoogleCloudVoiceData):
        # voice_data_dict = google_cloud_voice_data.voice_data.__dict__
        voice_data_dict = vars(google_cloud_voice_data.voice_data)
        if 'en-US' in voice_data_dict:
            self.assertEqual(voice_data_dict['en-US'].language_code, 'en-US')
        else:
            self.fail('en-US not in google_cloud_voice_data.voice_data')

        if 'es-US' in voice_data_dict:
            self.assertEqual(voice_data_dict['es-US'].language_code, 'es-US')
        else:
            self.fail('es-US not in google_cloud_voice_data.voice_data')

        if 'es-ES' in voice_data_dict:
            self.assertEqual(voice_data_dict['es-ES'].language_code, 'es-ES')
        else:
            self.fail('es-ES not in google_cloud_voice_data.voice_data')

    def test_create_new_file(self):
        self.gctts.cache_voice_data()
        google_cloud_voice_data: GoogleCloudVoiceData = self.gctts.get_voice_data()
        with open(self.file_to_create, 'w') as f:
            json.dump(asdict(google_cloud_voice_data), f, indent=4, sort_keys=True)

        copy_file(self.file_to_create, self.file_to_test)

    def test_load_from_string(self):
        with open(self.file_to_test) as f:
            text = f.read()
            # Parse JSON into an object with attributes corresponding to dict keys.
            google_cloud_voice_data: GoogleCloudVoiceData = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
            self.process_google_cloud_voice_data(google_cloud_voice_data)


if __name__ == '__main__':
    unittest.main()
