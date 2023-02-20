from dataclasses import dataclass, field
from typing import Any

from scenario.scenario_config.character_config import CharacterConfig
from scenario.scenario_config.conversation_config import ConversationConfig
from scenario.scenario_config.scenario_config_version import ScenarioConfigVersion


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
