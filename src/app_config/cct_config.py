from dataclasses import dataclass, field
from typing import Any

from app_config.service_provider_config import ServiceProviderConfig


@dataclass
class CCTConfig:
    service_provider: ServiceProviderConfig = field(default_factory=ServiceProviderConfig)

    @staticmethod
    def from_dict(obj: Any) -> 'CCTConfig':
        _service_provider = ServiceProviderConfig.from_dict(obj.get("service_provider"))
        return CCTConfig(
            _service_provider
        )
