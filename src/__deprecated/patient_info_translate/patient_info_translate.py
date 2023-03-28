from dataclasses import asdict

from hrsa_data.scenario_data.ehr.patient_information import PatientInformation
from hrsa_data.scenario_data.ehr.social_health_history import SocialHealthHistory
from text_translate.google_cloud.google_cloud_translate import GoogleCloudTranslate
from text_translate.google_cloud.google_cloud_translate_response_data import GoogleCloudTranslateResponseData


def translate_patient_info(file_path: str = None):
    # TODO: Translate patient info from one language to another.
    #   patient_info_es.json
    if file_path is None:
        return
    # TODO: [FIXME] Translation Fails if the content has empty strings
    #   for example, in social_health_history...
    #   if the dict key value is empty string, then the translation fails from that key onwards
    patient_info: PatientInformation = PatientInformation.load_from_json_file(file_path)

    # translate problems
    gc_translate: GoogleCloudTranslate = GoogleCloudTranslate()
    for item in patient_info.problems.problems:
        translated_problem = item.problem
        if item.problem:
            gc_rd: GoogleCloudTranslateResponseData = gc_translate.translate_text(text_content_list=[item.problem],
                                                                                  target_language_code='es',
                                                                                  source_language_code='en-US')
            translated_problem = gc_rd.response_data[0].translated_text
        item.problem = translated_problem

    # translate family_health_history
    translated_family_health_history = []
    for item in patient_info.family_health_history.family_health_history:
        gc_rd: GoogleCloudTranslateResponseData = gc_translate.translate_text(text_content_list=[item],
                                                                              target_language_code='es',
                                                                              source_language_code='en-US')
        if len(gc_rd.response_data) > 0:
            translated_family_health_history.append(gc_rd.response_data[0].translated_text)
        else:
            translated_family_health_history.append(item)
    patient_info.family_health_history.family_health_history = translated_family_health_history

    # translate social_health_history
    social_health_history_dict = asdict(patient_info.social_health_history)
    gc_rd: GoogleCloudTranslateResponseData = gc_translate.translate_text(text_content_list=list(social_health_history_dict.values()),
                                                                          target_language_code='es',
                                                                          source_language_code='en-US')
    social_health_history_values = [value.translated_text for value in gc_rd.response_data.values()]
    social_health_history_dict.update(zip(social_health_history_dict, social_health_history_values))
    patient_info.social_health_history = SocialHealthHistory.from_dict(social_health_history_dict)

    patient_info.save_to_json_file(patient_info, file_path)
