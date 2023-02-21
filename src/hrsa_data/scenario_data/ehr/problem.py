from dataclasses import dataclass, field
from typing import Any


@dataclass
class Problem:
    problem: str = field(default='')
    date_of_diagnosis: str = field(default='')
    date_of_resolution: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'Problem':
        _problem = str(obj.get("problem"))
        _date_of_diagnosis = str(obj.get("date_of_diagnosis"))
        _date_of_resolution = str(obj.get("date_of_resolution"))
        return Problem(
            _problem,
            _date_of_diagnosis,
            _date_of_resolution
        )
