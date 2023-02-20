from dataclasses import dataclass, field
from typing import Any


@dataclass
class FamilyHealthHistory:
    family_health_history: list[str] = field(default_factory=list)

    def __post_init__(self):
        if len(self.family_health_history) == 0:
            self.family_health_history = ['']

    @staticmethod
    def from_dict(obj: Any) -> 'FamilyHealthHistory':
        _family_health_history = [family_health_history_element for family_health_history_element in obj.get("family_health_history")]
        return FamilyHealthHistory(
            _family_health_history
        )
