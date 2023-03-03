from hrsa_data.scenario_data.ehr.patient_information import PatientInformation


def translate_patient_info():
    # TODO: Translate patient info from one language to another.
    #   patient_info_es.json
    patient_info: PatientInformation = PatientInformation.load_from_json_file('patient_information_test.json')
    print(patient_info)
    patient_info.save_to_json_file(patient_info, 'patient_info_es.json')
    pass


if __name__ == '__main__':
    translate_patient_info()
