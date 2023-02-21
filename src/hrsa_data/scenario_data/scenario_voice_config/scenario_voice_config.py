import json
from dataclasses import dataclass, field, asdict
from typing import Any

from app_file_system.app_file_system_constants import AppFileSystemConstants
from hrsa_data.scenario_data.scenario_voice_config.charater_voice_config import CharacterVoiceConfig
from hrsa_data.scenario_data.scenario_voice_config.scenario_voice_config_version import ScenarioVoiceConfigVersion

# Module Level Constants
__afsc__: AppFileSystemConstants = AppFileSystemConstants()


@dataclass
class ScenarioVoiceConfig:
    version: ScenarioVoiceConfigVersion = field(default_factory=ScenarioVoiceConfigVersion)
    player: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)
    medicalstudent: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)
    patient: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)
    trainer: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'ScenarioVoiceConfig':
        _version = ScenarioVoiceConfigVersion.from_dict(obj.get("version"))
        _player = CharacterVoiceConfig.from_dict(obj.get("player"))
        _medicalstudent = CharacterVoiceConfig.from_dict(obj.get("medicalstudent"))
        _patient = CharacterVoiceConfig.from_dict(obj.get("patient"))
        _trainer = CharacterVoiceConfig.from_dict(obj.get("trainer"))
        return ScenarioVoiceConfig(
            _version,
            _player,
            _medicalstudent,
            _patient,
            _trainer
        )

    @classmethod
    def load_from_json_file(cls, json_file_path) -> 'ScenarioVoiceConfig':
        with open(json_file_path, 'r', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            return ScenarioVoiceConfig.from_dict(json.load(json_file))

    @staticmethod
    def save_to_json_file(obj: 'ScenarioVoiceConfig', json_file_path: str) -> bool:
        # TODO: Add error handling - save scenario config to json file
        with open(json_file_path, 'w', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            json.dump(asdict(obj), json_file, indent=4)
            return True
