from dataclasses import dataclass, field
from typing import Any


@dataclass
class GoogleCloudConfig:
    use_user_service_account_file: bool = field(default=False)
    user_service_account_file_path: str = field(default="")

    @staticmethod
    def from_dict(obj: Any) -> 'GoogleCloudConfig':
        _use_user_service_account_file = bool(obj.get("use_user_service_account_file"))
        _user_service_account_file_path = str(obj.get("user_service_account_file_path"))
        return GoogleCloudConfig(
            _use_user_service_account_file,
            _user_service_account_file_path
        )
