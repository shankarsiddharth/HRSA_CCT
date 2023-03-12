from dataclasses import dataclass
from typing import Any

from app_config.config_file_version import ConfigFileVersion


@dataclass
class AppConfigFileVersion(ConfigFileVersion):

    def __post_init__(self):
        super().__init__(self)
        self.major = 1
        self.minor = 0
        self.patch = 0

    @staticmethod
    def from_dict(obj: Any) -> 'AppConfigFileVersion':
        _major = int(obj.get("major"))
        _minor = int(obj.get("minor"))
        _patch = int(obj.get("patch"))
        return AppConfigFileVersion(
            _major,
            _minor,
            _patch
        )
