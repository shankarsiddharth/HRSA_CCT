from dataclasses import dataclass, field
from typing import Any

from .app_config_file_version import AppConfigFileVersion
from .cct_config import CCTConfig


@dataclass
class AppConfig:
    version: AppConfigFileVersion = field(default_factory=AppConfigFileVersion)
    cct_config: CCTConfig = field(default_factory=CCTConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'AppConfig':
        _version = AppConfigFileVersion.from_dict(obj.get("version"))
        _cct_config = CCTConfig.from_dict(obj.get("cct_config"))
        return AppConfig(
            _version,
            _cct_config
        )
