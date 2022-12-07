import dearpygui.dearpygui as dpg
import hrsa_cct_constants
import json

from configuration import character_model_data
from configuration import hrsa_config

model_data_list = []

patient_gender_combo = None
patient_ethnicity_combo = None

student_gender_combo = None
student_ethnicity_combo = None

trainer_gender_combo = None
trainer_ethnicity_combo = None

patient_model_window = None
patient_model_detail_window = None

student_model_window = None
student_model_detail_window = None

trainer_model_window = None
trainer_model_detail_window = None

loaded_texture = []

app_config = None


def _get_characters_of_type(conditions):
    print('search conditions ', conditions)
    data_of_type = []
    global model_data_list

    for data in model_data_list:
        matched = True
        for key in conditions:
            if not key in dir(data.metaData):
                matched = False
                break

            data_type = getattr(data.metaData, key)
            if not data_type == conditions[key]:
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
        # print(_get_characters_of_type({'CharacterType': 'kMedicalStudent'}))


def _log(sender, app_data, user_data):
    # print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
    # print(dpg.get_value(sender))
    pass
    # sender: 130, 	 app_data: White, 	 user_data: None

def _mouse_click_callback(sender, app_data, user_data):
    print(f"mouse click sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
    if dpg.is_item_clicked('uid_MedStudent1'):
        print('True')
        global loaded_texture
        if 'MedStudent1_0' not in loaded_texture:
            # print('texture not loaded')
            _load_character_model_image('MedStudent1_0')
        dpg.set_value('uid_MedStudent1', 'MedStudent1_0')

def _update_model_config(sender, app_data, user_data):
    uid = sender.replace('uid_', '')
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")

    global loaded_texture
    detail_texture = uid + '_0'
    if detail_texture not in loaded_texture:
        print('texture not loaded ', detail_texture)
        _load_character_model_image(detail_texture)

    global patient_model_detail_window, student_model_detail_window, trainer_model_detail_window
    global app_config
    if user_data == 'Patient':
        if app_config is not None:
            app_config.patient.model_config.uid = uid
        dpg.delete_item(patient_model_detail_window, children_only=True)
        dpg.add_image(detail_texture, tag='detail_' + uid, parent=patient_model_detail_window)
    elif user_data == 'MedicalStudent':
        if app_config is not None:
            app_config.medicalstudent.model_config.uid = uid
        dpg.delete_item(student_model_detail_window, children_only=True)
        dpg.add_image(detail_texture, tag='detail_' + uid, parent=student_model_detail_window)
    elif user_data == 'Trainer':
        if app_config is not None:
            app_config.trainer.model_config.uid = uid
        dpg.delete_item(trainer_model_detail_window, children_only=True)
        dpg.add_image(detail_texture, tag='detail_' + uid, parent=trainer_model_detail_window)


def _load_character_model_image(image_name):
    width, height, channels, data = dpg.load_image('assets/avatar/' + image_name + '.png')
    dpg.add_static_texture(width=width, height=height, default_value=data, tag=image_name, parent='static_texture_container')
    global loaded_texture
    loaded_texture.insert(0, image_name)


def _callback_update_filter(sender, app_data, user_data):
    global patient_gender_combo, patient_ethnicity_combo

    gender = dpg.get_value(patient_gender_combo)
    ethnicity = dpg.get_value(patient_ethnicity_combo)

    global patient_model_window, student_model_window, trainer_model_window
    global patient_model_detail_window, student_model_detail_window, trainer_model_detail_window

    target_window = patient_model_window
    target_detail_window = patient_model_detail_window
    if user_data == 'MedicalStudent':
        target_window = student_model_window
        gender = dpg.get_value(student_gender_combo)
        ethnicity = dpg.get_value(student_ethnicity_combo)
    elif user_data == 'Trainer':
        target_window = trainer_model_window
        gender = dpg.get_value(trainer_gender_combo)
        ethnicity = dpg.get_value(trainer_ethnicity_combo)

    conditions = dict()

    conditions['CharacterType'] = 'k' + user_data
    if not gender == 'None':
        conditions['GenderType'] = 'k' + gender
    if not ethnicity == 'None':
        conditions['EthnicityType'] = 'k' + ethnicity

    # print(conditions)
    patients_data = _get_characters_of_type(conditions)

    dpg.delete_item(target_window, children_only=True)
    dpg.delete_item(target_detail_window, children_only=True)

    global loaded_texture
    with dpg.group(horizontal=True, indent=20, parent=target_window):
        for patient in patients_data:
            print(patient.uid)
            if patient.uid not in loaded_texture:
                # print('texture not loaded')
                _load_character_model_image(patient.uid)
            dpg.add_image_button(patient.uid, callback=_update_model_config, tag='uid_' + patient.uid, user_data=user_data, background_color=[0])
            # dpg.add_text(patient.uid, parent=target_window)

def _load_character_config_for_current_scenario():
    file_path = "character_config/test_app_config.json"
    global app_config
    with open(file_path, "r", encoding="UTF-8") as app_config_file:
        row_data = app_config_file.read()
        row_config = json.loads(row_data)
        app_config = hrsa_config.HRSAConfig(**row_config)
    print(app_config.toJson())


def _update_character_config_for_current_scenario():
    file_path = "character_config/test_app_config.json"
    global app_config
    if app_config is None:
        return
    app_config_json = json.dumps(app_config.toJson(), indent=4)
    with open(file_path, "w", encoding="UTF-8") as outfile:
        outfile.write(app_config_json)

def init_ui():
    _load_character_config()

    dpg.add_texture_registry(label="Demo Texture Container", tag="static_texture_container")

    # with dpg.handler_registry():
    #     dpg.add_mouse_move_handler(callback=_log)
    #     dpg.add_mouse_click_handler(callback=_mouse_click_callback)

    with dpg.collapsing_header(label="Character Config", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        # TODO: UI Creation

        dpg.add_button(label="Load Setting", callback=_load_character_config_for_current_scenario)
        dpg.add_button(label="Save Setting", callback=_update_character_config_for_current_scenario)

        dpg.add_text('Patient', indent=20)
        with dpg.group(horizontal=True, indent=20):
            global patient_gender_combo, patient_ethnicity_combo
            patient_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200, user_data='Patient')
            patient_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200,
                                                    user_data='Patient')

        global patient_model_window, patient_model_detail_window
        with dpg.group(horizontal=True):
            patient_model_window = dpg.add_child_window(width=500, height=225)
            patient_model_detail_window = dpg.add_child_window(width=225, height=225)

        dpg.add_text('Medical Student', indent=20)
        with dpg.group(horizontal=True, indent=20):
            global student_gender_combo, student_ethnicity_combo
            student_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200,
                                                 user_data='MedicalStudent')
            student_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200,
                                                    user_data='MedicalStudent')

        global student_model_window, student_model_detail_window
        with dpg.group(horizontal=True):
            student_model_window = dpg.add_child_window(width=500, height=225)
            student_model_detail_window = dpg.add_child_window(width=225, height=225)

        dpg.add_text('Trainer', indent=20)
        with dpg.group(horizontal=True, indent=20):
            global trainer_gender_combo, trainer_ethnicity_combo
            trainer_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200, user_data='Trainer')
            trainer_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200,
                                                    user_data='Trainer')

        global trainer_model_window, trainer_model_detail_window
        with dpg.group(horizontal=True):
            trainer_model_window = dpg.add_child_window(width=500, height=225)
            trainer_model_detail_window = dpg.add_child_window(width=225, height=225)

        _callback_update_filter(None, None, 'Patient')
        _callback_update_filter(None, None, 'MedicalStudent')
        _callback_update_filter(None, None, 'Trainer')
