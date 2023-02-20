from dataclasses import dataclass
from typing import Any

from scenario.file_version.data_file_version import DataFileVersion


@dataclass
class ScenarioConfigVersion(DataFileVersion):

    def __post_init__(self):
        super().__init__(self)
        self.major = 1
        self.minor = 0
        self.patch = 0

    @staticmethod
    def from_dict(obj: Any) -> 'ScenarioConfigVersion':
        _major = int(obj.get("major"))
        _minor = int(obj.get("minor"))
        _patch = int(obj.get("patch"))
        return ScenarioConfigVersion(
            _major,
            _minor,
            _patch
        )
