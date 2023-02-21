import json
from dataclasses import dataclass, field, asdict
from typing import Any

from app_file_system.app_file_system_constants import AppFileSystemConstants
from .character_config import CharacterConfig
from .conversation_config import ConversationConfig
from .scenario_config_version import ScenarioConfigVersion

# Module Level Constants
__afsc__: AppFileSystemConstants = AppFileSystemConstants()


@dataclass
class ScenarioConfig:
    version: ScenarioConfigVersion = field(default_factory=ScenarioConfigVersion)
    player_config: CharacterConfig = field(default_factory=CharacterConfig)
    medicalstudent_config: CharacterConfig = field(default_factory=CharacterConfig)
    patient_config: CharacterConfig = field(default_factory=CharacterConfig)
    trainer_config: CharacterConfig = field(default_factory=CharacterConfig)
    conversation_config: ConversationConfig = field(default_factory=ConversationConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'ScenarioConfig':
        _version = ScenarioConfigVersion.from_dict(obj.get("version"))
        _player_config = CharacterConfig.from_dict(obj.get("player_config"))
        _medicalstudent_config = CharacterConfig.from_dict(obj.get("medicalstudent_config"))
        _patient_config = CharacterConfig.from_dict(obj.get("patient_config"))
        _trainer_config = CharacterConfig.from_dict(obj.get("trainer_config"))
        _conversation_config = ConversationConfig.from_dict(obj.get("conversation_config"))
        return ScenarioConfig(
            _version,
            _player_config,
            _medicalstudent_config,
            _patient_config,
            _trainer_config,
            _conversation_config
        )

    @classmethod
    def load_from_json_file(cls, json_file_path) -> 'ScenarioConfig':
        with open(json_file_path, 'r', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            return ScenarioConfig.from_dict(json.load(json_file))

    @staticmethod
    def save_to_json_file(obj: 'ScenarioConfig', json_file_path: str) -> bool:
        # TODO: Add error handling - save scenario config to json file
        with open(json_file_path, 'w', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            json.dump(asdict(obj), json_file, indent=4)
            return True
