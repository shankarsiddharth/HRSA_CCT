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
    duc_color_setting.player.ui.subtitle.text_color = hex_color


def _callback_update_medicalstudent_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global duc_color_setting
    duc_color_setting.medicalstudent.ui.subtitle.text_color = hex_color


def _callback_update_patient_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global duc_color_setting
    duc_color_setting.patient.ui.subtitle.text_color = hex_color


def _callback_update_trainer_subtitle_text_color(sender, app_data, user_data):
    rgb_color = [int(value) for value in dpg.get_value(sender)[:-1]]
    rgb_color = tuple(rgb_color)
    hex_color = '#%02x%02x%02x' % rgb_color
    # print(rgb_color, hex_color)
    global duc_color_setting
    duc_color_setting.trainer.ui.subtitle.text_color = hex_color


duc_color_setting = None


def _load_default_color_set(sender, app_data, user_data):
    global duc_color_setting
    with open('dialogue_ui_config/dialogue_ui_config.json', "r", encoding="UTF-8") as ui_config_file:
        row_data = ui_config_file.read()
        row_config = json.loads(row_data)
        duc_color_setting = hrsa_config.HRSAConfig(**row_config)


def _save_color_set(sender, app_data, user_data):
    global duc_color_setting
    duc_color_setting_json = json.dumps(duc_color_setting.toJson(), indent=4)
    with open('dialogue_ui_config/dialogue_ui_config_back.json', "w", encoding="UTF-8") as outfile:
        outfile.write(duc_color_setting_json)


def init_ui():
    _load_default_color_set(None, None, None)

    with dpg.collapsing_header(label="Dialogue UI Config", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        # TODO: UI Creation
        dpg.add_button(label="Load Setting", callback=_load_default_color_set)
        dpg.add_button(label="Save Setting", callback=_save_color_set)

        dpg.add_color_edit(default_value=_hex_to_rgb(duc_color_setting.player.ui.subtitle.text_color), label="Player Subtitle Text Color",
                           tag="DUC_PLAYER_SUBTITLE_TEXT_COLOR", callback=_callback_update_player_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)

        dpg.add_color_edit(default_value=_hex_to_rgb(duc_color_setting.medicalstudent.ui.subtitle.text_color), label="Medical Student Subtitle Text Color",
                           tag="DUC_MEDICALSTUDENT_SUBTITLE_TEXT_COLOR", callback=_callback_update_medicalstudent_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)

        dpg.add_color_edit(default_value=_hex_to_rgb(duc_color_setting.patient.ui.subtitle.text_color), label="Patient Subtitle Text Color",
                           tag="DUC_PATIENT_SUBTITLE_TEXT_COLOR", callback=_callback_update_patient_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)

        dpg.add_color_edit(default_value=_hex_to_rgb(duc_color_setting.trainer.ui.subtitle.text_color), label="Trainer Subtitle Text Color",
                           tag="DUC_TRAINER_SUBTITLE_TEXT_COLOR", callback=_callback_update_trainer_subtitle_text_color, input_mode=dpg.mvColorEdit_input_rgb)
