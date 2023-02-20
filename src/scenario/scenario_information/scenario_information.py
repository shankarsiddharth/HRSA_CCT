from dataclasses import dataclass, field
from typing import Any

from scenario.scenario_information.scenario_information_version import ScenarioInformationVersion


@dataclass
class ScenarioInformation:
    version: ScenarioInformationVersion = field(default_factory=ScenarioInformationVersion)
    name: str = field(default='')
    localized_name: str = field(default='')
    description: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'ScenarioInformation':
        _version = ScenarioInformationVersion.from_dict(obj.get("version"))
        _name = str(obj.get("name"))
        _localized_name = str(obj.get("localized_name"))
        _description = str(obj.get("description"))
        return ScenarioInformation(
            _version,
            _name,
            _localized_name,
            _description
        )
