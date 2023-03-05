import json
import os
import unittest
from dataclasses import asdict
from types import SimpleNamespace

from hrsa_data.scenario_data.scenario_config.scenario_config import ScenarioConfig
from tests.helper import get_test_path_of_file, afsc


class TestScenarioConfig(unittest.TestCase):
    file_path_to_test = os.path.join(get_test_path_of_file(__file__), 'scenario_config_test.json')
    file_path_to_create = os.path.join(get_test_path_of_file(__file__), 'new_scenario_config.json')

    def test_load_from_string(self):
        with open(self.file_path_to_test, encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            text = f.read()
            # Parse JSON into an object with attributes corresponding to dict keys.
            hrsa_config_data: ScenarioConfig = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
            self.assertEqual(hrsa_config_data.player_config.ui_config.subtitle_config.text_color, '#FFFFFF')
            self.assertEqual(hrsa_config_data.conversation_config.question_timer_in_seconds, 120)

    def test_load_from_dict(self):
        with open(self.file_path_to_test, encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            hrsa_config_data: ScenarioConfig = ScenarioConfig.from_dict(json.load(f))
            self.assertEqual(hrsa_config_data.player_config.ui_config.subtitle_config.text_color, '#FFFFFF')
            self.assertEqual(hrsa_config_data.conversation_config.question_timer_in_seconds, 120)

    def test_create_object(self):
        hrsa_config_data = ScenarioConfig()
        self.assertEqual(hrsa_config_data.player_config.ui_config.subtitle_config.text_color, '#FFFFFF')
        self.assertEqual(hrsa_config_data.conversation_config.question_timer_in_seconds, 0)

    def test_create_new_file(self):
        config_data: ScenarioConfig = ScenarioConfig()
        with open(self.file_path_to_create, 'w', encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            json.dump(asdict(config_data), f, indent=4)


if __name__ == '__main__':
    unittest.main()
