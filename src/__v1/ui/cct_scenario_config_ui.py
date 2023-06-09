import json
import os
import pathlib
import sys

import dearpygui.dearpygui as dpg

from __v1 import hrsa_cct_constants, hrsa_cct_globals, hrsa_cct_config, cct_ui_panels, character_model_data, cct_advanced_options_ui
from __v1.hrsa_cct_globals import hfs, log
from hrsa_data.scenario_data.scenario_config.conversation_config import ConversationConfig
from hrsa_data.scenario_data.scenario_config.scenario_config import ScenarioConfig

model_data_list = []

patient_model_info_window = None

loaded_texture = []

scenario_config: ScenarioConfig = ScenarioConfig()

CCT_CHARACTER_CONFIG_COLLAPSING_HEADER: str = 'CCT_CHARACTER_CONFIG_COLLAPSING_HEADER'
CCT_DIALOGUE_UI_CONFIG_COLLAPSING_HEADER: str = 'CCT_DIALOGUE_UI_CONFIG_COLLAPSING_HEADER'
SCU_OPEN_FILE_DIALOG: str = 'SCU_OPEN_FILE_DIALOG'
CCT_SCENARIO_CONFIG_SAVE_SETTINGS_BUTTON: str = 'CCT_SCENARIO_CONFIG_SAVE_SETTINGS_BUTTON'

PATIENT_LABEL: str = 'Patient'
TRAINER_LABEL: str = 'Trainer'
PLAYER_LABEL: str = 'Player'
MEDICAL_STUDENT_LABEL: str = 'MedicalStudent'

GENDER_LABEL: str = 'Gender'
ETHNICITY_LABEL: str = 'Ethnicity'

DEFAULT_PLAYER_SUBTITLE_TEXT_COLOR: str = "#000000"
DEFAULT_MEDICAL_STUDENT_SUBTITLE_TEXT_COLOR: str = "#FF0000"
DEFAULT_TRAINER_SUBTITLE_TEXT_COLOR: str = "#00ABFF"
DEFAULT_PATIENT_SUBTITLE_TEXT_COLOR: str = "#0CA600"

NO_AVAILABLE_CHARACTER: str = "No available Character."

scenario_config_json_file_path = ""
scu_scenario_path = ""

# region Dialog UI Config Global Variables

DUC_UNLIMITED_QUESTION_TIMER_MARK: str = 'duc_unlimited_question_timer_mark'
DUC_QUESTION_TIMER_INPUT_TEXT: str = 'duc_question_timer_input_text'

MINIMUM_QUESTION_TIMER_VALUE = 30
DEFAULT_QUESTION_TIMER_VALUE = 60


# endregion Dialog UI Config Global Variables


# target: Player: key: Gender
def get_combo_tag(target: str, key: str):
    return 'SCU_{0}_{1}_COMBO'.format(target.upper(), key.upper())


def get_model_window_tag(target: str):
    return 'SCU_{}_MODEL_WINDOW'.format(target.upper())


def get_model_detail_window_tag(target: str):
    return 'SCU_{}_MODEL_DETAIL_WINDOW'.format(target.upper())


def get_model_detail_image_tag(target: str, uid):
    return 'SCU_{0}_MODEL_DETAIL_IMAGE_{1}'.format(target.upper(), uid)


def get_selected_model_property_tag(target: str, key: str):
    return 'SCU_SELECTED_{0}_MODEL_INFO_{1}'.format(target.upper(), key.upper())


# region Dialog UI Config

def set_scenario_path(scenario_path):
    global scu_scenario_path, scenario_config_json_file_path
    dic_scenario_path = scenario_path
    scenario_config_json_file_path = os.path.join(dic_scenario_path, hrsa_cct_globals.default_language_code,
                                                  hrsa_cct_constants.SCENARIO_CONFIG_JSON_FILE_NAME)
    dpg.configure_item(cct_advanced_options_ui.SCU_SCENARIO_CONFIG_JSON_PATH_TEXT, default_value=scenario_config_json_file_path)
    _load_character_config_for_current_scenario(None, app_data=dict(file_path_name=scenario_config_json_file_path),
                                                user_data=None)
    _show_scenario_config_ui_sections()


# region helper functions start
def _hex_to_rgb(hex_color):
    value = hex_color.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


# region helper functions end


def _get_character_by_uid(uid):
    for data in model_data_list:
        if data.uid == uid:
            return data
    return None


def _get_characters_of_type(conditions):
    print(conditions)
    data_of_type = []
    global model_data_list

    for data in model_data_list:
        matched = True
        for key in conditions:
            if key not in dir(data.metaData):
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
    character_model_data_file_path = hfs.get_character_model_data_file_path()
    # with open('character_config/CharacterModelData.json', 'r', encoding='UTF-8') as character_config_file:
    with open(character_model_data_file_path, 'r', encoding='UTF-8') as character_config_file:
        row_data = character_config_file.read()
        row_config = json.loads(row_data)
        file_version = row_config['version']
        for data in row_config['ModelDataList']:
            item = character_model_data.CharacterModelData(**data)
            model_data_list.append(item)


def _update_model_config(sender, app_data, user_data):
    uid = sender.replace('uid_', '')

    global loaded_texture
    detail_texture = uid + '_0'
    detail_texture = _load_character_model_image(detail_texture)

    global scenario_config
    if user_data == PATIENT_LABEL:
        scenario_config.patient_config.character_model_config.uid = uid
    elif user_data == MEDICAL_STUDENT_LABEL:
        scenario_config.medicalstudent_config.character_model_config.uid = uid
    elif user_data == TRAINER_LABEL:
        scenario_config.trainer_config.character_model_config.uid = uid

    model_detail_window_tag = get_model_detail_window_tag(user_data)
    dpg.delete_item(model_detail_window_tag, children_only=True)
    dpg.add_image(detail_texture, tag=get_model_detail_image_tag(user_data, uid), parent=model_detail_window_tag)
    _update_selected_model_info(user_data, uid)


def _update_selected_model_info(category, uid):
    model_info = _get_character_by_uid(uid)
    if model_info is not None:
        name_tag = get_selected_model_property_tag(category, 'Name')
        gender_tag = get_selected_model_property_tag(category, GENDER_LABEL)
        ethnicity_tag = get_selected_model_property_tag(category, ETHNICITY_LABEL)
        dpg.set_value(name_tag, 'Name: ' + model_info.uid)
        dpg.set_value(gender_tag, 'Gender: ' + model_info.metaData.GenderType)
        dpg.set_value(ethnicity_tag, 'Ethnicity: ' + model_info.metaData.get_ethnicity_name())


def _load_character_model_image(image_name):
    global loaded_texture

    if image_name in loaded_texture:
        return image_name
    avatars_folder_path = hrsa_cct_globals.hfs.get_default_data_images_avatars_folder_path()
    avatar_image_path_to_load = os.path.join(avatars_folder_path, image_name + '.png')
    image_data = dpg.load_image(avatar_image_path_to_load)

    if image_data is None:
        if "default_avatar" not in loaded_texture:
            error_image_file_name = hrsa_cct_globals.hfsc.DEFAULT_ERROR_AVATAR_IMAGE_FILE_NAME
            error_image_path_to_load = hrsa_cct_globals.hfs.get_default_assets_images_avatars_file_path(
                error_image_file_name)
            image_data = dpg.load_image(error_image_path_to_load)
        else:
            return 'default_avatar'
        image_name = 'default_avatar'

    width, height, channels, data = image_data
    dpg.add_static_texture(width=width, height=height, default_value=data, tag=image_name,
                           parent='static_texture_container')

    loaded_texture.insert(0, image_name)
    return image_name


def _callback_update_filter(sender, app_data, user_data):
    gender = dpg.get_value(get_combo_tag(user_data, GENDER_LABEL))
    if gender.find(' ') != -1:
        gender = gender[:gender.find(' ')]
    ethnicity = dpg.get_value(get_combo_tag(user_data, ETHNICITY_LABEL))
    if ethnicity.find(' ') != -1:
        ethnicity = ethnicity[:ethnicity.find(' ')]

    target_window = get_model_window_tag(user_data)

    conditions = dict()

    conditions['CharacterType'] = 'k' + user_data
    if not gender == 'None':
        conditions['GenderType'] = 'k' + gender
    if not ethnicity == 'None':
        conditions['EthnicityType'] = 'k' + ethnicity

    patients_data = _get_characters_of_type(conditions)

    dpg.delete_item(target_window, children_only=True)

    global loaded_texture
    with dpg.group(horizontal=True, indent=20, parent=target_window):
        for patient in patients_data:
            image_id = _load_character_model_image(patient.uid)
            dpg.add_image_button(image_id, callback=_update_model_config, tag='uid_' + patient.uid,
                                 user_data=user_data, background_color=[0])
        if len(patients_data) == 0:
            dpg.add_text(NO_AVAILABLE_CHARACTER)


def _show_scenario_config_ui_sections():
    dpg.configure_item(CCT_CHARACTER_CONFIG_COLLAPSING_HEADER, show=True)
    dpg.configure_item(CCT_DIALOGUE_UI_CONFIG_COLLAPSING_HEADER, show=True)
    dpg.configure_item(CCT_SCENARIO_CONFIG_SAVE_SETTINGS_BUTTON, show=True)


def _load_character_config_for_current_scenario(sender, app_data, user_data):
    global scenario_config, scenario_config_json_file_path
    scenario_config_json_file_path = app_data["file_path_name"]

    if not scenario_config_json_file_path:
        log.debug("Scenario Config json file path is empty!")
        return

    file_name_with_extension = pathlib.Path(scenario_config_json_file_path).name
    if file_name_with_extension != hrsa_cct_constants.SCENARIO_CONFIG_JSON_FILE_NAME:
        log.error("Scenario Config json file name is invalid! Choose " + hrsa_cct_constants.SCENARIO_CONFIG_JSON_FILE_NAME + " file.")
        return

    scenario_config = ScenarioConfig.load_from_json_file(scenario_config_json_file_path)

    _update_model_config(scenario_config.patient_config.character_model_config.uid, None, PATIENT_LABEL)
    _update_model_config(scenario_config.trainer_config.character_model_config.uid, None, TRAINER_LABEL)
    _update_model_config(scenario_config.medicalstudent_config.character_model_config.uid, None, MEDICAL_STUDENT_LABEL)
    _init_question_timer(scenario_config.conversation_config)
    _init_dialog_color(scenario_config)

    _show_scenario_config_ui_sections()

    dpg.configure_item(cct_advanced_options_ui.SCU_SCENARIO_CONFIG_JSON_PATH_TEXT, default_value=scenario_config_json_file_path)


def _update_current_scenario_config_file():
    global scenario_config_json_file_path
    global scenario_config

    if not scenario_config_json_file_path:
        log.debug("Scenario Config json file path is empty!")
        return
    ScenarioConfig.save_to_json_file(scenario_config, scenario_config_json_file_path)
    log.clear_log()
    log.success("Scenario Configuration Saved Successfully.")


def _clear_filter(sender, app_data, user_data):
    dpg.set_value(get_combo_tag(user_data, GENDER_LABEL), 'None')
    dpg.set_value(get_combo_tag(user_data, ETHNICITY_LABEL), 'None')
    _callback_update_filter(sender, app_data, user_data)


# region Dialogue UI Config callbacks start
def _callback_update_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)]
    rgb_color = tuple(rgb_color[:3])
    # hex_color = ('#%02x%02x%02x%02x' % rgb_color).upper()
    hex_color = ('#%02x%02x%02x' % rgb_color).upper()
    global scenario_config
    if user_data == PLAYER_LABEL:
        scenario_config.player_config.ui_config.subtitle_config.text_color = hex_color
    elif user_data == MEDICAL_STUDENT_LABEL:
        scenario_config.medicalstudent_config.ui_config.subtitle_config.text_color = hex_color
    elif user_data == TRAINER_LABEL:
        scenario_config.trainer_config.ui_config.subtitle_config.text_color = hex_color
    elif user_data == PATIENT_LABEL:
        scenario_config.patient_config.ui_config.subtitle_config.text_color = hex_color


def _init_question_timer(conversation_config: ConversationConfig):
    if conversation_config.question_timer_in_seconds == 0:
        dpg.hide_item(DUC_QUESTION_TIMER_INPUT_TEXT)
        dpg.set_value(DUC_UNLIMITED_QUESTION_TIMER_MARK, True)
    else:
        dpg.show_item(DUC_QUESTION_TIMER_INPUT_TEXT)
        dpg.set_value(DUC_QUESTION_TIMER_INPUT_TEXT, conversation_config.question_timer_in_seconds)
        dpg.set_value(DUC_UNLIMITED_QUESTION_TIMER_MARK, False)


def _init_dialog_color(in_scenario_config: ScenarioConfig):
    dpg.set_value("DUC_PLAYER_SUBTITLE_TEXT_COLOR",
                  _hex_to_rgb(in_scenario_config.player_config.ui_config.subtitle_config.text_color))
    dpg.set_value("DUC_MEDICAL_STUDENT_SUBTITLE_TEXT_COLOR",
                  _hex_to_rgb(in_scenario_config.medicalstudent_config.ui_config.subtitle_config.text_color))
    dpg.set_value("DUC_PATIENT_SUBTITLE_TEXT_COLOR",
                  _hex_to_rgb(in_scenario_config.patient_config.ui_config.subtitle_config.text_color))
    dpg.set_value("DUC_TRAINER_SUBTITLE_TEXT_COLOR",
                  _hex_to_rgb(in_scenario_config.trainer_config.ui_config.subtitle_config.text_color))


def _set_question_timer(sender, app_data, user_data):
    global scenario_config

    if sender == DUC_UNLIMITED_QUESTION_TIMER_MARK:
        if app_data:
            dpg.hide_item(DUC_QUESTION_TIMER_INPUT_TEXT)
            scenario_config.conversation_config.question_timer_in_seconds = 0
        else:
            dpg.show_item(DUC_QUESTION_TIMER_INPUT_TEXT)
            value = max(MINIMUM_QUESTION_TIMER_VALUE, int(dpg.get_value(DUC_QUESTION_TIMER_INPUT_TEXT)))
            scenario_config.conversation_config.question_timer_in_seconds = value
    else:
        value = MINIMUM_QUESTION_TIMER_VALUE
        if dpg.get_value(DUC_QUESTION_TIMER_INPUT_TEXT):
            value = max(MINIMUM_QUESTION_TIMER_VALUE, int(dpg.get_value(DUC_QUESTION_TIMER_INPUT_TEXT)))
        dpg.set_value(DUC_QUESTION_TIMER_INPUT_TEXT, value)
        scenario_config.conversation_config.question_timer_in_seconds = value


def _callback_reset_subtitle_text_color(sender, app_data, user_data):
    label = user_data['label']
    if label == PLAYER_LABEL:
        dpg.set_value("DUC_PLAYER_SUBTITLE_TEXT_COLOR", _hex_to_rgb(DEFAULT_PLAYER_SUBTITLE_TEXT_COLOR))
        scenario_config.player_config.ui_config.subtitle_config.text_color = DEFAULT_PLAYER_SUBTITLE_TEXT_COLOR
    elif label == MEDICAL_STUDENT_LABEL:
        dpg.set_value("DUC_MEDICAL_STUDENT_SUBTITLE_TEXT_COLOR", _hex_to_rgb(DEFAULT_MEDICAL_STUDENT_SUBTITLE_TEXT_COLOR))
        scenario_config.medicalstudent_config.ui_config.subtitle_config.text_color = DEFAULT_MEDICAL_STUDENT_SUBTITLE_TEXT_COLOR
    elif label == TRAINER_LABEL:
        dpg.set_value("DUC_TRAINER_SUBTITLE_TEXT_COLOR", _hex_to_rgb(DEFAULT_TRAINER_SUBTITLE_TEXT_COLOR))
        scenario_config.trainer_config.ui_config.subtitle_config.text_color = DEFAULT_TRAINER_SUBTITLE_TEXT_COLOR
    elif label == PATIENT_LABEL:
        dpg.set_value("DUC_PATIENT_SUBTITLE_TEXT_COLOR", _hex_to_rgb(DEFAULT_PATIENT_SUBTITLE_TEXT_COLOR))
        scenario_config.patient_config.ui_config.subtitle_config.text_color = DEFAULT_PATIENT_SUBTITLE_TEXT_COLOR


# region Dialogue UI Config callbacks end

def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


def _help(message):
    last_item = dpg.last_item()
    group = dpg.add_group(horizontal=True)
    dpg.move_item(last_item, parent=group)
    dpg.capture_next_item(lambda s: dpg.move_item(s, parent=group))
    t = dpg.add_text("(?)", color=[0, 255, 0])
    with dpg.tooltip(t):
        dpg.add_text(message)


def init_ui():
    global patient_model_info_window

    _load_character_config()

    dpg.add_texture_registry(label="Demo Texture Container", tag="static_texture_container")
    with dpg.collapsing_header(tag=cct_ui_panels.CCT_SCENARIO_CONFIG_COLLAPSING_HEADER,
                               label="Character Selection / Subtitle Color / Question Timer - (Scenario Configuration)",
                               default_open=False, open_on_double_click=False, open_on_arrow=False):
        dpg.add_text(tag=cct_advanced_options_ui.SCU_SCENARIO_CONFIG_JSON_PATH_TEXT)
        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_load_character_config_for_current_scenario, tag=SCU_OPEN_FILE_DIALOG,
                             modal=True, default_path=hrsa_cct_config.get_file_dialog_default_path(),
                             cancel_callback=file_dialog_cancel_callback):
            dpg.add_file_extension(".json", color=(255, 255, 0, 255))
        with dpg.group(horizontal=True):
            dpg.add_button(label="Select Scenario Config JSON File...", tag=cct_advanced_options_ui.SCU_OPEN_FILE_DIALOG_BUTTON,
                           callback=lambda: dpg.show_item(SCU_OPEN_FILE_DIALOG))
        # region Character Config
        with dpg.collapsing_header(indent=25, tag=CCT_CHARACTER_CONFIG_COLLAPSING_HEADER,
                                   label="Character Configuration", default_open=False,
                                   show=False):
            # region Patient Config
            dpg.add_text(PATIENT_LABEL, indent=20)
            available_gender = ['None']
            available_ethnicity = ['None']
            for gender in ['Male', 'Female']:
                available_model = _get_characters_of_type({'CharacterType': 'kPatient', 'GenderType': 'k' + gender})
                if len(available_model) > 0:
                    available_gender.append('{0} ({1})'.format(gender, len(available_model)))
            for ethnicity in ['White', 'Black', 'Hispanic']:
                available_model = _get_characters_of_type({'CharacterType': 'kPatient', 'EthnicityType': 'k' + ethnicity})
                if len(available_model) > 0:
                    available_ethnicity.append('{0} ({1})'.format(ethnicity, len(available_model)))
            with dpg.group(horizontal=True, indent=20):
                dpg.add_text(GENDER_LABEL + ': ')
                dpg.add_combo(available_gender, label='', default_value='None',
                              tag=get_combo_tag(PATIENT_LABEL, GENDER_LABEL), callback=_callback_update_filter, width=200,
                              user_data=PATIENT_LABEL)
                dpg.add_text(ETHNICITY_LABEL + ': ')
                dpg.add_combo(available_ethnicity, label='',
                              default_value='None', tag=get_combo_tag(PATIENT_LABEL, ETHNICITY_LABEL),
                              callback=_callback_update_filter, width=200,
                              user_data=PATIENT_LABEL)
                dpg.add_button(label='Clear Filter', callback=_clear_filter, user_data=PATIENT_LABEL)
            with dpg.group(horizontal=True):
                dpg.add_text('Available Characters:')
                dpg.add_text('Current Selection:', indent=500)
            with dpg.group(horizontal=True):
                dpg.add_child_window(width=500, height=225, tag=get_model_window_tag(PATIENT_LABEL))
                dpg.add_child_window(width=225, height=225, tag=get_model_detail_window_tag(PATIENT_LABEL))
                patient_model_info_window = dpg.add_child_window(width=225, height=225)

            dpg.add_text('Name', parent=patient_model_info_window,
                         tag=get_selected_model_property_tag(PATIENT_LABEL, 'Name'))
            dpg.add_text(GENDER_LABEL, parent=patient_model_info_window,
                         tag=get_selected_model_property_tag(PATIENT_LABEL, GENDER_LABEL))
            dpg.add_text(ETHNICITY_LABEL, parent=patient_model_info_window,
                         tag=get_selected_model_property_tag(PATIENT_LABEL, ETHNICITY_LABEL))
            # endregion Patient Config

            # region Medical Student Config
            dpg.add_text('Medical Student', indent=20)
            available_gender = ['None']
            available_ethnicity = ['None']
            for gender in ['Male', 'Female']:
                available_model = _get_characters_of_type({'CharacterType': 'kMedicalStudent', 'GenderType': 'k' + gender})
                if len(available_model) > 0:
                    available_gender.append('{0} ({1})'.format(gender, len(available_model)))
            for ethnicity in ['White', 'Black', 'Hispanic']:
                available_model = _get_characters_of_type({'CharacterType': 'kMedicalStudent', 'EthnicityType': 'k' + ethnicity})
                if len(available_model) > 0:
                    available_ethnicity.append('{0} ({1})'.format(ethnicity, len(available_model)))
            with dpg.group(horizontal=True, indent=20):
                dpg.add_text(GENDER_LABEL + ': ')
                dpg.add_combo(available_gender, label='', default_value='None',
                              tag=get_combo_tag(MEDICAL_STUDENT_LABEL, GENDER_LABEL),
                              callback=_callback_update_filter, width=200,
                              user_data=MEDICAL_STUDENT_LABEL)
                dpg.add_text(ETHNICITY_LABEL + ': ')
                dpg.add_combo(available_ethnicity, label='',
                              default_value='None', tag=get_combo_tag(MEDICAL_STUDENT_LABEL, ETHNICITY_LABEL),
                              callback=_callback_update_filter, width=200,
                              user_data=MEDICAL_STUDENT_LABEL)
                dpg.add_button(label='Clear Filter', callback=_clear_filter, user_data=MEDICAL_STUDENT_LABEL)
            with dpg.group(horizontal=True):
                dpg.add_text('Available Characters:')
                dpg.add_text('Current Selection:', indent=500)
            with dpg.group(horizontal=True):
                dpg.add_child_window(width=500, height=225, tag=get_model_window_tag(MEDICAL_STUDENT_LABEL))
                dpg.add_child_window(width=225, height=225, tag=get_model_detail_window_tag(MEDICAL_STUDENT_LABEL))
                student_model_info_window = dpg.add_child_window(width=225, height=225)

            dpg.add_text('Name', parent=student_model_info_window,
                         tag=get_selected_model_property_tag(MEDICAL_STUDENT_LABEL, 'Name'))
            dpg.add_text(GENDER_LABEL, parent=student_model_info_window,
                         tag=get_selected_model_property_tag(MEDICAL_STUDENT_LABEL, GENDER_LABEL))
            dpg.add_text(ETHNICITY_LABEL, parent=student_model_info_window,
                         tag=get_selected_model_property_tag(MEDICAL_STUDENT_LABEL, ETHNICITY_LABEL))
            # endregion Medical Student Config

            # region Trainer Config
            dpg.add_text(TRAINER_LABEL, indent=20)
            available_gender = ['None']
            available_ethnicity = ['None']
            for gender in ['Male', 'Female']:
                available_model = _get_characters_of_type({'CharacterType': 'kTrainer', 'GenderType': 'k' + gender})
                if len(available_model) > 0:
                    available_gender.append('{0} ({1})'.format(gender, len(available_model)))
            for ethnicity in ['White', 'Black', 'Hispanic']:
                available_model = _get_characters_of_type({'CharacterType': 'kTrainer', 'EthnicityType': 'k' + ethnicity})
                if len(available_model) > 0:
                    available_ethnicity.append('{0} ({1})'.format(ethnicity, len(available_model)))
            with dpg.group(horizontal=True, indent=20):
                dpg.add_text(GENDER_LABEL + ': ')
                dpg.add_combo(available_gender, label='', default_value='None',
                              tag=get_combo_tag(TRAINER_LABEL, GENDER_LABEL),
                              callback=_callback_update_filter, width=200, user_data=TRAINER_LABEL)
                dpg.add_text(ETHNICITY_LABEL + ': ')
                dpg.add_combo(available_ethnicity, label='',
                              default_value='None', tag=get_combo_tag(TRAINER_LABEL, ETHNICITY_LABEL),
                              callback=_callback_update_filter, width=200,
                              user_data=TRAINER_LABEL)
                dpg.add_button(label='Clear Filter', callback=_clear_filter, user_data=TRAINER_LABEL)
            with dpg.group(horizontal=True):
                dpg.add_text('Available Characters:')
                dpg.add_text('Current Selection:', indent=500)
            with dpg.group(horizontal=True):
                dpg.add_child_window(width=500, height=225, tag=get_model_window_tag(TRAINER_LABEL))
                dpg.add_child_window(width=225, height=225, tag=get_model_detail_window_tag(TRAINER_LABEL))
                trainer_model_info_window = dpg.add_child_window(width=225, height=225)

            dpg.add_text('Name', parent=trainer_model_info_window,
                         tag=get_selected_model_property_tag(TRAINER_LABEL, 'Name'))
            dpg.add_text(GENDER_LABEL, parent=trainer_model_info_window,
                         tag=get_selected_model_property_tag(TRAINER_LABEL, GENDER_LABEL))
            dpg.add_text(ETHNICITY_LABEL, parent=trainer_model_info_window,
                         tag=get_selected_model_property_tag(TRAINER_LABEL, ETHNICITY_LABEL))
            # endregion Trainer Config

            _callback_update_filter(None, None, PATIENT_LABEL)
            _callback_update_filter(None, None, MEDICAL_STUDENT_LABEL)
            _callback_update_filter(None, None, TRAINER_LABEL)
        # endregion Character Config

        # region Dialogue UI Config
        with dpg.collapsing_header(indent=25, tag=CCT_DIALOGUE_UI_CONFIG_COLLAPSING_HEADER,
                                   label="Dialogue UI Configuration", default_open=False,
                                   show=False):
            with dpg.group(horizontal=True):
                dpg.add_text("Player Subtitle Text Color")
                dpg.add_button(label="Reset",
                               user_data={'label': PLAYER_LABEL},
                               callback=_callback_reset_subtitle_text_color)
            dpg.add_color_edit(label="",
                               tag="DUC_PLAYER_SUBTITLE_TEXT_COLOR",
                               callback=_callback_update_subtitle_text_color,
                               user_data=PLAYER_LABEL,
                               input_mode=dpg.mvColorEdit_input_rgb,
                               indent=20)

            with dpg.group(horizontal=True):
                dpg.add_text("Medical Student Subtitle Text Color")
                dpg.add_button(label="Reset",
                               user_data={'label': MEDICAL_STUDENT_LABEL},
                               callback=_callback_reset_subtitle_text_color)
            dpg.add_color_edit(label="",
                               tag="DUC_MEDICAL_STUDENT_SUBTITLE_TEXT_COLOR",
                               callback=_callback_update_subtitle_text_color,
                               user_data=MEDICAL_STUDENT_LABEL,
                               input_mode=dpg.mvColorEdit_input_rgb,
                               indent=20)

            with dpg.group(horizontal=True):
                dpg.add_text("Patient Subtitle Text Color")
                dpg.add_button(label="Reset",
                               user_data={'label': PATIENT_LABEL},
                               callback=_callback_reset_subtitle_text_color)
            dpg.add_color_edit(label="",
                               tag="DUC_PATIENT_SUBTITLE_TEXT_COLOR",
                               callback=_callback_update_subtitle_text_color,
                               user_data=PATIENT_LABEL,
                               input_mode=dpg.mvColorEdit_input_rgb,
                               indent=20)

            with dpg.group(horizontal=True):
                dpg.add_text("Trainer Subtitle Text Color")
                dpg.add_button(label="Reset",
                               user_data={'label': TRAINER_LABEL},
                               callback=_callback_reset_subtitle_text_color)
            dpg.add_color_edit(label="",
                               tag="DUC_TRAINER_SUBTITLE_TEXT_COLOR",
                               callback=_callback_update_subtitle_text_color,
                               user_data=TRAINER_LABEL,
                               input_mode=dpg.mvColorEdit_input_rgb,
                               indent=20)

            dpg.add_text("Question Timer")
            with dpg.group(horizontal=True):
                dpg.add_checkbox(label="Unlimited Timer", source="bool_value", tag=DUC_UNLIMITED_QUESTION_TIMER_MARK,
                                 callback=_set_question_timer)
                dpg.add_input_text(label="Question Timer in Seconds", width=100, decimal=True, default_value=str(DEFAULT_QUESTION_TIMER_VALUE),
                                   tag=DUC_QUESTION_TIMER_INPUT_TEXT,
                                   callback=_set_question_timer)
                _help("If this value is below 30 seconds, the timer will be set to 30 seconds.")

            # endregion Dialogue UI Config

        dpg.add_button(tag=CCT_SCENARIO_CONFIG_SAVE_SETTINGS_BUTTON, label="Save Scenario Configuration",
                       show=False, callback=_update_current_scenario_config_file)

        dpg.add_separator()


if sys.flags.dev_mode:
    print("cct_scenario_config_ui.__init__()")
