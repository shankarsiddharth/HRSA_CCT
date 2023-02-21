from dataclasses import dataclass, field
from typing import Any


@dataclass
class DataFileVersion:
    major: int = field(default=0)
    minor: int = field(default=0)
    patch: int = field(default=0)

    @staticmethod
    def from_dict(obj: Any) -> 'DataFileVersion':
        _major = int(obj.get("major"))
        _minor = int(obj.get("minor"))
        _patch = int(obj.get("patch"))
        return DataFileVersion(
            _major,
            _minor,
            _patch
        )
