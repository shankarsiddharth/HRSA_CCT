import json
from dataclasses import dataclass, field, asdict
from typing import Any

from app_file_system.app_file_system_constants import AppFileSystemConstants
from .scenario_information_version import ScenarioInformationVersion

# Module level constants
__afsc__: AppFileSystemConstants = AppFileSystemConstants()


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

    @classmethod
    def load_from_json_file(cls, json_file_path) -> 'ScenarioInformation':
        with open(json_file_path, 'r', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            return ScenarioInformation.from_dict(json.load(json_file))

    @staticmethod
    def save_to_json_file(obj: 'ScenarioInformation', json_file_path: str) -> bool:
        # TODO: Add error handling - save scenario information to json file
        with open(json_file_path, 'w', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            json.dump(asdict(obj), json_file, indent=4)
            return True
