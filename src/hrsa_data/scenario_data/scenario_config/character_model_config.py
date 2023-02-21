from dataclasses import dataclass, field
from typing import Any


@dataclass
class CharacterModelConfig:
    uid: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'CharacterModelConfig':
        _uid = str(obj.get("uid"))
        return CharacterModelConfig(
            _uid
        )
