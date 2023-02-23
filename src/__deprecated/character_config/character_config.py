import json
import os

import dearpygui.dearpygui as dpg
from adbutils import adb

from __deprecated import hrsa_cct_constants, hrsa_cct_globals
from __deprecated.configuration import hrsa_config, character_model_data

model_data_list = []

patient_gender_combo = None
patient_ethnicity_combo = None

student_gender_combo = None
student_ethnicity_combo = None

trainer_gender_combo = None
trainer_ethnicity_combo = None

patient_model_window = None
patient_model_detail_window = None
patient_model_info_window = None

student_model_window = None
student_model_detail_window = None

trainer_model_window = None
trainer_model_detail_window = None

loaded_texture = []

app_config = None

selected_patient_model_info_name = None
selected_patient_model_info_gender = None
selected_patient_model_info_ethnicity = None

selected_student_model_info_name = None
selected_student_model_info_gender = None
selected_student_model_info_ethnicity = None

selected_trainer_model_info_name = None
selected_trainer_model_info_gender = None
selected_trainer_model_info_ethnicity = None

target_devices = []

SCU_SCENARIO_CONFIG_JSON_PATH_TEXT: str = 'SCU_SCENARIO_CONFIG_JSON_PATH_TEXT'
SCU_OPEN_FILE_DIALOG: str = 'SCU_OPEN_FILE_DIALOG'

# scenario_config = dict()
scenario_config_json_file_path = ""
scu_scenario_path = ""


def set_scenario_path(scenario_path):
    global scu_scenario_path, scenario_config_json_file_path
    dic_scenario_path = scenario_path
    scenario_config_json_file_path = os.path.join(dic_scenario_path, hrsa_cct_globals.default_language_code, hrsa_cct_constants.SCENARIO_CONFIG_JSON_FILE_NAME)
    dpg.configure_item(SCU_SCENARIO_CONFIG_JSON_PATH_TEXT, default_value=scenario_config_json_file_path)
    _load_character_config_for_current_scenario(None, app_data=dict(file_path_name=scenario_config_json_file_path), user_data=None)


def _get_character_by_uid(uid):
    for data in model_data_list:
        if data.uid == uid:
            return data
    return None


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
        file_version = row_config['version']
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
    detail_texture = _load_character_model_image(detail_texture)

    global patient_model_detail_window, student_model_detail_window, trainer_model_detail_window
    global app_config
    if user_data == 'Patient':
        if app_config is not None:
            app_config.patient_config.character_model_config.uid = uid
        dpg.delete_item(patient_model_detail_window, children_only=True)
        dpg.add_image(detail_texture, tag='detail_patient_' + uid, parent=patient_model_detail_window)
    elif user_data == 'MedicalStudent':
        if app_config is not None:
            app_config.medicalstudent_config.character_model_config.uid = uid
        dpg.delete_item(student_model_detail_window, children_only=True)
        dpg.add_image(detail_texture, tag='detail_student_' + uid, parent=student_model_detail_window)
    elif user_data == 'Trainer':
        if app_config is not None:
            app_config.trainer_config.character_model_config.uid = uid
        dpg.delete_item(trainer_model_detail_window, children_only=True)
        dpg.add_image(detail_texture, tag='detail_trainer_' + uid, parent=trainer_model_detail_window)

    _update_selected_model_info(user_data, uid)


def _update_selected_model_info(category, uid):
    model_info = _get_character_by_uid(uid)
    if model_info is not None:
        if category == 'Patient':
            global selected_patient_model_info_name, selected_patient_model_info_gender, selected_patient_model_info_ethnicity
            dpg.set_value(selected_patient_model_info_name, 'Name: ' + model_info.uid)
            dpg.set_value(selected_patient_model_info_gender, 'Gender: ' + model_info.metaData.GenderType)
            dpg.set_value(selected_patient_model_info_ethnicity, 'Ethnicity: ' + model_info.metaData.EthnicityType)
        elif category == 'MedicalStudent':
            global selected_student_model_info_name, selected_student_model_info_gender, selected_student_model_info_ethnicity
            dpg.set_value(selected_student_model_info_name, 'Name: ' + model_info.uid)
            dpg.set_value(selected_student_model_info_gender, 'Gender: ' + model_info.metaData.GenderType)
            dpg.set_value(selected_student_model_info_ethnicity, 'Ethnicity: ' + model_info.metaData.EthnicityType)
        elif category == 'Trainer':
            global selected_trainer_model_info_name, selected_trainer_model_info_gender, selected_trainer_model_info_ethnicity
            dpg.set_value(selected_trainer_model_info_name, 'Name: ' + model_info.uid)
            dpg.set_value(selected_trainer_model_info_gender, 'Gender: ' + model_info.metaData.GenderType)
            dpg.set_value(selected_trainer_model_info_ethnicity, 'Ethnicity: ' + model_info.metaData.EthnicityType)


def _load_character_model_image(image_name):
    global loaded_texture

    if image_name in loaded_texture:
        return image_name
    image_data = dpg.load_image('../../data/avatar/' + image_name + '.png')

    if image_data is None:
        if "default_avatar" not in loaded_texture:
            image_data = dpg.load_image('../../data/defaults/error.png')
        else:
            return 'default_avatar'
        image_name = 'default_avatar'

    width, height, channels, data = image_data
    dpg.add_static_texture(width=width, height=height, default_value=data, tag=image_name, parent='static_texture_container')

    loaded_texture.insert(0, image_name)
    return image_name


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

    print('conditions => ', conditions)
    patients_data = _get_characters_of_type(conditions)

    dpg.delete_item(target_window, children_only=True)
    dpg.delete_item(target_detail_window, children_only=True)

    global loaded_texture
    with dpg.group(horizontal=True, indent=20, parent=target_window):
        for patient in patients_data:
            print(patient.uid)
            image_id = _load_character_model_image(patient.uid)
            dpg.add_image_button(image_id, callback=_update_model_config, tag='uid_' + patient.uid,
                                 user_data=user_data, background_color=[0])
            # dpg.add_text(patient.uid, parent=target_window)


def _load_character_config_for_current_scenario(sender, app_data, user_data):
    global app_config, scenario_config_json_file_path
    scenario_config_json_file_path = app_data["file_path_name"]
    # file_path = "character_config/test_app_config.json"
    global app_config
    with open(scenario_config_json_file_path, "r", encoding="UTF-8") as app_config_file:
        row_data = app_config_file.read()
        row_config = json.loads(row_data)
        app_config = hrsa_config.HRSAConfig(**row_config)

    _update_model_config(app_config.patient_config.character_model_config.uid, None, 'Patient')
    _update_model_config(app_config.trainer_config.character_model_config.uid, None, 'Trainer')
    _update_model_config(app_config.medicalstudent_config.character_model_config.uid, None, 'MedicalStudent')


def _update_character_config_for_current_scenario():
    global scenario_config_json_file_path
    # file_path = "character_config/test_app_config.json"
    global app_config
    if app_config is None:
        print("Character config for current scenario is none!")
        return

    app_config_json = json.dumps(app_config.toJson(), indent=4)
    print(app_config_json)
    with open(scenario_config_json_file_path, "w", encoding="UTF-8") as outfile:
        outfile.write(app_config_json)


def _filter_clear(sender, app_data, user_data):
    print(sender, app_data, user_data)
    if user_data == 'Patient':
        global patient_gender_combo, patient_ethnicity_combo
        dpg.set_value(patient_gender_combo, 'None')
        dpg.set_value(patient_ethnicity_combo, 'None')
        global selected_patient_model_info_name, selected_patient_model_info_gender, selected_patient_model_info_ethnicity
        dpg.set_value(selected_patient_model_info_name, '')
        dpg.set_value(selected_patient_model_info_gender, '')
        dpg.set_value(selected_patient_model_info_ethnicity, '')
    elif user_data == 'MedicalStudent':
        global student_gender_combo, student_ethnicity_combo
        dpg.set_value(student_gender_combo, 'None')
        dpg.set_value(student_ethnicity_combo, 'None')
        global selected_student_model_info_name, selected_student_model_info_gender, selected_student_model_info_ethnicity
        dpg.set_value(selected_student_model_info_name, '')
        dpg.set_value(selected_student_model_info_gender, '')
        dpg.set_value(selected_student_model_info_ethnicity, '')
    elif user_data == 'Trainer':
        global trainer_gender_combo, trainer_ethnicity_combo
        dpg.set_value(trainer_gender_combo, 'None')
        dpg.set_value(trainer_ethnicity_combo, 'None')
        global selected_trainer_model_info_name, selected_trainer_model_info_gender, selected_trainer_model_info_ethnicity
        dpg.set_value(selected_trainer_model_info_name, '')
        dpg.set_value(selected_trainer_model_info_gender, '')
        dpg.set_value(selected_trainer_model_info_ethnicity, '')

    # _callback_update_filter(sender, app_data, user_data)
    _update_model_config('0', app_data, user_data)


def _select_target_device(sender, app_data, user_data):
    print(sender, app_data)
    global target_devices
    if user_data not in target_devices:
        target_devices.append(user_data)


def _toggle_media_transfer(sender, app_data, user_data):
    global target_devices
    if len(target_devices) <= 0:
        print("No target devices selected!")
    for info in target_devices:
        try:
            device = adb.device(serial=info.serial)
            if user_data:
                device.shell("svc usb setFunctions mtp")
                device = adb.device(serial=info.serial)  # need reconnect
                device.shell("svc usb setScreenUnlockedFunctions mtp")
            else:
                device.shell("svc usb setScreenUnlockedFunctions")
                device = adb.device(serial=info.serial)  # need reconnect
                device.shell("svc usb setFunctions")
        except RuntimeError as e:
            print(e)


def _install_package_callback(messages):
    print('Install package message ', messages)


def _install_latest_package(sender, app_data, user_data):
    global target_devices
    if len(target_devices) <= 0:
        print("No target devices selected!")
    for info in target_devices:
        device = adb.device(serial=info.serial)
        device.install('/home/uoubyy/Downloads/Netease.apk', silent=True, callback=_install_package_callback)


def _select_scenario_config_file(sender, app_data, user_data):
    dpg.configure_item(SCU_OPEN_FILE_DIALOG, show=True)


# def _callback_load_scenario_config_file(sender, app_data, user_data):
#     global app_config, scenario_config_json_file_path
#     scenario_config_json_file_path = app_data["file_path_name"]
#     dpg.configure_item(SCU_SCENARIO_CONFIG_JSON_PATH_TEXT, default_value=str(scenario_config_json_file_path))
#     if scenario_config_json_file_path is not None or scenario_config_json_file_path != '':
#         with open(scenario_config_json_file_path, "r", encoding="UTF-8") as scenario_config_json:
#             app_config = json.load(scenario_config_json)


def init_ui():
    _load_character_config()

    dpg.add_texture_registry(label="Demo Texture Container", tag="static_texture_container")

    # with dpg.handler_registry():
    #     dpg.add_mouse_move_handler(callback=_log)
    #     dpg.add_mouse_click_handler(callback=_mouse_click_callback)

    with dpg.collapsing_header(label="Character Config", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        # TODO: UI Creation
        dpg.add_text(tag=SCU_SCENARIO_CONFIG_JSON_PATH_TEXT)
        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_load_character_config_for_current_scenario, tag=SCU_OPEN_FILE_DIALOG, modal=True):
            dpg.add_file_extension(".json", color=(255, 255, 0, 255))

        with dpg.group(horizontal=True):
            dpg.add_button(label="Select Scenario Config JSON File...", callback=_select_scenario_config_file)

        dpg.add_button(label="Load Setting", show=False, callback=_load_character_config_for_current_scenario)

        dpg.add_text('Patient', indent=20)
        with dpg.group(horizontal=True, indent=20):
            global patient_gender_combo, patient_ethnicity_combo
            patient_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200, user_data='Patient')
            patient_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200,
                                                    user_data='Patient')
            dpg.add_button(label='Reset', callback=_filter_clear, user_data='Patient')

        global patient_model_window, patient_model_detail_window, patient_model_info_window
        with dpg.group(horizontal=True):
            patient_model_window = dpg.add_child_window(width=500, height=225)
            patient_model_detail_window = dpg.add_child_window(width=225, height=225)
            patient_model_info_window = dpg.add_child_window(width=225, height=225)

        global selected_patient_model_info_name, selected_patient_model_info_gender, selected_patient_model_info_ethnicity
        selected_patient_model_info_name = dpg.add_text('Name', parent=patient_model_info_window)
        selected_patient_model_info_gender = dpg.add_text('Gender', parent=patient_model_info_window)
        selected_patient_model_info_ethnicity = dpg.add_text('Ethnicity', parent=patient_model_info_window)

        dpg.add_text('Medical Student', indent=20)
        with dpg.group(horizontal=True, indent=20):
            global student_gender_combo, student_ethnicity_combo
            student_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200,
                                                 user_data='MedicalStudent')
            student_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200,
                                                    user_data='MedicalStudent')
            dpg.add_button(label='Reset', callback=_filter_clear, user_data='MedicalStudent')

        global student_model_window, student_model_detail_window
        with dpg.group(horizontal=True):
            student_model_window = dpg.add_child_window(width=500, height=225)
            student_model_detail_window = dpg.add_child_window(width=225, height=225)
            student_model_info_window = dpg.add_child_window(width=225, height=225)

        global selected_student_model_info_name, selected_student_model_info_gender, selected_student_model_info_ethnicity
        selected_student_model_info_name = dpg.add_text('Name', parent=student_model_info_window)
        selected_student_model_info_gender = dpg.add_text('Gender', parent=student_model_info_window)
        selected_student_model_info_ethnicity = dpg.add_text('Ethnicity', parent=student_model_info_window)

        dpg.add_text('Trainer', indent=20)
        with dpg.group(horizontal=True, indent=20):
            global trainer_gender_combo, trainer_ethnicity_combo
            trainer_gender_combo = dpg.add_combo(('None', 'Male', 'Female'), label='Gender', default_value='None', callback=_callback_update_filter, width=200, user_data='Trainer')
            trainer_ethnicity_combo = dpg.add_combo(('None', 'White', 'Black', 'Hispanic'), label='Ethnicity', default_value='None', callback=_callback_update_filter, width=200,
                                                    user_data='Trainer')
            dpg.add_button(label='Reset', callback=_filter_clear, user_data='Trainer')

        global trainer_model_window, trainer_model_detail_window
        with dpg.group(horizontal=True):
            trainer_model_window = dpg.add_child_window(width=500, height=225)
            trainer_model_detail_window = dpg.add_child_window(width=225, height=225)
            trainer_model_info_window = dpg.add_child_window(width=225, height=225)

        global selected_trainer_model_info_name, selected_trainer_model_info_gender, selected_trainer_model_info_ethnicity
        selected_trainer_model_info_name = dpg.add_text('Name', parent=trainer_model_info_window)
        selected_trainer_model_info_gender = dpg.add_text('Gender', parent=trainer_model_info_window)
        selected_trainer_model_info_ethnicity = dpg.add_text('Ethnicity', parent=trainer_model_info_window)

        _callback_update_filter(None, None, 'Patient')
        _callback_update_filter(None, None, 'MedicalStudent')
        _callback_update_filter(None, None, 'Trainer')

        with dpg.collapsing_header(label="Transfer to Device", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
            dpg.add_text('Devices', indent=20)
            connected_devices = adb.device_list()
            for device in connected_devices:
                print(device.serial, device.prop.model)
                dpg.add_checkbox(label=device.serial, source="bool_value", callback=_select_target_device, user_data=device.serial)
            if len(connected_devices) == 0:
                dpg.add_text('No Device Connected!', indent=40)

            dpg.add_button(label='Install Latest Package', callback=_install_latest_package, user_data=True)
            dpg.add_button(label='Enable Media Transfer', callback=_toggle_media_transfer, user_data=True)

        dpg.add_button(label="Save Setting", show=True, callback=_update_character_config_for_current_scenario)
