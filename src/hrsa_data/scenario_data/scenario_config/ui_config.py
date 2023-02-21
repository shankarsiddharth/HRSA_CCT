from dataclasses import dataclass, field
from typing import Any

from hrsa_data.scenario_data.scenario_config.subtitle_config import SubtitleConfig


@dataclass
class UIConfig:
    subtitle_config: SubtitleConfig = field(default_factory=SubtitleConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'UIConfig':
        _subtitle_config = SubtitleConfig.from_dict(obj.get("subtitle_config"))
        return UIConfig(
            _subtitle_config
        )
