import os.path

import dearpygui.dearpygui as dpg

from __v1 import hrsa_cct_constants, hrsa_cct_globals, cct_ui_panels, hrsa_cct_config
from hrsa_data.scenario_data.ehr.patient_demographics import PatientDemographics
from hrsa_data.scenario_data.ehr.patient_information import PatientInformation
from hrsa_data.scenario_data.ehr.problem import Problem
from hrsa_data.scenario_data.ehr.social_health_history import SocialHealthHistory
from hrsa_data.scenario_data.ehr.substance_information import SubstanceInformation
from hrsa_data.scenario_data.ehr.vital_signs import VitalSigns

patient_info: PatientInformation = PatientInformation()

piu_scenario_path = ''
patient_information_json_file_path = ''

PIU_SCENARIO_PATIENT_INFO_JSON_PATH_TEXT: str = 'PIU_SCENARIO_DIRECTORY_PATH_TEXT'
PIU_OPEN_FILE_DIALOG: str = 'PIU_OPEN_FILE_DIALOG'
PIU_PATIENT_INFO_GROUP: str = 'PIU_PATIENT_INFO_GROUP'

patient_demographics_header_name = 'Patient Demographics'
problems_header_name = 'Problems'
problems_list_header_name = 'Problems List'
sdoh_problems_header_name = 'SDOH Problems Health Concerns'
sdoh_problems_list_header_name = 'SDOH Problems List'
medications_header_name = 'Medications'
medications_list_header_name = 'Medications List'
allergies_intolerances_header_name = 'Allergies Intolerances'
allergies_intolerances_list_header_name = 'Allergies Intolerances List'
vital_signs_header_name = 'Vital Signs'
family_health_history_name = 'Family Health History'
family_health_history_list_name = 'Family Health History List'
social_health_history_header_name = 'Social Health History'


def set_scenario_path(scenario_path):
    global piu_scenario_path, patient_information_json_file_path
    piu_scenario_path = scenario_path
    patient_information_json_file_path = os.path.join(piu_scenario_path, hrsa_cct_globals.default_language_code,
                                                      hrsa_cct_constants.PATIENT_INFORMATION_JSON_FILE_NAME)
    dpg.configure_item(PIU_SCENARIO_PATIENT_INFO_JSON_PATH_TEXT, default_value=patient_information_json_file_path)
    _load_patient_info_file(patient_information_json_file_path)
    print('set_scenario_path ', patient_information_json_file_path)
    _toggle_patient_info_ui_sections(True)


def _load_patient_info_file(file_path_name: str):
    global patient_info, patient_information_json_file_path
    patient_information_json_file_path = file_path_name
    # Load the patient information from the JSON file
    if file_path_name != '':
        patient_info = PatientInformation.load_from_json_file(patient_information_json_file_path)

    header_name = patient_demographics_header_name
    fields_name = vars(PatientDemographics())
    for field_name in fields_name:
        field_value = getattr(patient_info.patient_demographics, field_name)
        dpg.set_value(_get_ui_object_tag(header_name, field_name), field_value)

    header_name = problems_list_header_name
    header_tag = _get_header_tag(header_name)
    dpg.delete_item(header_tag, children_only=True)
    for problem_id, _ in enumerate(patient_info.problems.problems):
        _add_problem_ui(problem_id)

    header_name = sdoh_problems_list_header_name
    header_tag = _get_header_tag(header_name)
    dpg.delete_item(header_tag, children_only=True)
    for sdoh_problem_id, _ in enumerate(patient_info.problems.sdoh_problems_health_concerns):
        _add_sdoh_problem_ui(sdoh_problem_id)

    header_name = medications_list_header_name
    header_tag = _get_header_tag(header_name)
    dpg.delete_item(header_tag, children_only=True)
    for medication_id, _ in enumerate(patient_info.medications.medications):
        _add_medication_ui(medication_id)

    header_name = allergies_intolerances_list_header_name
    header_tag = _get_header_tag(header_name)
    dpg.delete_item(header_tag, children_only=True)
    for allergy_id, _ in enumerate(patient_info.allergies_intolerances.substances):
        _add_allergy_ui(allergy_id)

    header_name = vital_signs_header_name
    fields_name = vars(VitalSigns())
    for field_name in fields_name:
        field_value = getattr(patient_info.vital_signs, field_name)
        dpg.set_value(_get_ui_object_tag(header_name, field_name), field_value)

    header_name = family_health_history_list_name
    header_tag = _get_header_tag(header_name)
    dpg.delete_item(header_tag, children_only=True)
    for family_history_id, _ in enumerate(patient_info.family_health_history.family_health_history):
        _add_family_health_history_ui(family_history_id)

    header_name = social_health_history_header_name
    fields_name = vars(SocialHealthHistory())
    for field_name in fields_name:
        field_value = getattr(patient_info.social_health_history, field_name)
        dpg.set_value(_get_ui_object_tag(header_name, field_name), field_value)


def _get_header_tag(header_name: str):
    header_tag = 'PIU_HEADER_{}'.format(header_name.upper().replace(' ', '_'))
    print(header_tag)
    return header_tag


def _get_ui_object_tag(header_name: str, node_name: str):
    ui_object_tag = 'PIU_{0}_{1}'.format(header_name.upper().replace(' ', '_'), node_name.upper().replace(' ', '_'))
    print(ui_object_tag)
    return ui_object_tag


def _get_ui_child_object_tag(header_name: str, node_name: str, index: int):
    ui_object_tag = 'PIU_{0}_{1}_{2}'.format(header_name.upper().replace(' ', '_'), index,
                                             node_name.upper().replace(' ', '_'))
    print(ui_object_tag)
    return ui_object_tag


def _callback_update_patient_demographics(sender, app_data, user_data):
    global patient_info
    node_name = user_data['node_name']
    setattr(patient_info.patient_demographics, node_name, app_data)


def _callback_add_problem(sender, app_data, user_data):
    global patient_info
    patient_info.problems.problems.append(Problem())
    problem_id = len(patient_info.problems.problems) - 1
    _add_problem_ui(problem_id)


def _add_problem_ui(problem_id: int):
    header_name = problems_list_header_name
    header_tag = _get_header_tag(header_name)
    global patient_info
    problem = patient_info.problems.problems[problem_id]
    with dpg.group(horizontal=True, indent=20, parent=header_tag,
                   tag=_get_ui_child_object_tag(header_name, 'button_group', problem_id)):
        dpg.add_text('Problem {0}: '.format(problem_id + 1),
                     tag=_get_ui_child_object_tag(header_name, 'title', problem_id),
                     user_data={'header_name': header_name, 'node_name': 'title', 'id': problem_id})
        dpg.add_button(label='Delete',
                       tag=_get_ui_child_object_tag(header_name, 'delete_button', problem_id),
                       user_data={'header_name': header_name, 'node_name': 'title', 'id': problem_id},
                       callback=_callback_delete_problem)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'problem', problem_id),
                       label='Problem',
                       user_data={'header_name': header_name, 'node_name': 'problem', 'id': problem_id},
                       default_value=problem.problem, parent=header_tag, indent=20,
                       callback=_callback_update_problem)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'date_of_diagnosis', problem_id),
                       label='Date of Diagnosis',
                       user_data={'header_name': header_name, 'node_name': 'date_of_diagnosis', 'id': problem_id},
                       default_value=problem.date_of_diagnosis, parent=header_tag, indent=20,
                       callback=_callback_update_problem)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'date_of_resolution', problem_id),
                       label='Date of Resolution',
                       user_data={'header_name': header_name, 'node_name': 'date_of_resolution', 'id': problem_id},
                       default_value=problem.date_of_resolution, parent=header_tag, indent=20,
                       callback=_callback_update_problem)


def _callback_delete_problem(sender, app_data, user_data):
    global patient_info
    header_name = problems_list_header_name
    problem_id = user_data['id']
    the_last_id = len(patient_info.problems.problems) - 1
    if problem_id > the_last_id:
        return
    for i in range(problem_id, the_last_id):
        next_problem = patient_info.problems.problems[i + 1]
        dpg.set_value(_get_ui_child_object_tag(header_name, 'title', i), 'Problem {0}: '.format(i + 1))
        dpg.set_value(_get_ui_child_object_tag(header_name, 'problem', i), next_problem.problem)
        dpg.set_value(_get_ui_child_object_tag(header_name, 'date_of_diagnosis', i), next_problem.date_of_diagnosis)
        dpg.set_value(_get_ui_child_object_tag(header_name, 'date_of_resolution', i), next_problem.date_of_resolution)

    del patient_info.problems.problems[problem_id]
    _delete_problem_ui(the_last_id)


def _callback_delete_last_problem(sender, app_data, user_data):
    global patient_info
    if len(patient_info.problems.problems) <= 0:
        return

    patient_info.problems.problems = patient_info.problems.problems[:-1]
    problem_id = len(patient_info.problems.problems)
    _delete_problem_ui(problem_id)


def _delete_problem_ui(problem_id: int):
    header_name = problems_list_header_name
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'button_group', problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'title', problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'delete_button', problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'problem', problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'date_of_diagnosis', problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'date_of_resolution', problem_id))


def _callback_update_problem(sender, app_data, user_data):
    global patient_info
    node_name = user_data['node_name']
    problem_id = user_data['id']

    if problem_id >= len(patient_info.problems.problems):
        return

    setattr(patient_info.problems.problems[problem_id], node_name, app_data)


def _callback_add_sdoh_problem(sender, app_data, user_data):
    global patient_info
    patient_info.problems.sdoh_problems_health_concerns.append(Problem())
    sdoh_problem_id = len(patient_info.problems.sdoh_problems_health_concerns) - 1
    _add_sdoh_problem_ui(sdoh_problem_id)


def _add_sdoh_problem_ui(sdoh_problem_id: int):
    header_name = sdoh_problems_list_header_name
    header_tag = _get_header_tag(header_name)
    global patient_info
    sdoh_problem = patient_info.problems.sdoh_problems_health_concerns[sdoh_problem_id]
    with dpg.group(horizontal=True, indent=20, parent=header_tag,
                   tag=_get_ui_child_object_tag(header_name, 'button_group', sdoh_problem_id)):
        dpg.add_text('Problem {0}: '.format(sdoh_problem_id + 1),
                     tag=_get_ui_child_object_tag(header_name, 'title', sdoh_problem_id),
                     user_data={'header_name': header_name, 'node_name': 'title', 'id': sdoh_problem_id})
        dpg.add_button(label='Delete',
                       tag=_get_ui_child_object_tag(header_name, 'delete_button', sdoh_problem_id),
                       user_data={'header_name': header_name, 'node_name': 'title', 'id': sdoh_problem_id},
                       callback=_callback_delete_sdoh_problem)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'problem', sdoh_problem_id),
                       label='Problem',
                       user_data={'header_name': header_name, 'node_name': 'problem', 'id': sdoh_problem_id},
                       default_value=sdoh_problem.problem, parent=header_tag, indent=20,
                       callback=_callback_update_sdoh_problem)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'date_of_diagnosis', sdoh_problem_id),
                       label='Date of Diagnosis',
                       user_data={'header_name': header_name, 'node_name': 'date_of_diagnosis', 'id': sdoh_problem_id},
                       default_value=sdoh_problem.date_of_diagnosis, parent=header_tag, indent=20,
                       callback=_callback_update_sdoh_problem)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'date_of_resolution', sdoh_problem_id),
                       label='Date of Resolution',
                       user_data={'header_name': header_name, 'node_name': 'date_of_resolution', 'id': sdoh_problem_id},
                       default_value=sdoh_problem.date_of_resolution, parent=header_tag, indent=20,
                       callback=_callback_update_sdoh_problem)


def _callback_delete_sdoh_problem(sender, app_data, user_data):
    global patient_info
    header_name = problems_list_header_name
    sdoh_problem_id = user_data['id']
    the_last_id = len(patient_info.problems.sdoh_problems_health_concerns) - 1
    if sdoh_problem_id > the_last_id:
        return
    for i in range(sdoh_problem_id, the_last_id):
        next_problem = patient_info.problems.problems[i + 1]
        dpg.set_value(_get_ui_child_object_tag(header_name, 'title', i), 'Problem {0}: '.format(i + 1))
        dpg.set_value(_get_ui_child_object_tag(header_name, 'problem', i), next_problem.problem)
        dpg.set_value(_get_ui_child_object_tag(header_name, 'date_of_diagnosis', i), next_problem.date_of_diagnosis)
        dpg.set_value(_get_ui_child_object_tag(header_name, 'date_of_resolution', i), next_problem.date_of_resolution)

    del patient_info.problems.sdoh_problems_health_concerns[sdoh_problem_id]
    _delete_sdoh_problem_ui(the_last_id)


def _callback_delete_last_sdoh_problem(sender, app_data, user_data):
    global patient_info
    if len(patient_info.problems.sdoh_problems_health_concerns) <= 0:
        return

    patient_info.problems.sdoh_problems_health_concerns = patient_info.problems.sdoh_problems_health_concerns[:-1]
    sdoh_problem_id = len(patient_info.problems.sdoh_problems_health_concerns)
    _delete_sdoh_problem_ui(sdoh_problem_id)


def _delete_sdoh_problem_ui(sdoh_problem_id: int):
    header_name = sdoh_problems_list_header_name
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'button_group', sdoh_problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'title', sdoh_problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'delete_button', sdoh_problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'problem', sdoh_problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'date_of_diagnosis', sdoh_problem_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'date_of_resolution', sdoh_problem_id))


def _callback_update_sdoh_problem(sender, app_data, user_data):
    global patient_info
    node_name = user_data['node_name']
    sdoh_problem_id = user_data['id']

    if sdoh_problem_id >= len(patient_info.problems.sdoh_problems_health_concerns):
        return

    setattr(patient_info.problems.sdoh_problems_health_concerns[sdoh_problem_id], node_name, app_data)


def _callback_add_medication(sender, app_data, user_data):
    global patient_info
    patient_info.medications.medications.append('')
    medication_id = len(patient_info.medications.medications) - 1
    _add_medication_ui(medication_id)


def _add_medication_ui(medication_id: int):
    header_name = medications_list_header_name
    header_tag = _get_header_tag(header_name)
    global patient_info
    medication = patient_info.medications.medications[medication_id]
    with dpg.group(horizontal=True, indent=20, parent=header_tag,
                   tag=_get_ui_child_object_tag(header_name, 'button_group', medication_id)):
        dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'medication', medication_id),
                           label='Medication {0}'.format(medication_id + 1),
                           user_data={'header_name': header_name, 'node_name': 'medication', 'id': medication_id},
                           default_value=medication, callback=_callback_update_medication)
        dpg.add_button(label='Delete',
                       tag=_get_ui_child_object_tag(header_name, 'delete_button', medication_id),
                       user_data={'header_name': header_name, 'id': medication_id},
                       callback=_callback_delete_medication)


def _callback_update_medication(sender, app_data, user_data):
    global patient_info

    medication_id = user_data['id']
    if medication_id >= len(patient_info.medications.medications):
        return

    patient_info.medications.medications[medication_id] = app_data


def _callback_delete_medication(sender, app_data, user_data):
    medication_id = user_data['id']
    global patient_info
    the_last_id = len(patient_info.medications.medications) - 1
    if medication_id > the_last_id:
        return
    header_name = medications_list_header_name
    for i in range(medication_id, the_last_id):
        next_medication = patient_info.medications.medications[i + 1]
        dpg.set_value(_get_ui_child_object_tag(header_name, 'medication', i), next_medication)
    del patient_info.medications.medications[medication_id]
    _delete_medication_ui(the_last_id)


def _callback_delete_last_medication(sender, app_data, user_data):
    global patient_info
    if len(patient_info.medications.medications) > 0:
        patient_info.medications.medications = patient_info.medications.medications[:-1]
        medication_id = len(patient_info.medications.medications)
        _delete_medication_ui(medication_id)


def _delete_medication_ui(medication_id: int):
    header_name = medications_list_header_name
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'button_group', medication_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'medication', medication_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'delete_button', medication_id))


def _callback_add_allergy(sender, app_data, user_data):
    global patient_info
    patient_info.allergies_intolerances.substances.append(SubstanceInformation())
    allergy_id = len(patient_info.allergies_intolerances.substances) - 1
    _add_allergy_ui(allergy_id)


def _add_allergy_ui(allergy_id: int):
    header_name = allergies_intolerances_list_header_name
    header_tag = _get_header_tag(header_name)
    global patient_info
    allergy = patient_info.allergies_intolerances.substances[allergy_id]
    with dpg.group(horizontal=True, indent=20, parent=header_tag,
                   tag=_get_ui_child_object_tag(header_name, 'button_group', allergy_id)):
        dpg.add_text('Substance {0}: '.format(allergy_id + 1),
                     tag=_get_ui_child_object_tag(header_name, 'title', allergy_id),
                     user_data={'header_name': header_name, 'node_name': 'title', 'id': allergy_id})
        dpg.add_button(label='Delete',
                       tag=_get_ui_child_object_tag(header_name, 'delete_button', allergy_id),
                       user_data={'header_name': header_name, 'id': allergy_id},
                       callback=_callback_delete_allergy)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'substance_medication', allergy_id),
                       label='Substance Medication',
                       user_data={'header_name': header_name, 'node_name': 'substance_medication', 'id': allergy_id},
                       default_value=allergy.substance_medication, parent=header_tag, indent=20,
                       callback=_callback_update_allergy)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'substance_drug_class', allergy_id),
                       label='Substance Drug Class',
                       user_data={'header_name': header_name, 'node_name': 'substance_drug_class', 'id': allergy_id},
                       default_value=allergy.substance_drug_class, parent=header_tag, indent=20,
                       callback=_callback_update_allergy)
    dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'reaction', allergy_id),
                       label='Reaction',
                       user_data={'header_name': header_name, 'node_name': 'reaction', 'id': allergy_id},
                       default_value=allergy.reaction, parent=header_tag, indent=20,
                       callback=_callback_update_allergy)


def _callback_update_allergy(sender, app_data, user_data):
    global patient_info
    node_name = user_data['node_name']
    allergy_id = user_data['id']
    if allergy_id >= len(patient_info.allergies_intolerances.substances):
        return
    setattr(patient_info.allergies_intolerances.substances[allergy_id], node_name, app_data)


def _callback_delete_allergy(sender, app_data, user_data):
    allergy_id = user_data['id']
    global patient_info
    the_last_id = len(patient_info.allergies_intolerances.substances) - 1
    if allergy_id > the_last_id:
        return
    header_name = allergies_intolerances_list_header_name
    for i in range(allergy_id, the_last_id):
        next_allergy = patient_info.allergies_intolerances.substances[i + 1]
        dpg.set_value(_get_ui_child_object_tag(header_name, 'title', i), 'Substance {0}: '.format(i + 1))
        dpg.set_value(_get_ui_child_object_tag(header_name, 'substance_medication', i),
                      next_allergy.substance_medication)
        dpg.set_value(_get_ui_child_object_tag(header_name, 'substance_drug_class', i),
                      next_allergy.substance_drug_class)
        dpg.set_value(_get_ui_child_object_tag(header_name, 'reaction', i), next_allergy.reaction)
    del patient_info.allergies_intolerances.substances[allergy_id]
    _delete_allergy_ui(the_last_id)


def _callback_delete_last_allergy(sender, app_data, user_data):
    global patient_info

    if len(patient_info.allergies_intolerances.substances) <= 0:
        return

    patient_info.allergies_intolerances.substances = patient_info.allergies_intolerances.substances[:-1]
    allergy_id = len(patient_info.allergies_intolerances.substances)
    _delete_allergy_ui(allergy_id)


def _delete_allergy_ui(allergy_id: int):
    header_name = allergies_intolerances_list_header_name
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'button_group', allergy_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'title', allergy_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'delete_button', allergy_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'substance_medication', allergy_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'substance_drug_class', allergy_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'reaction', allergy_id))


def _callback_add_family_health_history(sender, app_data, user_data):
    global patient_info
    patient_info.family_health_history.family_health_history.append('')
    family_health_history_id = len(patient_info.family_health_history.family_health_history) - 1
    _add_family_health_history_ui(family_health_history_id)


def _add_family_health_history_ui(family_health_history_id: int):
    header_name = family_health_history_list_name
    header_tag = _get_header_tag(header_name)
    global patient_info
    family_health_history = patient_info.family_health_history.family_health_history[family_health_history_id]
    with dpg.group(horizontal=True, indent=20, parent=header_tag,
                   tag=_get_ui_child_object_tag(header_name, 'button_group', family_health_history_id)):
        dpg.add_input_text(tag=_get_ui_child_object_tag(header_name, 'family_health_history', family_health_history_id),
                           user_data={'header_name': header_name, 'node_name': 'family_health_history',
                                      'id': family_health_history_id},
                           default_value=family_health_history,
                           callback=_callback_update_family_health_history)
        dpg.add_button(label='Delete',
                       tag=_get_ui_child_object_tag(header_name, 'delete_button', family_health_history_id),
                       user_data={'header_name': header_name, 'id': family_health_history_id},
                       callback=_callback_delete_family_health_history)


def _callback_delete_family_health_history(sender, app_data, user_data):
    family_health_history_id = user_data['id']
    global patient_info
    last_history_id = len(patient_info.family_health_history.family_health_history) - 1
    if family_health_history_id > last_history_id:
        return
    header_name = family_health_history_list_name
    for i in range(family_health_history_id, last_history_id):
        next_history = patient_info.family_health_history.family_health_history[i + 1]
        dpg.set_value(_get_ui_child_object_tag(header_name, 'family_health_history', i), next_history)
    del patient_info.family_health_history.family_health_history[family_health_history_id]
    _delete_family_health_history_ui(last_history_id)


def _callback_delete_last_family_health_history(sender, app_data, user_data):
    global patient_info
    if len(patient_info.family_health_history.family_health_history) <= 0:
        return

    patient_info.family_health_history.family_health_history = patient_info.family_health_history.family_health_history[
                                                               :-1]
    family_health_history_id = len(patient_info.family_health_history.family_health_history)

    _delete_family_health_history_ui(family_health_history_id)


def _delete_family_health_history_ui(family_health_history_id: int):
    header_name = family_health_history_list_name
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'button_group', family_health_history_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'family_health_history', family_health_history_id))
    dpg.delete_item(_get_ui_child_object_tag(header_name, 'delete_button', family_health_history_id))


def _callback_update_family_health_history(sender, app_data, user_data):
    global patient_info
    family_health_history_id = user_data['id']
    patient_info.family_health_history.family_health_history[family_health_history_id] = app_data


def _callback_update_patient_vital_signs(sender, app_data, user_data):
    global patient_info
    node_name = user_data['node_name']
    setattr(patient_info.vital_signs, node_name, app_data)


def _callback_update_social_health_history(sender, app_data, user_data):
    global patient_info
    node_name = user_data['node_name']
    setattr(patient_info.social_health_history, node_name, app_data)


def _callback_export_patient_info(sender, app_data, user_data):
    global patient_info
    if patient_information_json_file_path == '':
        return
    # Save the patient information to a JSON file
    PatientInformation.save_to_json_file(patient_info, patient_information_json_file_path)


def _toggle_patient_info_ui_sections(value: bool):
    dpg.configure_item(PIU_PATIENT_INFO_GROUP, show=value)


def file_dialog_confirm_callback(sender, app_data, user_data):
    file_path_name = app_data["file_path_name"]
    _load_patient_info_file(file_path_name)
    dpg.configure_item(PIU_SCENARIO_PATIENT_INFO_JSON_PATH_TEXT, default_value=file_path_name)
    _toggle_patient_info_ui_sections(True)


def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


def init_ui():
    with dpg.collapsing_header(label='Patient Info UI', tag=cct_ui_panels.CCT_PATIENT_INFO_COLLAPSING_HEADER,
                               default_open=False):
        # TODO: Add a 'Clear Data Button' that clears all the UI information

        dpg.add_text(tag=PIU_SCENARIO_PATIENT_INFO_JSON_PATH_TEXT)

        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=file_dialog_confirm_callback, tag=PIU_OPEN_FILE_DIALOG,
                             modal=True, default_path=hrsa_cct_config.get_file_dialog_default_path(),
                             cancel_callback=file_dialog_cancel_callback):
            dpg.add_file_extension(".json", color=(255, 255, 0, 255))
        with dpg.group(horizontal=True):
            dpg.add_button(label="Select Patient Info Config JSON File...",
                           callback=lambda: dpg.show_item(PIU_OPEN_FILE_DIALOG))

        # region Patient Info UI Sections
        with dpg.group(show=False, tag=PIU_PATIENT_INFO_GROUP):
            # region Patient Demographics
            header_name = patient_demographics_header_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'first_name'), label='First Name',
                                   user_data={'header_name': header_name, 'node_name': 'first_name'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'last_name'), label='Last Name',
                                   user_data={'header_name': header_name, 'node_name': 'last_name'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'middle_name'), label='Middle Name',
                                   user_data={'header_name': header_name, 'node_name': 'middle_name'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'suffix'), label='Suffix',
                                   user_data={'header_name': header_name, 'node_name': 'suffix'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'previous_name'), label='Previous Name',
                                   user_data={'header_name': header_name, 'node_name': 'previous_name'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'date_of_birth'), label='Date of Birth',
                                   user_data={'header_name': header_name, 'node_name': 'date_of_birth'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'date_of_death'), label='Date of Death',
                                   user_data={'header_name': header_name, 'node_name': 'date_of_death'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'age'), label='Age',
                                   user_data={'header_name': header_name, 'node_name': 'age'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'race'), label='Race',
                                   user_data={'header_name': header_name, 'node_name': 'race'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'ethnicity'), label='Ethnicity',
                                   user_data={'header_name': header_name, 'node_name': 'ethnicity'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'tribal_affiliation'), label='Tribal Affiliation',
                                   user_data={'header_name': header_name, 'node_name': 'tribal_affiliation'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'sex_assigned_at_birth'),
                                   label='Sex Assigned at Birth',
                                   user_data={'header_name': header_name, 'node_name': 'sex_assigned_at_birth'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'sexual_orientation'), label='Sexual Orientation',
                                   user_data={'header_name': header_name, 'node_name': 'sexual_orientation'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'gender_identity'), label='Gender Identity',
                                   user_data={'header_name': header_name, 'node_name': 'gender_identity'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'preferred_language'), label='Preferred Language',
                                   user_data={'header_name': header_name, 'node_name': 'preferred_language'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'current_address'), label='Current Address',
                                   user_data={'header_name': header_name, 'node_name': 'current_address'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'previous_address'), label='Previous Address',
                                   user_data={'header_name': header_name, 'node_name': 'previous_address'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'phone_number'), label='Phone Number',
                                   user_data={'header_name': header_name, 'node_name': 'phone_number'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'phone_number_type'), label='Phone Number Type',
                                   user_data={'header_name': header_name, 'node_name': 'phone_number_type'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'email_address'), label='Email Address',
                                   user_data={'header_name': header_name, 'node_name': 'email_address'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'related_persons_name'),
                                   label='Related Persons Name',
                                   user_data={'header_name': header_name, 'node_name': 'related_persons_name'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'related_persons_relationship'),
                                   label='Related Persons Relationship',
                                   user_data={'header_name': header_name, 'node_name': 'related_persons_relationship'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'occupation'), label='Occupation',
                                   user_data={'header_name': header_name, 'node_name': 'occupation'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'occupation_history'), label='Occupation History',
                                   user_data={'header_name': header_name, 'node_name': 'occupation_history'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'chief_complaint'), label='Chief Complaint',
                                   user_data={'header_name': header_name, 'node_name': 'chief_complaint'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'insurance'), label='Insurance',
                                   user_data={'header_name': header_name, 'node_name': 'insurance'},
                                   default_value='', indent=20, callback=_callback_update_patient_demographics)
            # endregion Patient Demographics

            # region Problems
            header_name = problems_header_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                with dpg.group(horizontal=True, indent=20):
                    dpg.add_button(label='Add Problem', callback=_callback_add_problem)
                    dpg.add_button(label='Delete The Last Problem', callback=_callback_delete_last_problem)
                with dpg.group(tag=_get_header_tag(problems_list_header_name), indent=20):
                    pass
            # endregion Problems

            # region SDOH Problems Health Concerns
            header_name = sdoh_problems_header_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                with dpg.group(horizontal=True, indent=20):
                    dpg.add_button(label='Add SDOH Problem', callback=_callback_add_sdoh_problem)
                    dpg.add_button(label='Delete The Last SDOH Problem', callback=_callback_delete_last_sdoh_problem)
                with dpg.group(tag=_get_header_tag(sdoh_problems_list_header_name), indent=20):
                    pass
            # endregion SDOH Problems Health Concerns

            # region Medications
            header_name = medications_header_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                with dpg.group(horizontal=True, indent=20):
                    dpg.add_button(label='Add Medication', callback=_callback_add_medication)
                    dpg.add_button(label='Delete The Last Medication', callback=_callback_delete_last_medication)
                with dpg.group(tag=_get_header_tag(medications_list_header_name), indent=20):
                    pass
            # endregion Medications

            # region Allergies Intolerances
            header_name = allergies_intolerances_header_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                with dpg.group(horizontal=True, indent=20):
                    dpg.add_button(label='Add Allergy', callback=_callback_add_allergy)
                    dpg.add_button(label='Delete The Last Allergy', callback=_callback_delete_last_allergy)
                with dpg.group(tag=_get_header_tag(allergies_intolerances_list_header_name), indent=20):
                    pass
            # endregion Allergies Intolerances

            # region Vital Signs
            header_name = vital_signs_header_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'systolic_blood_pressure'),
                                   label='Systolic Blood Pressure',
                                   user_data={'header_name': header_name, 'node_name': 'systolic_blood_pressure'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'diastolic_blood_pressure'),
                                   label='Diastolic Blood_pressure',
                                   user_data={'header_name': header_name, 'node_name': 'diastolic_blood_pressure'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'heart_rate'), label='Heart Rate',
                                   user_data={'header_name': header_name, 'node_name': 'heart_rate'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'respiratory_rate'), label='Respiratory Rate',
                                   user_data={'header_name': header_name, 'node_name': 'respiratory_rate'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'body_temperature'), label='Body Temperature',
                                   user_data={'header_name': header_name, 'node_name': 'body_temperature'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'body_height'), label='Body Height',
                                   user_data={'header_name': header_name, 'node_name': 'body_height'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'body_weight'), label='Body Weight',
                                   user_data={'header_name': header_name, 'node_name': 'body_weight'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'pulse_oximetry'), label='Pulse Oximetry',
                                   user_data={'header_name': header_name, 'node_name': 'pulse_oximetry'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'inhaled_oxygen_concentration'),
                                   label='Inhaled Oxygen Concentration',
                                   user_data={'header_name': header_name, 'node_name': 'inhaled_oxygen_concentration'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'bmi_percentile_2_to_20_years'),
                                   label='BMI Percentile 2 to 20 years',
                                   user_data={'header_name': header_name, 'node_name': 'bmi_percentile_2_to_20_years'},
                                   default_value='', indent=20, callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'weight_for_length_percentile_birth_36_months'),
                                   label='Weight for Length Percentile birth 36 months', default_value='', indent=20,
                                   user_data={'header_name': header_name,
                                              'node_name': 'weight_for_length_percentile_birth_36_months'},
                                   callback=_callback_update_patient_vital_signs)
                dpg.add_input_text(
                    tag=_get_ui_object_tag(header_name, 'head_occipital_frontal_circumference_percentile_birth_36_months'),
                    label='Head Occipital frontal circumference percentile birth 36 months',
                    user_data={'header_name': header_name,
                               'node_name': 'head_occipital_frontal_circumference_percentile_birth_36_months'},
                    default_value='', indent=20,
                    callback=_callback_update_patient_vital_signs)
            # endregion Vital Signs

            # region Family Health History
            header_name = family_health_history_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                with dpg.group(horizontal=True, indent=20):
                    dpg.add_button(label='Add Family History', callback=_callback_add_family_health_history)
                    dpg.add_button(label='Delete The Last Family History',
                                   callback=_callback_delete_last_family_health_history)
                with dpg.group(tag=_get_header_tag(family_health_history_list_name), indent=20):
                    pass
            # endregion Family Health History

            # region Social Health History
            header_name = social_health_history_header_name
            with dpg.collapsing_header(label=header_name, tag=_get_header_tag(header_name), default_open=True, indent=20):
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'social_history_observation'),
                                   label='Social History Observation',
                                   user_data={'header_name': header_name, 'node_name': 'social_history_observation'},
                                   default_value='', indent=20, callback=_callback_update_social_health_history)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'alcohol_use'), label='Alcohol Use',
                                   user_data={'header_name': header_name, 'node_name': 'alcohol_use'},
                                   default_value='', indent=20, callback=_callback_update_social_health_history)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'drug_use'),
                                   user_data={'header_name': header_name, 'node_name': 'drug_use'},
                                   label='Drug Use', default_value='', indent=20)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'sexual_activity'), label='Sexual Activity',
                                   user_data={'header_name': header_name, 'node_name': 'sexual_activity'},
                                   default_value='', indent=20, callback=_callback_update_social_health_history)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'refugee_status'), label='Refugee Status',
                                   user_data={'header_name': header_name, 'node_name': 'refugee_status'},
                                   default_value='', indent=20, callback=_callback_update_social_health_history)
                dpg.add_input_text(tag=_get_ui_object_tag(header_name, 'congregate_living'), label='Congregate Living',
                                   user_data={'header_name': header_name, 'node_name': 'congregate_living'},
                                   default_value='', indent=20, callback=_callback_update_social_health_history)
            # endregion Social Health History

            dpg.add_button(label='Save Patient Information', callback=_callback_export_patient_info)
        # endregion Patient Information UI Sections


def init_data():
    _load_patient_info_file(file_path_name="")
