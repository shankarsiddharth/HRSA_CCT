from dataclasses import dataclass, field
from typing import Any

from scenario.ehr.substance_information import SubstanceInformation


@dataclass
class AllergiesIntolerances:
    substances: list[SubstanceInformation] = field(default_factory=list)

    def __post_init__(self):
        if len(self.substances) == 0:
            self.substances = [SubstanceInformation()]

    @staticmethod
    def from_dict(obj: Any) -> 'AllergiesIntolerances':
        _substances = [SubstanceInformation.from_dict(substance) for substance in obj.get("substances")]
        return AllergiesIntolerances(
            _substances
        )
