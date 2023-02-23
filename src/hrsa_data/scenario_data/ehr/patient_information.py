import json
from dataclasses import dataclass, field, asdict
from typing import Any

from app_file_system.app_file_system_constants import AppFileSystemConstants
from .allergies_intolerances import AllergiesIntolerances
from .family_health_history import FamilyHealthHistory
from .medications import Medications
from .patient_demographics import PatientDemographics
from .patient_information_version import PatientInformationVersion
from .problems import Problems
from .social_health_history import SocialHealthHistory
from .vital_signs import VitalSigns

# Module Level Constants
__afsc__: AppFileSystemConstants = AppFileSystemConstants()

r"""
Reference: https://www.healthit.gov/isa/united-states-core-data-interoperability-uscdi#draft-uscdi-v3
"""


@dataclass
class PatientInformation:
    version: PatientInformationVersion = field(default_factory=PatientInformationVersion)
    patient_demographics: PatientDemographics = field(default_factory=PatientDemographics)
    problems: Problems = field(default_factory=Problems)
    medications: Medications = field(default_factory=Medications)
    allergies_intolerances: AllergiesIntolerances = field(default_factory=AllergiesIntolerances)
    vital_signs: VitalSigns = field(default_factory=VitalSigns)
    family_health_history: FamilyHealthHistory = field(default_factory=FamilyHealthHistory)
    social_health_history: SocialHealthHistory = field(default_factory=SocialHealthHistory)

    @staticmethod
    def from_dict(obj: Any) -> 'PatientInformation':
        _version = PatientInformationVersion.from_dict(obj.get("version"))
        _patient_demographics = PatientDemographics.from_dict(obj.get("patient_demographics"))
        _problems = Problems.from_dict(obj.get("problems"))
        _medications = Medications.from_dict(obj.get("medications"))
        _allergies_intolerances = AllergiesIntolerances.from_dict(obj.get("allergies_intolerances"))
        _vital_signs = VitalSigns.from_dict(obj.get("vital_signs"))
        _family_health_history = FamilyHealthHistory.from_dict(obj.get("family_health_history"))
        _social_health_history = SocialHealthHistory.from_dict(obj.get("social_health_history"))
        return PatientInformation(
            _version,
            _patient_demographics,
            _problems,
            _medications,
            _allergies_intolerances,
            _vital_signs,
            _family_health_history,
            _social_health_history
        )

    @classmethod
    def load_from_json_file(cls, json_file_path) -> 'PatientInformation':
        with open(json_file_path, 'r', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            return PatientInformation.from_dict(json.load(json_file))

    @staticmethod
    def save_to_json_file(obj: 'PatientInformation', json_file_path) -> bool:
        # TODO: Add error handling - save patient information to json file
        with open(json_file_path, 'w', encoding=__afsc__.DEFAULT_FILE_ENCODING) as json_file:
            json.dump(asdict(obj), json_file, indent=4)
            return True
