from dataclasses import dataclass, field
from typing import Any

from hrsa_data.scenario_data.scenario_voice_config.charater_voice_config import CharacterVoiceConfig
from hrsa_data.scenario_data.scenario_voice_config.scenario_voice_config_version import ScenarioVoiceConfigVersion


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
