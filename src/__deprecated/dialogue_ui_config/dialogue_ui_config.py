import json

import dearpygui.dearpygui as dpg

from __deprecated import hrsa_cct_constants
from __deprecated.configuration import hrsa_config


# GUI Element Tags


# Module Variables

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
    global duc_color_setting
    duc_color_setting.player_config.ui_config.subtitle_config.text_color = hex_color


def _callback_update_medicalstudent_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global duc_color_setting
    duc_color_setting.medicalstudent_config.ui_config.subtitle_config.text_color = hex_color


def _callback_update_patient_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global duc_color_setting
    duc_color_setting.patient_config.ui_config.subtitle_config.text_color = hex_color


def _callback_update_trainer_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global duc_color_setting
    duc_color_setting.trainer_config.ui_config.subtitle_config.text_color = hex_color


duc_color_setting: hrsa_config.HRSAConfig = None
duc_unlimited_question_timer_mark = None
duc_question_timer_input_text = None


def _load_default_color_set(sender, app_data, user_data):
    global duc_color_setting
    with open('dialogue_ui_config/dialogue_ui_config.json', "r", encoding="UTF-8") as ui_config_file:
        row_data = ui_config_file.read()
        row_config = json.loads(row_data)
        duc_color_setting = hrsa_config.HRSAConfig(**row_config)
        _init_question_timer(duc_color_setting.conversation_config)
        _init_dialog_color(duc_color_setting)


def _save_color_set(sender, app_data, user_data):
    global duc_color_setting
    duc_color_setting_json = json.dumps(duc_color_setting.toJson(), indent=4)
    with open('dialogue_ui_config/dialogue_ui_config_back.json', "w", encoding="UTF-8") as outfile:
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
    global duc_color_setting
    if duc_color_setting is None:
        print('Test process, should load the configuration file firstly.')

    global duc_unlimited_question_timer_mark, duc_question_timer_input_text
    if sender == duc_unlimited_question_timer_mark:
        if app_data:
            dpg.hide_item(duc_question_timer_input_text)
            duc_color_setting.conversation_config.question_timer_in_seconds = 0
        else:
            dpg.show_item(duc_question_timer_input_text)
    else:
        duc_color_setting.conversation_config.question_timer_in_seconds = dpg.get_value(duc_question_timer_input_text)


def init_ui():
    with dpg.collapsing_header(label="Dialogue UI Config", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        # TODO: UI Creation
        dpg.add_button(label="Load Setting", callback=_load_default_color_set)
        dpg.add_button(label="Save Setting", callback=_save_color_set)

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
            duc_question_timer_input_text = dpg.add_input_text(label="Question Timer in Seconds", width=100, decimal=True, callback=_set_question_timer)
    _load_default_color_set(None, None, None)