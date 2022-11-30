import dearpygui.dearpygui as dpg
import hrsa_cct_constants
import json

from configuration import character_model_data

model_data_list = []

patient_gender_combo = None
patient_ethnicity_combo = None

student_gender_combo = None
student_ethnicity_combo = None

trainer_gender_combo = None
trainer_ethnicity_combo = None

def _get_characters_of_type(condictions):
    data_of_type = []
    global model_data_list

    for data in model_data_list:
        matched = True
        for key in condictions:
            if not key in dir(data.metaData):
                matched = False
                break

            data_type = getattr(data.metaData, key)
            if not data_type == condictions[key]:
                matched = False
                break

        if matched:
            data_of_type.append(data)

    return data_of_type

def _load_character_config():
    global model_data_list
    with open('character_config/CharacterModelData.json', 'r', encoding='UTF-8') as character_config_file:
        row_data = character_config_file.read()
        row_config = json.loads(row_data)

        for data in row_config['ModelDataList']:
            item = character_model_data.CharacterModelData(**data)
            model_data_list.append(item)

        print(_get_characters_of_type({'CharacterType': 'kMedicalStudent'}))


def _log(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
    print(dpg.get_value(sender))
    # sender: 130, 	 app_data: White, 	 user_data: None


def _callback_update_filter(sender, app_data, user_data):
    global patient_gender_combo, patient_ethnicity_combo
    gender = dpg.get_value(patient_gender_combo)
    ethnicity = dpg.get_value(patient_ethnicity_combo)
    condictions = {}
    condictions['CharacterType'] = 'k' + user_data
    if not gender == 'None':
        condictions['GenderType'] = 'k' + gender
    if not ethnicity == 'None':
        condictions['EthnicityType'] = 'k' + ethnicity

    patients_data = _get_characters_of_type(condictions)
    for patient in patients_data:
        print(patient.uid)

def init_ui():
    _load_character_config()
    with dpg.collapsing_header(label="Character Config", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        # TODO: UI Creation
        dpg.add_text('Patient', indent=20)
        with dpg.group(horizontal=True, indent=20):
            global patient_gender_combo, patient_ethnicity_combo
            patient_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200, user_data='Patient')
            patient_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200, user_data='Patient')

        with dpg.group(horizontal=True, indent=20):
            global student_gender_combo, student_ethnicity_combo
            student_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200, user_data='MedicalStudent')
            student_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200, user_data='MedicalStudent')

        with dpg.group(horizontal=True, indent=20):
            global trainer_gender_combo, trainer_ethnicity_combo
            trainer_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200, user_data='Trainer')
            trainer_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200, user_data='Trainer')