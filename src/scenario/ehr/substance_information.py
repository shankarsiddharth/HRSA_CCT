from dataclasses import dataclass, field
from typing import Any


@dataclass
class SubstanceInformation:
    substance_medication: str = field(default='')
    substance_drug_class: str = field(default='')
    reaction: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'SubstanceInformation':
        _substance_medication = str(obj.get("substance_medication"))
        _substance_drug_class = str(obj.get("substance_drug_class"))
        _reaction = str(obj.get("reaction"))
        return SubstanceInformation(
            _substance_medication,
            _substance_drug_class,
            _reaction
        )
