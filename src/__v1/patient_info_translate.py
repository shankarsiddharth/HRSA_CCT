import sys
from dataclasses import asdict

from hrsa_data.scenario_data.ehr.patient_information import PatientInformation
from hrsa_data.scenario_data.ehr.social_health_history import SocialHealthHistory
from hrsa_data.scenario_data.ehr.vital_signs import VitalSigns
from text_translate.google_cloud.google_cloud_translate import GoogleCloudTranslate
from text_translate.google_cloud.google_cloud_translate_response_data import GoogleCloudTranslateResponseData


# TODO: Use source language code and target language code for translation
def translate_patient_info(file_path: str = None):
    if file_path is None:
        return
    patient_info: PatientInformation = PatientInformation.load_from_json_file(file_path)

    # translate demographics
    # patient_info_demographics_dict = asdict(patient_info.patient_demographics)
    # for key, value in patient_info_demographics_dict.items():
    #     patient_info_demographics_dict[key] = translate_text_from_en_to_es(value)
    # patient_info.patient_demographics = PatientDemographics.from_dict(patient_info_demographics_dict)
    patient_info.patient_demographics.occupation = translate_text_from_en_to_es(patient_info.patient_demographics.occupation)
    patient_info.patient_demographics.occupation_history = translate_text_from_en_to_es(patient_info.patient_demographics.occupation_history)
    patient_info.patient_demographics.chief_complaint = translate_text_from_en_to_es(patient_info.patient_demographics.chief_complaint)
    patient_info.patient_demographics.insurance = translate_text_from_en_to_es(patient_info.patient_demographics.insurance)

    # translate problems
    for item in patient_info.problems.problems:
        item.problem = translate_text_from_en_to_es(item.problem)

    # translate SDOH problems
    for item in patient_info.problems.sdoh_problems_health_concerns:
        item.problem = translate_text_from_en_to_es(item.problem)

    # # translate medications
    # translated_medication_list = []
    # for item in patient_info.medications.medications:
    #     translated_medication_list.append(translate_text_from_en_to_es(item))
    # patient_info.medications.medications = translated_medication_list

    # translate Allergies and Intolerances - Substances
    for substance_item in patient_info.allergies_intolerances.substances:
        substance_item.substance_medication = translate_text_from_en_to_es(substance_item.substance_medication)
        substance_item.reaction = translate_text_from_en_to_es(substance_item.reaction)
        substance_item.substance_drug_class = translate_text_from_en_to_es(substance_item.substance_drug_class)

    # translate vital_signs
    vital_signs_dict = asdict(patient_info.vital_signs)
    for key, value in vital_signs_dict.items():
        vital_signs_dict[key] = translate_text_from_en_to_es(value)
    patient_info.vital_signs = VitalSigns.from_dict(vital_signs_dict)

    # translate family_health_history
    translated_family_health_history = []
    for item in patient_info.family_health_history.family_health_history:
        translated_family_health_history.append(translate_text_from_en_to_es(item))
    patient_info.family_health_history.family_health_history = translated_family_health_history

    # translate social_health_history
    social_health_history_dict = asdict(patient_info.social_health_history)
    for key, value in social_health_history_dict.items():
        social_health_history_dict[key] = translate_text_from_en_to_es(value)
    patient_info.social_health_history = SocialHealthHistory.from_dict(social_health_history_dict)

    patient_info.save_to_json_file(patient_info, file_path)


def translate_text_from_en_to_es(text: str = None) -> str:
    if text is None or text == '':
        return ''
    gc_translate: GoogleCloudTranslate = GoogleCloudTranslate()
    gc_rd: GoogleCloudTranslateResponseData = gc_translate.translate_text(text_content_list=[text],
                                                                          target_language_code='es',
                                                                          source_language_code='en-US')
    return gc_rd.response_data[0].translated_text


if sys.flags.dev_mode:
    print("patient_info_translate.__init__()")
