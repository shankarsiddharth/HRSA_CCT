from dataclasses import dataclass, field
from typing import Any

from scenario.ehr.allergies_intolerances import AllergiesIntolerances
from scenario.ehr.family_health_history import FamilyHealthHistory
from scenario.ehr.medications import Medications
from scenario.ehr.patient_demographics import PatientDemographics
from scenario.ehr.patient_information_version import PatientInformationVersion
from scenario.ehr.problems import Problems
from scenario.ehr.social_health_history import SocialHealthHistory
from scenario.ehr.vital_signs import VitalSigns


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
