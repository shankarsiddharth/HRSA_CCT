from dataclasses import dataclass, field
from typing import Any


@dataclass
class Medications:
    medications: list[str] = field(default_factory=list)

    def __post_init__(self):
        if len(self.medications) == 0:
            self.medications = ['']

    @staticmethod
    def from_dict(obj: Any) -> 'Medications':
        _medications = [medication for medication in obj.get("medications")]
        return Medications(
            _medications
        )
