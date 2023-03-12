from dataclasses import dataclass, field
from typing import Any

from app_config.google_cloud_config import GoogleCloudConfig


@dataclass
class ServiceProviderConfig:
    google_cloud: GoogleCloudConfig = field(default_factory=GoogleCloudConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'ServiceProviderConfig':
        _google_cloud = GoogleCloudConfig.from_dict(obj.get("google_cloud"))
        return ServiceProviderConfig(
            _google_cloud
        )
