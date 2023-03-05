import json
import os.path
import unittest
from dataclasses import asdict
from types import SimpleNamespace

from hrsa_data.scenario_data.ehr.patient_information import PatientInformation
from tests.helper import get_test_path_of_file, afsc


class TestPatientInformationLoading(unittest.TestCase):

    file_to_create = os.path.join(get_test_path_of_file(__file__), 'new_patient_information.json')
    file_to_test = os.path.join(get_test_path_of_file(__file__), 'patient_information_test.json')

    def process_patient_information_data(self, patient_information_data: PatientInformation):
        # print(patient_information_data, '\n')
        self.assertEqual(
            patient_information_data.patient_demographics.first_name,
            'Sofia'
        )
        self.assertEqual(
            patient_information_data.patient_demographics.occupation,
            'Works at a turkey processing plant'
        )
        self.assertEqual(
            patient_information_data.problems.problems[0].problem,
            'Weight Gain'
        )
        self.assertEqual(
            patient_information_data.problems.problems[0].date_of_diagnosis,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.problems[2].problem,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.problems[2].date_of_diagnosis,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.sdoh_problems_health_concerns[0].problem,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.sdoh_problems_health_concerns[0].date_of_diagnosis,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.sdoh_problems_health_concerns[2].problem,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.sdoh_problems_health_concerns[2].date_of_diagnosis,
            ''
        )
        self.assertEqual(
            patient_information_data.medications.medications[0],
            'Lisinopril 10mg daily'
        )
        self.assertEqual(
            patient_information_data.medications.medications[2],
            'Acetaminophen 1000mg four times a day'
        )
        self.assertEqual(
            patient_information_data.allergies_intolerances.substances[0].substance_medication,
            'No known allergies'
        )
        self.assertEqual(
            patient_information_data.allergies_intolerances.substances[0].reaction,
            ''
        )
        self.assertEqual(
            patient_information_data.allergies_intolerances.substances[2].substance_medication,
            ''
        )
        self.assertEqual(
            patient_information_data.allergies_intolerances.substances[2].reaction,
            ''
        )
        self.assertEqual(
            patient_information_data.vital_signs.systolic_blood_pressure,
            '150'
        )
        self.assertEqual(
            patient_information_data.vital_signs.head_occipital_frontal_circumference_percentile_birth_36_months,
            ''
        )
        self.assertEqual(
            patient_information_data.family_health_history.family_health_history[0],
            ''
        )
        self.assertEqual(
            patient_information_data.family_health_history.family_health_history[2],
            ''
        )
        self.assertEqual(
            patient_information_data.social_health_history.social_history_observation,
            ''
        )
        self.assertEqual(
            patient_information_data.social_health_history.alcohol_use,
            '1-2 glasses of beer, 3 times per week'
        )
        self.assertEqual(
            patient_information_data.social_health_history.congregate_living,
            ''
        )

    def test_load_from_string(self):
        with open(self.file_to_test, encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            text = f.read()
            # Parse JSON into an object with attributes corresponding to dict keys.
            patient_information_data: PatientInformation = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))
            self.process_patient_information_data(patient_information_data)

    def test_load_from_dict(self):
        with open(self.file_to_test, encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            patient_information_data: PatientInformation = PatientInformation.from_dict(json.load(f))
            print(json.dumps(asdict(patient_information_data)), '\n')
            self.process_patient_information_data(patient_information_data)

    def test_create_object(self):
        patient_information_data = PatientInformation()
        print(json.dumps(asdict(patient_information_data)), '\n')
        self.assertEqual(
            patient_information_data.patient_demographics.first_name,
            ''
        )
        self.assertEqual(
            patient_information_data.patient_demographics.insurance,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.problems[0].problem,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.problems[0].date_of_diagnosis,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.sdoh_problems_health_concerns[0].problem,
            ''
        )
        self.assertEqual(
            patient_information_data.problems.sdoh_problems_health_concerns[0].date_of_diagnosis,
            ''
        )
        self.assertEqual(
            patient_information_data.medications.medications[0],
            ''
        )
        self.assertEqual(
            patient_information_data.allergies_intolerances.substances[0].substance_medication,
            ''
        )
        self.assertEqual(
            patient_information_data.allergies_intolerances.substances[0].reaction,
            ''
        )
        self.assertEqual(
            patient_information_data.vital_signs.systolic_blood_pressure,
            ''
        )
        self.assertEqual(
            patient_information_data.vital_signs.head_occipital_frontal_circumference_percentile_birth_36_months,
            ''
        )
        self.assertEqual(
            patient_information_data.family_health_history.family_health_history[0],
            ''
        )
        self.assertEqual(
            patient_information_data.social_health_history.social_history_observation,
            ''
        )
        self.assertEqual(
            patient_information_data.social_health_history.congregate_living,
            ''
        )

    def test_create_new_file(self):
        config_data: PatientInformation = PatientInformation()
        with open(self.file_to_create, 'w', encoding=afsc.DEFAULT_FILE_ENCODING) as f:
            json.dump(asdict(config_data), f, indent=4)


if __name__ == '__main__':
    unittest.main()
