from hrsa_data.scenario_data.ehr.patient_information import PatientInformation
from hrsa_data.scenario_data.ehr.social_health_history import SocialHealthHistory
from text_translate.google_cloud.google_cloud_translate import GoogleCloudTranslate
from text_translate.google_cloud.google_cloud_translate_response_data import GoogleCloudTranslateResponseData


def translate_patient_info():
    # TODO: Translate patient info from one language to another.
    #   patient_info_es.json
    patient_info: PatientInformation = PatientInformation.load_from_json_file('patient_information_test.json')

    # translate problems
    gc_translate: GoogleCloudTranslate = GoogleCloudTranslate()
    for item in patient_info.problems.problems:
        translated_problem = item.problem
        if item.problem:
            gc_rd: GoogleCloudTranslateResponseData = gc_translate.translate_text(text=[item.problem],
                                                                                  target_language_code='es',
                                                                                  source_language_code='en-US')
            translated_problem = gc_rd.response_data[0].translated_text
        item.problem = translated_problem

    # translate family_health_history
    translated_family_health_history = []
    for item in patient_info.family_health_history.family_health_history:
        gc_rd: GoogleCloudTranslateResponseData = gc_translate.translate_text(text=[item],
                                                                              target_language_code='es',
                                                                              source_language_code='en-US')
        if len(gc_rd.response_data) > 0:
            translated_family_health_history.append(gc_rd.response_data[0].translated_text)
        else:
            translated_family_health_history.append(item)
    patient_info.family_health_history.family_health_history = translated_family_health_history

    # translate social_health_history
    social_health_history_dict = patient_info.social_health_history.to_dict()
    gc_rd: GoogleCloudTranslateResponseData = gc_translate.translate_text(text=list(social_health_history_dict.values()),
                                                                          target_language_code='es',
                                                                          source_language_code='en-US')
    social_health_history_values = [value.translated_text for value in gc_rd.response_data.values()]
    social_health_history_dict.update(zip(social_health_history_dict, social_health_history_values))
    patient_info.social_health_history = SocialHealthHistory.from_dict(social_health_history_dict)

    patient_info.save_to_json_file(patient_info, 'patient_info_es.json')


if __name__ == '__main__':
    translate_patient_info()
