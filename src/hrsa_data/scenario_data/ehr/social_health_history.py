from dataclasses import dataclass, field
from typing import Any


@dataclass
class SocialHealthHistory:
    social_history_observation: str = field(default='')
    alcohol_use: str = field(default='')
    drug_use: str = field(default='')
    sexual_activity: str = field(default='')
    refugee_status: str = field(default='')
    congregate_living: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'SocialHealthHistory':
        _social_history_observation = str(obj.get("social_history_observation"))
        _alcohol_use = str(obj.get("alcohol_use"))
        _drug_use = str(obj.get("drug_use"))
        _sexual_activity = str(obj.get("sexual_activity"))
        _refugee_status = str(obj.get("refugee_status"))
        _congregate_living = str(obj.get("congregate_living"))
        return SocialHealthHistory(
            _social_history_observation,
            _alcohol_use,
            _drug_use,
            _sexual_activity,
            _refugee_status,
            _congregate_living
        )
