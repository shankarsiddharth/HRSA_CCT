from dataclasses import dataclass, field
from typing import Any

from scenario.hrsa_config.character_config import CharacterConfig
from scenario.hrsa_config.conversation_config import ConversationConfig
from scenario.hrsa_config.hrsa_config_version import HRSAConfigVersion


@dataclass
class HRSAConfig:
    version: HRSAConfigVersion = field(default_factory=HRSAConfigVersion)
    player_config: CharacterConfig = field(default_factory=CharacterConfig)
    medicalstudent_config: CharacterConfig = field(default_factory=CharacterConfig)
    patient_config: CharacterConfig = field(default_factory=CharacterConfig)
    trainer_config: CharacterConfig = field(default_factory=CharacterConfig)
    conversation_config: ConversationConfig = field(default_factory=ConversationConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'HRSAConfig':
        _version = HRSAConfigVersion.from_dict(obj.get("version"))
        _player_config = CharacterConfig.from_dict(obj.get("player_config"))
        _medicalstudent_config = CharacterConfig.from_dict(obj.get("medicalstudent_config"))
        _patient_config = CharacterConfig.from_dict(obj.get("patient_config"))
        _trainer_config = CharacterConfig.from_dict(obj.get("trainer_config"))
        _conversation_config = ConversationConfig.from_dict(obj.get("conversation_config"))
        return HRSAConfig(
            _version,
            _player_config,
            _medicalstudent_config,
            _patient_config,
            _trainer_config,
            _conversation_config
        )
