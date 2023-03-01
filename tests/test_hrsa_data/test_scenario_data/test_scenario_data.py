import json
import os
import unittest
from dataclasses import asdict

from hrsa_data.scenario_data.ehr.patient_information import PatientInformation
from hrsa_data.scenario_data.scenario_config.scenario_config import ScenarioConfig
from hrsa_data.scenario_data.scenario_information.scenario_information import ScenarioInformation
from hrsa_data.scenario_data.scenario_voice_config.scenario_voice_config import ScenarioVoiceConfig
from tests.helper import get_test_path_of_file


class TestScenarioData(unittest.TestCase):
    file_path_to_test = os.path.join(get_test_path_of_file(__file__), 'scenario_voice_config_test.json')

    def test_scenario_information(self):
        print(json.dumps(asdict(ScenarioInformation())), '\n')
        print(ScenarioInformation())
        with open(self.file_path_to_test, 'w') as f:
            json.dump(asdict(ScenarioInformation()), f, indent=4)

        with open(self.file_path_to_test, 'r') as f:
            config_data: ScenarioInformation = ScenarioInformation.from_dict(json.load(f))
            print(json.dumps(asdict(config_data)), '\n')
            self.assertEqual(config_data.version.major, 1)

    def test_patient_information(self):
        print(json.dumps(asdict(PatientInformation())), '\n')
        print(PatientInformation())
        with open(self.file_path_to_test, 'w') as f:
            json.dump(asdict(PatientInformation()), f, indent=4)

        with open(self.file_path_to_test, 'r') as f:
            config_data: PatientInformation = PatientInformation.from_dict(json.load(f))
            print(json.dumps(asdict(config_data)), '\n')
            self.assertEqual(config_data.version.major, 1)

    def test_scenario_config(self):
        print(json.dumps(asdict(ScenarioConfig())), '\n')
        print(ScenarioConfig())
        with open(self.file_path_to_test, 'w') as f:
            json.dump(asdict(ScenarioConfig()), f, indent=4)

        with open(self.file_path_to_test, 'r') as f:
            config_data: ScenarioConfig = ScenarioConfig.from_dict(json.load(f))
            print(json.dumps(asdict(config_data)), '\n')
            self.assertEqual(config_data.version.major, 1)

    def test_voice_config(self):
        print(json.dumps(asdict(ScenarioVoiceConfig())), '\n')
        print(ScenarioVoiceConfig())
        with open(self.file_path_to_test, 'w') as f:
            json.dump(asdict(ScenarioVoiceConfig()), f, indent=4)

        with open(self.file_path_to_test, 'r') as f:
            config_data: ScenarioVoiceConfig = ScenarioVoiceConfig.from_dict(json.load(f))
            print(json.dumps(asdict(config_data)), '\n')
            self.assertEqual(config_data.version.major, 1)


if __name__ == '__main__':
    unittest.main()
