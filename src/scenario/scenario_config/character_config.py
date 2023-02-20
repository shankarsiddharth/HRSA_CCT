from dataclasses import dataclass, field
from typing import Any

from scenario.scenario_config.character_model_config import CharacterModelConfig
from scenario.scenario_config.ui_config import UIConfig


@dataclass
class CharacterConfig:
    ui_config: UIConfig = field(default_factory=UIConfig)
    character_model_config: CharacterModelConfig = field(default_factory=CharacterModelConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'CharacterConfig':
        _ui_config = UIConfig.from_dict(obj.get("ui_config"))
        _character_model_config = CharacterModelConfig.from_dict(obj.get("character_model_config"))
        return CharacterConfig(
            _ui_config,
            _character_model_config
        )
