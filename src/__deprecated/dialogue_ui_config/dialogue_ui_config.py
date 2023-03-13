import json
import os

import dearpygui.dearpygui as dpg

from __deprecated import hrsa_cct_constants, hrsa_cct_globals
from __deprecated.configuration import hrsa_config
from hrsa_data.scenario_data.scenario_config.scenario_config import ScenarioConfig

# GUI Element Tags


# Module Variables
DUC_SCENARIO_CONFIG_JSON_PATH_TEXT: str = 'DUC_SCENARIO_CONFIG_JSON_PATH_TEXT'
DUC_OPEN_FILE_DIALOG: str = 'DUC_OPEN_FILE_DIALOG'

# scenario_config = dict()
scenario_config_json_file_path = ""
duc_scenario_path = ""

scenario_config: ScenarioConfig = ScenarioConfig()
duc_unlimited_question_timer_mark = None
duc_question_timer_input_text = None


def set_scenario_path(scenario_path):
    global duc_scenario_path, scenario_config_json_file_path
    duc_scenario_path = scenario_path
    scenario_config_json_file_path = os.path.join(duc_scenario_path, hrsa_cct_globals.default_language_code, hrsa_cct_constants.SCENARIO_CONFIG_JSON_FILE_NAME)
    dpg.configure_item(DUC_SCENARIO_CONFIG_JSON_PATH_TEXT, default_value=scenario_config_json_file_path)
    _callback_load_dialog_config_file(None, app_data=dict(file_path_name=scenario_config_json_file_path), user_data=None)


def _hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h * 6.)  # XXX assume int() truncates!
    f = (h * 6.) - i;
    p, q, t = v * (1. - s), v * (1. - s * f), v * (1. - s * (1. - f));
    i %= 6
    if i == 0: return int(255 * v), int(255 * t), int(255 * p)
    if i == 1: return int(255 * q), int(255 * v), int(255 * p)
    if i == 2: return int(255 * p), int(255 * v), int(255 * t)
    if i == 3: return int(255 * p), int(255 * q), int(255 * v)
    if i == 4: return int(255 * t), int(255 * p), int(255 * v)
    if i == 5: return int(255 * v), int(255 * p), int(255 * q)


def _rgb_to_hex(rgb_color):
    return '#%02x%02x%02x' % rgb_color


def _hex_to_rgb(hex_color):
    value = hex_color.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def _callback_update_player_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global scenario_config
    scenario_config.player_config.ui_config.subtitle_config.text_color = hex_color


def _callback_update_medicalstudent_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global scenario_config
    scenario_config.medicalstudent_config.ui_config.subtitle_config.text_color = hex_color


def _callback_update_patient_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global scenario_config
    scenario_config.patient_config.ui_config.subtitle_config.text_color = hex_color


def _callback_update_trainer_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global scenario_config
    scenario_config.trainer_config.ui_config.subtitle_config.text_color = hex_color


def _load_default_color_set(sender, app_data, user_data):
    dpg.configure_item("DUC_OPEN_FILE_DIALOG", show=True)


def _save_color_set(sender, app_data, user_data):
    global scenario_config_json_file_path
    global scenario_config
    duc_color_setting_json = json.dumps(scenario_config.toJson(), indent=4)
    with open(scenario_config_json_file_path, "w", encoding="UTF-8") as outfile:
        outfile.write(duc_color_setting_json)


def _init_question_timer(conversation_config: hrsa_config.ConversationConfig):
    global duc_unlimited_question_timer_mark, duc_question_timer_input_text
    if conversation_config.question_timer_in_seconds == 0:
        dpg.hide_item(duc_question_timer_input_text)
        dpg.set_value(duc_unlimited_question_timer_mark, True)
    else:
        dpg.show_item(duc_question_timer_input_text)
        dpg.set_value(duc_question_timer_input_text, conversation_config.question_timer_in_seconds)
        dpg.set_value(duc_unlimited_question_timer_mark, False)


def _init_dialog_color(color_setting: hrsa_config.HRSAConfig):
    dpg.set_value("DUC_PLAYER_SUBTITLE_TEXT_COLOR", _hex_to_rgb(color_setting.player_config.ui_config.subtitle_config.text_color))
    dpg.set_value("DUC_MEDICALSTUDENT_SUBTITLE_TEXT_COLOR", _hex_to_rgb(color_setting.medicalstudent_config.ui_config.subtitle_config.text_color))
    dpg.set_value("DUC_PATIENT_SUBTITLE_TEXT_COLOR", _hex_to_rgb(color_setting.patient_config.ui_config.subtitle_config.text_color))
    dpg.set_value("DUC_TRAINER_SUBTITLE_TEXT_COLOR", _hex_to_rgb(color_setting.trainer_config.ui_config.subtitle_config.text_color))


def _set_question_timer(sender, app_data, user_data):
    global scenario_config
    if scenario_config is None:
        print('Test process, should load the configuration file firstly.')

    global duc_unlimited_question_timer_mark, duc_question_timer_input_text
    if sender == duc_unlimited_question_timer_mark:
        if app_data:
            dpg.hide_item(duc_question_timer_input_text)
            scenario_config.conversation_config.question_timer_in_seconds = 0
        else:
            dpg.show_item(duc_question_timer_input_text)
    else:
        scenario_config.conversation_config.question_timer_in_seconds = dpg.get_value(duc_question_timer_input_text)


def _callback_load_dialog_config_file(sender, app_data, user_data):
    global scenario_config, scenario_config_json_file_path
    scenario_config_json_file_path = app_data["file_path_name"]
    dpg.configure_item(DUC_SCENARIO_CONFIG_JSON_PATH_TEXT, default_value=str(scenario_config_json_file_path))
    with open(scenario_config_json_file_path, "r", encoding="UTF-8") as ui_config_file:
        row_data = ui_config_file.read()
        row_config = json.loads(row_data)
        scenario_config = hrsa_config.HRSAConfig(**row_config)
        _init_question_timer(scenario_config.conversation_config)
        _init_dialog_color(scenario_config)


def _select_scenario_config_file(sender, app_data, user_data):
    dpg.configure_item(DUC_OPEN_FILE_DIALOG, show=True)


#
# def _callback_load_scenario_config_file(sender, app_data, user_data):
#     global duc_color_setting, scenario_config_json_file_path
#     scenario_config_json_file_path = app_data["file_path_name"]
#     dpg.configure_item(DUC_SCENARIO_CONFIG_JSON_PATH_TEXT, default_value=str(scenario_config_json_file_path))
#     if scenario_config_json_file_path is not None or scenario_config_json_file_path != '':
#         with open(scenario_config_json_file_path, "r", encoding="UTF-8") as scenario_config_json:
#             duc_color_setting = json.load(scenario_config_json)
#
#     _init_dialog_color(duc_color_setting)
#     _init_question_timer(duc_color_setting.conversation_config)


def init_ui():
    with dpg.collapsing_header(label="Dialogue UI Config", default_open=False, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        # TODO: UI Creation
        dpg.add_text(tag=DUC_SCENARIO_CONFIG_JSON_PATH_TEXT)
        # file selection dialog start
        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_callback_load_dialog_config_file, tag=DUC_OPEN_FILE_DIALOG, modal=True):
            dpg.add_file_extension(".json", color=(255, 255, 0, 255))
        # file selection dialog end

        with dpg.group(horizontal=True):
            dpg.add_button(label="Select Scenario Config JSON File...", callback=_select_scenario_config_file)

        dpg.add_button(label="Load Setting", show=False, callback=_load_default_color_set)

        dpg.add_color_edit(label="Player Subtitle Text Color", tag="DUC_PLAYER_SUBTITLE_TEXT_COLOR",
                           callback=_callback_update_player_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)

        dpg.add_color_edit(label="Medical Student Subtitle Text Color", tag="DUC_MEDICALSTUDENT_SUBTITLE_TEXT_COLOR",
                           callback=_callback_update_medicalstudent_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)

        dpg.add_color_edit(label="Patient Subtitle Text Color", tag="DUC_PATIENT_SUBTITLE_TEXT_COLOR",
                           callback=_callback_update_patient_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)

        dpg.add_color_edit(label="Trainer Subtitle Text Color", tag="DUC_TRAINER_SUBTITLE_TEXT_COLOR",
                           callback=_callback_update_trainer_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)

        dpg.add_text("Question Timer", indent=20)
        with dpg.group(horizontal=True, indent=20):
            global duc_unlimited_question_timer_mark, duc_question_timer_input_text
            duc_unlimited_question_timer_mark = dpg.add_checkbox(label="Unlimited Timer", source="bool_value", callback=_set_question_timer)
            duc_question_timer_input_text = dpg.add_input_text(label="Question Timer in Seconds", width=100, decimal=True, default_value='60', callback=_set_question_timer)

        dpg.add_button(label="Save Setting", show=True, callback=_save_color_set)
