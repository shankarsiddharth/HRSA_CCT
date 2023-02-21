from dataclasses import dataclass, field
from typing import Any


@dataclass
class VitalSigns:
    systolic_blood_pressure: str = field(default='')
    diastolic_blood_pressure: str = field(default='')
    heart_rate: str = field(default='')
    respiratory_rate: str = field(default='')
    body_temperature: str = field(default='')
    body_height: str = field(default='')
    body_weight: str = field(default='')
    pulse_oximetry: str = field(default='')
    inhaled_oxygen_concentration: str = field(default='')
    bmi_percentile_2_to_20_years: str = field(default='')
    weight_for_length_percentile_birth_36_months: str = field(default='')
    head_occipital_frontal_circumference_percentile_birth_36_months: str = field(default='')

    @staticmethod
    def from_dict(obj: Any) -> 'VitalSigns':
        _systolic_blood_pressure = str(obj.get("systolic_blood_pressure"))
        _diastolic_blood_pressure = str(obj.get("diastolic_blood_pressure"))
        _heart_rate = str(obj.get("heart_rate"))
        _respiratory_rate = str(obj.get("respiratory_rate"))
        _body_temperature = str(obj.get("body_temperature"))
        _body_height = str(obj.get("body_height"))
        _body_weight = str(obj.get("body_weight"))
        _pulse_oximetry = str(obj.get("pulse_oximetry"))
        _inhaled_oxygen_concentration = str(obj.get("inhaled_oxygen_concentration"))
        _bmi_percentile_2_to_20_years = str(obj.get("bmi_percentile_2_to_20_years"))
        _weight_for_length_percentile_birth_36_months = str(obj.get("weight_for_length_percentile_birth_36_months"))
        _head_occipital_frontal_circumference_percentile_birth_36_months = str(obj.get("head_occipital_frontal_circumference_percentile_birth_36_months"))
        return VitalSigns(
            _systolic_blood_pressure,
            _diastolic_blood_pressure,
            _heart_rate,
            _respiratory_rate,
            _body_temperature,
            _body_height,
            _body_weight,
            _pulse_oximetry,
            _inhaled_oxygen_concentration,
            _bmi_percentile_2_to_20_years,
            _weight_for_length_percentile_birth_36_months,
            _head_occipital_frontal_circumference_percentile_birth_36_months
        )
