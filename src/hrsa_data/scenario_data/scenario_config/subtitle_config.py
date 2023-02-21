from dataclasses import dataclass, field
from typing import Any


@dataclass
class SubtitleConfig:
    text_color: str = field(default='#FFFFFF')

    @staticmethod
    def from_dict(obj: Any) -> 'SubtitleConfig':
        _text_color = str(obj.get("text_color"))
        return SubtitleConfig(
            _text_color
        )
