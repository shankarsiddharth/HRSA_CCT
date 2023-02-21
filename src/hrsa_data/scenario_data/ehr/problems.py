from dataclasses import dataclass, field
from typing import Any

from .problem import Problem


@dataclass
class Problems:
    problems: list[Problem] = field(default_factory=list)
    sdoh_problems_health_concerns: list[Problem] = field(default_factory=list)

    def __post_init__(self):
        if len(self.problems) == 0:
            self.problems = [Problem()]
        if len(self.sdoh_problems_health_concerns) == 0:
            self.sdoh_problems_health_concerns = [Problem()]

    @staticmethod
    def from_dict(obj: Any) -> 'Problems':
        _problems = [Problem.from_dict(problem) for problem in obj.get("problems")]
        _sdoh_problems_health_concerns = [Problem.from_dict(problem) for problem in obj.get("sdoh_problems_health_concerns")]
        return Problems(
            _problems,
            _sdoh_problems_health_concerns
        )
