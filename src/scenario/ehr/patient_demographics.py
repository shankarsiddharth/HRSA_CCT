from dataclasses import dataclass, field
from typing import Any


@dataclass
class PatientDemographics:
    first_name: str = field(default='')
    last_name: str = field(default='')
    middle_name: str = field(default='')
    suffix: str = field(default='')
    previous_name: str = field(default='')
    date_of_birth: str = field(default='')
    date_of_death: str = field(default='')
    age: str = field(default='')
    race: str = field(default='')
    ethnicity: str = field(default='')
    tribal_affiliation: str = field(default='')
    sex_assigned_at_birth: str = field(default='')
    sexual_orientation: str = field(default='')
    gender_identity: str = field(default='')
    preferred_language: str = field(default='')
    current_address: str = field(default='')
    previous_address: str = field(default='')
    phone_number: str = field(default='')
    phone_number_type: str = field(default='')
    email_address: str = field(default='')
    related_persons_name: str = field(default='')
    related_persons_relationship: str = field(default='')
    occupation: str = field(default='')
    occupation_history: str = field(default='')
    chief_complaint: str = field(default='')
    insurance: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'PatientDemographics':
        _first_name = str(obj.get("first_name"))
        _last_name = str(obj.get("last_name"))
        _middle_name = str(obj.get("middle_name"))
        _suffix = str(obj.get("suffix"))
        _previous_name = str(obj.get("previous_name"))
        _date_of_birth = str(obj.get("date_of_birth"))
        _date_of_death = str(obj.get("date_of_death"))
        _age = str(obj.get("age"))
        _race = str(obj.get("race"))
        _ethnicity = str(obj.get("ethnicity"))
        _tribal_affiliation = str(obj.get("tribal_affiliation"))
        _sex_assigned_at_birth = str(obj.get("sex_assigned_at_birth"))
        _sexual_orientation = str(obj.get("sexual_orientation"))
        _gender_identity = str(obj.get("gender_identity"))
        _preferred_language = str(obj.get("preferred_language"))
        _current_address = str(obj.get("current_address"))
        _previous_address = str(obj.get("previous_address"))
        _phone_number = str(obj.get("phone_number"))
        _phone_number_type = str(obj.get("phone_number_type"))
        _email_address = str(obj.get("email_address"))
        _related_persons_name = str(obj.get("related_persons_name"))
        _related_persons_relationship = str(obj.get("related_persons_relationship"))
        _occupation = str(obj.get("occupation"))
        _occupation_history = str(obj.get("occupation_history"))
        _chief_complaint = str(obj.get("chief_complaint"))
        _insurance = str(obj.get("insurance"))
        return PatientDemographics(
            _first_name,
            _last_name,
            _middle_name,
            _suffix,
            _previous_name,
            _date_of_birth,
            _date_of_death,
            _age,
            _race,
            _ethnicity,
            _tribal_affiliation,
            _sex_assigned_at_birth,
            _sexual_orientation,
            _gender_identity,
            _preferred_language,
            _current_address,
            _previous_address,
            _phone_number,
            _phone_number_type,
            _email_address,
            _related_persons_name,
            _related_persons_relationship,
            _occupation,
            _occupation_history,
            _chief_complaint,
            _insurance
        )
