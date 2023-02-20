from dataclasses import dataclass, field
from typing import Any

from scenario.voice_config.charater_voice_config import CharacterVoiceConfig
from scenario.voice_config.voice_config_version import VoiceConfigVersion


@dataclass
class VoiceConfig:
    version: VoiceConfigVersion = field(default_factory=VoiceConfigVersion)
    player: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)
    medicalstudent: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)
    patient: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)
    trainer: CharacterVoiceConfig = field(default_factory=CharacterVoiceConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'VoiceConfig':
        _version = VoiceConfigVersion.from_dict(obj.get("version"))
        _player = CharacterVoiceConfig.from_dict(obj.get("player"))
        _medicalstudent = CharacterVoiceConfig.from_dict(obj.get("medicalstudent"))
        _patient = CharacterVoiceConfig.from_dict(obj.get("patient"))
        _trainer = CharacterVoiceConfig.from_dict(obj.get("trainer"))
        return VoiceConfig(
            _version,
            _player,
            _medicalstudent,
            _patient,
            _trainer
        )
