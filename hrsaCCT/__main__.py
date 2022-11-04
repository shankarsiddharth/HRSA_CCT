import os
import shutil
import json

import dearpygui.dearpygui as dpg
from dearpygui_ext import themes

import hrsa_cct_globals
from hrsa_cct_globals import log

import audio_generation
import hrsa_cct_constants
import translate
from patient_info_ui import patient_info_ui
from dialogue_ui_config import dialogue_ui_config

# logger = dpg_logger.mvLogger()
# logger.log("mv Logger Started")
# TODO: Split into modules and change the global data variable to function return values

# DearPyGUI's Viewport Constants
VIEWPORT_WIDTH = 900
VIEWPORT_HEIGHT = 900  # 700

# GUI Element Tags
SCENARIO_NAME_INPUT_TEXT: str = "SCENARIO_NAME_INPUT_TEXT"
SCENARIO_DESCRIPTION_INPUT_TEXT: str = "SCENARIO_DESCRIPTION_INPUT_TEXT"
SCENARIO_DETAIL_INPUT_TEXT: str = "SCENARIO_DETAIL_INPUT_TEXT"
CREATE_SCENARIO_INFORMATION_BUTTON: str = "CREATE_SCENARIO_INFORMATION_BUTTON"
FILE_DIALOG: str = "FILE_DIALOG"
FILE_DIALOG_FOR_DATA_FOLDER: str = "FILE_DIALOG_FOR_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER"
DATA_DIRECTORY_PATH_TEXT: str = "DATA_DIRECTORY_PATH_TEXT"
FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER"
SCENARIO_DIRECTORY_PATH_TEXT_SOURCE: str = "SCENARIO_DIRECTORY_PATH_TEXT_SOURCE"
FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_DESTINATION_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_DESTINATION_FOLDER"
SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION: str = "SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION"
COPY_SCENARIO_INFORMATION_BUTTON: str = "COPY_SCENARIO_INFORMATION_BUTTON"

# Global Variable
data_path = ""
scenario_path = ""
scenario_path_source = ""
scenario_path_destination = ""
room_dialogue_data = dict()
character_voice_config_data = dict()
ink_file_path_list = []


def create_scenario_folders(scenario_name, scenario_information_json_object) -> None:
    global data_path, scenario_path
    # Scenario Folder
    scenario_path_root = os.path.join(data_path, scenario_name)
    log.info("scenario_path_root: " + scenario_path_root)
    # TODO: Check if the a scenario name already exists and display error information to the user
    os.mkdir(scenario_path_root)
    # Default Language Folder
    default_language_folder = os.path.join(scenario_path_root, hrsa_cct_globals.default_language_code)
    log.info("default_language_folder: " + default_language_folder)
    os.mkdir(default_language_folder)
    scenario_path = os.path.abspath(default_language_folder)
    # Scenario Information JSON
    scenario_information_json_path = os.path.join(scenario_path, hrsa_cct_constants.SCENARIO_INFORMATION_JSON_FILE_NAME)
    log.info("scenario_information_json_path: " + scenario_information_json_path)
    with open(scenario_information_json_path, "w", encoding="utf-8") as output_file:
        output_file.write(scenario_information_json_object)
    # Break Room
    break_room_folder_path = os.path.join(scenario_path, hrsa_cct_constants.BREAK_ROOM_NAME)
    os.mkdir(break_room_folder_path)
    audio_folder = os.path.join(break_room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Patient Room
    patient_room_folder_path = os.path.join(scenario_path, hrsa_cct_constants.PATIENT_ROOM_NAME)
    os.mkdir(patient_room_folder_path)
    audio_folder = os.path.join(patient_room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Feedback Room
    feedback_room_folder_path = os.path.join(scenario_path, hrsa_cct_constants.FEEDBACK_ROOM_NAME)
    os.mkdir(feedback_room_folder_path)
    # Break Room Feedback
    break_room_feedback_folder_path = os.path.join(feedback_room_folder_path, hrsa_cct_constants.FEEDBACK_TYPE_BREAK_ROOM_NAME)
    os.mkdir(break_room_feedback_folder_path)
    audio_folder = os.path.join(break_room_feedback_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_feedback_folder_path, hrsa_cct_constants.FEEDBACK_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Patient Room Feedback
    patient_room_feedback_folder_path = os.path.join(feedback_room_folder_path, hrsa_cct_constants.FEEDBACK_TYPE_PATIENT_ROOM_NAME)
    os.mkdir(patient_room_feedback_folder_path)
    audio_folder = os.path.join(patient_room_feedback_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_feedback_folder_path, hrsa_cct_constants.FEEDBACK_INK_FILE_NAME)
    open(file_path, 'a').close()
    log.info("New Scenario Created. Scenario Name: " + scenario_name)

    hrsa_cct_globals.app_data = dict(file_path_name=scenario_path_root)
    callback_on_scenario_destination_folder_selected(FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION, hrsa_cct_globals.app_data)


def callback_on_data_folder_selected(sender, app_data):
    log.debug("Sender: " + str(sender), False)
    log.debug("App Data: " + str(app_data), False)
    global data_path
    data_path = os.path.normpath(str(app_data['file_path_name']))
    log.info('Data Folder Path: ' + data_path)
    dpg.configure_item(DATA_DIRECTORY_PATH_TEXT, default_value=data_path)
    log.info('Data Folder Selected')
    # TODO : Error Checking of Valid Data Folder


# def callback_on_select_data_folder_button_clicked():
#     dpg.configure_item(FILE_DIALOG_FOR_DATA_FOLDER, show=True, modal=True)
#
#
# def callback_show_file_dialog_scenario_folder():
#     dpg.configure_item(FILE_DIALOG_FOR_SCENARIO_FOLDER, show=True, modal=True)


def callback_on_show_file_dialog_clicked(item_tag):
    dpg.configure_item(item_tag, show=True, modal=True)


def callback_on_create_scenario_button_clicked() -> None:
    scenario_name = dpg.get_value(SCENARIO_NAME_INPUT_TEXT)
    scenario_description = dpg.get_value(SCENARIO_DESCRIPTION_INPUT_TEXT)
    scenario_detail = dpg.get_value(SCENARIO_DETAIL_INPUT_TEXT)
    scenario_information = dict()
    scenario_information["name"] = scenario_name
    scenario_information["localized_name"] = scenario_name
    scenario_information["description"] = scenario_description
    scenario_information["detail"] = scenario_detail
    scenario_information_json_object = json.dumps(scenario_information, indent=4)
    create_scenario_folders(scenario_name, scenario_information_json_object)


def callback_on_scenario_source_folder_selected(sender, app_data):
    log.debug("Sender: " + str(sender), False)
    log.debug("App Data: " + str(app_data), False)
    global scenario_path_source
    scenario_path_source = os.path.normpath(str(app_data['file_path_name']))
    log.info("Source Scenario Path: " + scenario_path_source)
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT_SOURCE, default_value=scenario_path_source)


def callback_on_scenario_destination_folder_selected(sender, app_data):
    log.debug("Sender: " + str(sender), False)
    log.debug("App Data: " + str(app_data), False)
    global scenario_path_destination
    scenario_path_destination = os.path.normpath(str(app_data['file_path_name']))
    log.info("Destination Scenario Path: " + scenario_path_destination)
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION, default_value=scenario_path_destination)


def callback_on_copy_scenario_button_clicked():
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=False)
    global scenario_path_source, scenario_path_destination
    shutil.copytree(scenario_path_source, scenario_path_destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('*.mp3', '*.wav', 'scenario_information.json', 'feedback.json', 'dialogue.json'))
    log.info("Scenario Folder Copy Complete from: " + scenario_path_source + "\tto: " + scenario_path_destination)
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=True)

    audio_generation.callback_on_scenario_folder_selected(audio_generation.FILE_DIALOG_FOR_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    translate.callback_on_source_scenario_folder_selected(translate.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    patient_info_ui.set_scenario_path(scenario_path_destination)


def save_init():
    dpg.save_init_file("dpg.ini")


def main() -> None:
    dpg.create_context()
    # light_theme_id = themes.create_theme_imgui_light()
    # dark_theme_id = themes.create_theme_imgui_dark()
    # dpg.bind_theme(dark_theme_id)
    # dpg.configure_app(manual_callback_management=False, docking=True, docking_space=True, init_file="dpg.ini")
    dpg.configure_app(manual_callback_management=True, docking=True, docking_space=True, init_file="dpg.ini")
    dpg.create_viewport(title='HRSA Content Creation Tool', width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT)

    with dpg.window(label="HRSA CCT", tag=hrsa_cct_constants.HRSA_CCT_TOOL, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT, no_title_bar=True, no_close=True):
        dpg.add_button(label="Save Init", callback=lambda: save_init)
        with dpg.collapsing_header(label="Choose a location to create the Data Folder", default_open=True):
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_DATA_FOLDER, height=300, width=450, directory_selector=True, show=False, callback=callback_on_data_folder_selected)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER, label="Select Data Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_DATA_FOLDER))
            dpg.add_text(tag=DATA_DIRECTORY_PATH_TEXT)
            dpg.add_separator()

        with dpg.collapsing_header(label="Create Scenario", default_open=False):
            dpg.add_input_text(tag=SCENARIO_NAME_INPUT_TEXT, label="Scenario Name", default_value="")
            dpg.add_input_text(tag=SCENARIO_DESCRIPTION_INPUT_TEXT, label="Scenario Description", multiline=True, tab_input=False)
            dpg.add_input_text(tag=SCENARIO_DETAIL_INPUT_TEXT, label="Scenario Detail", multiline=True, tab_input=False)
            dpg.add_button(tag=CREATE_SCENARIO_INFORMATION_BUTTON, label="Create Scenario Folder", callback=callback_on_create_scenario_button_clicked)
            dpg.add_separator()

        with dpg.collapsing_header(label="Copy Scenario Content", default_open=False):
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE, height=300, width=450, directory_selector=True, show=False,
                                callback=callback_on_scenario_source_folder_selected)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER, label="Select Source Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE))
            dpg.add_text(tag=SCENARIO_DIRECTORY_PATH_TEXT_SOURCE)
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION, height=300, width=450, directory_selector=True, show=False,
                                callback=callback_on_scenario_destination_folder_selected)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_SCENARIO_DESTINATION_FOLDER, label="Select Destination Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION))
            dpg.add_text(tag=SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION)
            dpg.add_button(tag=COPY_SCENARIO_INFORMATION_BUTTON, label="Copy Scenario Folder", callback=callback_on_copy_scenario_button_clicked)
            dpg.add_separator()

        # Patient Info UI - Initialize
        patient_info_ui.init_ui()

        # Dialogue UI Config- Initialize
        dialogue_ui_config.init_ui()

        with dpg.collapsing_header(label="Choose the Scenario Folder for Audio Generation", default_open=False):
            dpg.add_file_dialog(tag=audio_generation.FILE_DIALOG_FOR_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False,
                                callback=audio_generation.callback_on_scenario_folder_selected)
            dpg.add_button(tag=audio_generation.SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, label="Select Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=audio_generation.FILE_DIALOG_FOR_SCENARIO_FOLDER))
            dpg.add_text(tag=audio_generation.SCENARIO_DIRECTORY_PATH_TEXT)
            with dpg.group(tag=audio_generation.AG_LANGUAGE_LISTBOX_GROUP, horizontal=True, show=False):
                dpg.add_text("Audio Generation Language: ")
                dpg.add_listbox(tag=audio_generation.AG_LANGUAGE_LISTBOX, items=hrsa_cct_globals.language_list,
                                callback=audio_generation.callback_on_language_code_selected, default_value="")
            dpg.add_text(tag=audio_generation.SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, show=False)
            # TODO: Voice Configuration
            with dpg.collapsing_header(indent=50, tag=audio_generation.VOICE_CONFIG_SECTION, label="Configure Character Voice Settings", default_open=True, show=False):
                dpg.add_listbox(tag=audio_generation.CHARACTER_SELECT_LISTBOX, label="Choose Character", num_items=5, show=True, callback=audio_generation.display_character_info)
                dpg.add_listbox(tag=audio_generation.LANGUAGE_CODE_TEXT, label="Language Code", num_items=4, callback=audio_generation.callback_on_change_language_code)
                dpg.add_listbox(tag=audio_generation.AUDIO_GENDER_TEXT, label="Gender", num_items=3, show=True, callback=audio_generation.callback_on_gender_selected)
                dpg.add_listbox(tag=audio_generation.AUDIO_VOICE_LIST, label="Voice", num_items=10, tracked=True)
                dpg.add_button(tag=audio_generation.SAVE_AUDIO_SETTINGS_BUTTON, label="Save voice settings", show=True, callback=audio_generation.save_audio_settings)
            dpg.add_button(tag=audio_generation.GENERATE_AUDIO_BUTTON, label="Generate Audio", show=False, callback=audio_generation.callback_on_generate_audio_clicked)
            dpg.add_separator()

        with dpg.collapsing_header(label="Choose a location to create the Translated Data Folder", default_open=False):
            dpg.add_file_dialog(tag=translate.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False,
                                callback=translate.callback_on_source_scenario_folder_selected)
            dpg.add_button(tag=translate.SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER, label="Select Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=translate.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER))
            with dpg.group(tag=translate.SOURCE_SECTION_GROUP, horizontal=True, show=False):
                dpg.add_text("Selected Source Language Folder (en) : ")
                dpg.add_text(tag=translate.SOURCE_SCENARIO_DIRECTORY_PATH_TEXT)
            with dpg.group(tag=translate.LANGUAGE_LISTBOX_GROUP, horizontal=True, show=False):
                dpg.add_text("Language To Translate: ")
                dpg.add_listbox(tag=translate.LANGUAGE_LISTBOX, items=hrsa_cct_globals.language_list,
                                callback=translate.set_new_language_code, default_value="")
            with dpg.group(tag=translate.DESTINATION_SECTION_GROUP, horizontal=True, show=False):
                dpg.add_text("Destination Language Folder: ")
                dpg.add_text(tag=translate.NEW_DATA_DIRECTORY_PATH_TEXT)
            dpg.add_button(tag=translate.TRANSLATE_TEXT_BUTTON, label="Translate Data", show=False, callback=translate.callback_on_translate_text_clicked)
            dpg.add_separator()

    log.init_ui()

    dpg.setup_dearpygui()
    dpg.show_viewport()

    # dpg.set_primary_window(hrsa_cct_constants.HRSA_CCT_TOOL, True)

    # dpg.start_dearpygui()

    while dpg.is_dearpygui_running():
        jobs = dpg.get_callback_queue()  # retrieves and clears queue
        dpg.run_callbacks(jobs)
        dpg.render_dearpygui_frame()

    dpg.destroy_context()


if __name__ == "__main__":
    main()
