import json
import os
import pathlib
import re
import shutil
import sys
from dataclasses import asdict

import dearpygui.dearpygui as dpg

from __v1 import cct_ui_panels, hrsa_cct_config, hrsa_cct_globals, hrsa_cct_constants
from __v1.hrsa_cct_globals import log, hfs
from __v1.ui import cct_patient_info_ui, cct_scenario_config_ui, audio_generation_ui, translate_ui, show_ink_files_ui, cct_workflow_ui
from hrsa_data.scenario_data.scenario_information.scenario_information import ScenarioInformation

# region Create Scenario Constants and Variables
SCENARIO_NAME_INPUT_TEXT: str = "SCENARIO_NAME_INPUT_TEXT"
SCENARIO_DESCRIPTION_INPUT_TEXT: str = "SCENARIO_DESCRIPTION_INPUT_TEXT"
CREATE_SCENARIO_INFORMATION_BUTTON: str = "CREATE_SCENARIO_INFORMATION_BUTTON"
FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER"
SCENARIO_DIRECTORY_PATH_TEXT_SOURCE: str = "SCENARIO_DIRECTORY_PATH_TEXT_SOURCE"
COPY_SCENARIO_INFORMATION_BUTTON: str = "COPY_SCENARIO_INFORMATION_BUTTON"
USE_SCENARIO_TEMPLATE_CHECKBOX: str = "USE_SCENARIO_TEMPLATE_CHECKBOX"

# endregion Create Scenario Constants and Variables

# region Select Scenario Constants and Variables
CSU_REFRESH_SCENARIO_LIST_BUTTON: str = "CSU_REFRESH_SCENARIO_LIST_BUTTON"
CSU_SELECT_SCENARIO_LISTBOX: str = "CSU_SELECT_SCENARIO_LISTBOX"
CSU_EDIT_SELECTED_SCENARIO_BUTTON: str = "CSU_EDIT_SELECTED_SCENARIO_BUTTON"
CSU_SELECT_SCENARIO_FOLDER_COLLAPSING_HEADER: str = "CSU_SELECT_SCENARIO_FOLDER_COLLAPSING_HEADER"
CSU_SELECT_SCENARIO_FOLDER_BUTTON: str = "CSU_SELECT_SCENARIO_FOLDER_BUTTON"
CSU_SELECTED_SCENARIO_FOLDER_TEXT: str = "CSU_SELECTED_SCENARIO_FOLDER_TEXT"
CSU_SELECTED_SCENARIO_TEXT_TAG: str = "CSU_SELECTED_SCENARIO_TEXT_TAG"
CSU_SELECT_SCENARIO_TEXT: str = "Select Scenario to Edit: "

scenario_list: list = list()
current_scenario_name: str = ""


# endregion Select Scenario Constants and Variables

# region Create Scenario Methods
def callback_on_scenario_source_folder_selected(sender, app_data):
    hrsa_cct_globals.scenario_path_source = os.path.normpath(str(app_data['file_path_name']))
    log.trace("Source Scenario Path: " + hrsa_cct_globals.scenario_path_source)
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT_SOURCE, default_value=hrsa_cct_globals.scenario_path_source)


def create_scenario_folders(scenario_name, scenario_information_json_object) -> bool:
    # Scenario Name Validation
    scenario_name = scenario_name.strip()
    if scenario_name == "":
        log.error("Scenario Name cannot be empty")
        return False
    if not re.match(hrsa_cct_globals.scenario_name_regular_expression, scenario_name):
        log.error("Scenario Name is not valid. Invalid Name: " + scenario_name)
        return False
    # Scenario Folder
    scenario_path_root = os.path.join(hrsa_cct_config.get_user_hrsa_data_folder_path(), scenario_name)
    log.trace("scenario_path_root: " + scenario_path_root)
    # TODO: Check if the a scenario name already exists and display error information to the user
    try:
        os.mkdir(scenario_path_root)
    except FileExistsError:
        log.error("Scenario folder already exists: " + scenario_name)
        return False
    except Exception as e:
        log.error("Scenario Name is not valid. Invalid Name: " + scenario_name)
        log.error(e)
        return False
    # Default Language Folder
    default_language_folder = os.path.join(scenario_path_root, hrsa_cct_globals.default_language_code)
    log.trace("default_language_folder: " + default_language_folder)
    os.mkdir(default_language_folder)
    hrsa_cct_globals.scenario_path = os.path.abspath(default_language_folder)
    # Scenario Information JSON
    scenario_information_json_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.SCENARIO_INFORMATION_JSON_FILE_NAME)
    log.trace("scenario_information_json_path: " + scenario_information_json_path)
    with open(scenario_information_json_path, "w", encoding="utf-8") as output_file:
        output_file.write(scenario_information_json_object)
    # Break Room
    break_room_folder_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.BREAK_ROOM_NAME)
    os.mkdir(break_room_folder_path)
    audio_folder = os.path.join(break_room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Patient Room
    patient_room_folder_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.PATIENT_ROOM_NAME)
    os.mkdir(patient_room_folder_path)
    audio_folder = os.path.join(patient_room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Feedback Room
    feedback_room_folder_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.FEEDBACK_ROOM_NAME)
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
    log.trace("New Scenario Created. Scenario Name: " + scenario_name)

    hrsa_cct_globals.app_data = dict(file_path_name=scenario_path_root)
    hrsa_cct_globals.scenario_path_destination = os.path.normpath(scenario_path_root)
    # callback_on_scenario_destination_folder_selected(FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION, hrsa_cct_globals.app_data)
    return True


def on_create_scenario_button_clicked() -> bool:
    scenario_name = dpg.get_value(SCENARIO_NAME_INPUT_TEXT)
    scenario_description = dpg.get_value(SCENARIO_DESCRIPTION_INPUT_TEXT)
    if scenario_name == "" or scenario_description == "":
        log.error("Scenario Name or Scenario Description cannot be Empty")
        return False

    scenario_information: ScenarioInformation = ScenarioInformation()
    scenario_information.name = scenario_name
    scenario_information.localized_name = scenario_name
    scenario_information.description = scenario_description
    scenario_information_json_object = json.dumps(asdict(scenario_information), indent=4)
    return create_scenario_folders(scenario_name, scenario_information_json_object)


def on_copy_scenario_button_clicked():
    source_path = hrsa_cct_globals.scenario_path_source
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=False)
    shutil.copytree(source_path, hrsa_cct_globals.scenario_path_destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('*.mp3', '*.wav', 'scenario_information.json', 'feedback.json', 'dialogue.json', 'es-US'))
    log.trace("Scenario Folder Copy Complete from: " + hrsa_cct_globals.scenario_path_source + "\tto: " + hrsa_cct_globals.scenario_path_destination)
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=True)

    set_current_scenario_path(hrsa_cct_globals.scenario_path_destination)


def callback_on_create_scenario_by_copy_button_clicked():
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=False)
    create_scenario_by_copy()
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=True)


def create_scenario_by_copy():
    is_checked = dpg.get_value(USE_SCENARIO_TEMPLATE_CHECKBOX)
    if is_checked:
        template_folder_path = hfs.get_default_data_scenario_template_folder_path()
        default_language_folder_path = os.path.join(template_folder_path, hrsa_cct_globals.default_language_code)
        default_language_folder = pathlib.Path(default_language_folder_path)
        if not default_language_folder.exists():
            log.error("Default Language Folder Scenario Template does not exist. Path: " + default_language_folder_path)
            return None
        hrsa_cct_globals.scenario_path_source = template_folder_path
    if hrsa_cct_globals.scenario_path_source is None \
            or hrsa_cct_globals.scenario_path_source == "" \
            or len(hrsa_cct_globals.scenario_path_source) == 0:
        log.error("Please, Select Source Scenario Folder and Try Again")
        return None
    is_scenario_created = on_create_scenario_button_clicked()
    if is_scenario_created:
        on_copy_scenario_button_clicked()
        log.clear_log()
        log.success("Scenario Created Successfully.")


def callback_on_use_scenario_template_checkbox_clicked():
    is_checked = dpg.get_value(USE_SCENARIO_TEMPLATE_CHECKBOX)
    if is_checked:
        dpg.configure_item(SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER, show=False)
    else:
        dpg.configure_item(SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER, show=True)


def callback_on_show_file_dialog_clicked(item_tag):
    dpg.configure_item(item_tag, show=True, modal=True)


def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


# endregion Create Scenario Methods

# region Select Scenario Folder Methods
def set_current_scenario_path(scenario_path: str):
    refresh_scenario_list()

    path = pathlib.PurePath(scenario_path)
    global current_scenario_name
    current_scenario_name = path.name
    dpg.configure_item(CSU_SELECT_SCENARIO_LISTBOX, default_value=current_scenario_name)

    update_selected_scenario_text_ui()
    update_globals_app_data()
    load_scenario_content(hrsa_cct_globals.app_data["file_path_name"])
    cct_workflow_ui.set_edit_ui_visibility(True)


def load_scenario_content(scenario_path: str):
    hrsa_cct_globals.scenario_path_destination = scenario_path
    audio_generation_ui.callback_on_scenario_folder_selected(audio_generation_ui.FILE_DIALOG_FOR_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    translate_ui.callback_on_source_scenario_folder_selected(translate_ui.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    cct_patient_info_ui.set_scenario_path(hrsa_cct_globals.scenario_path_destination)
    cct_scenario_config_ui.set_scenario_path(hrsa_cct_globals.scenario_path_destination)
    show_ink_files_ui.set_scenario_path(hrsa_cct_globals.scenario_path_destination)


def refresh_scenario_list():
    global scenario_list, current_scenario_name

    if hrsa_cct_config.is_user_hrsa_data_folder_found():
        scenario_list = hrsa_cct_config.get_scenario_list()
    else:
        scenario_list = list()

    scenario_list.insert(0, hrsa_cct_globals.default_selected_scenario)
    dpg.configure_item(CSU_SELECT_SCENARIO_LISTBOX, items=scenario_list)


def update_selected_scenario_text_ui():
    global current_scenario_name
    text_to_display = CSU_SELECT_SCENARIO_TEXT + " (Selected: " + current_scenario_name + ")"
    if current_scenario_name == hrsa_cct_globals.default_selected_scenario:
        text_to_display = CSU_SELECT_SCENARIO_TEXT + " (Selected: None)"
    dpg.configure_item(CSU_SELECTED_SCENARIO_TEXT_TAG, default_value=text_to_display)


def update_globals_app_data():
    scenario_path_root = os.path.join(hrsa_cct_config.get_user_hrsa_data_folder_path(), current_scenario_name)
    hrsa_cct_globals.app_data = dict(file_path_name=scenario_path_root)


def callback_on_scenario_selected(sender, app_data, user_data):
    global current_scenario_name
    current_scenario_name = dpg.get_value(CSU_SELECT_SCENARIO_LISTBOX)

    update_selected_scenario_text_ui()

    if current_scenario_name != hrsa_cct_globals.default_selected_scenario:
        update_globals_app_data()
        load_scenario_content(hrsa_cct_globals.app_data["file_path_name"])
        cct_workflow_ui.set_edit_ui_visibility(True)
    else:
        cct_workflow_ui.set_edit_ui_visibility(False)


def callback_on_scenario_folder_button_clicked(sender, app_data, user_data):
    pass


# endregion Select Scenario Folder Methods


def init_ui():
    # region Create Scenario UI
    with dpg.collapsing_header(label="Create Scenario",
                               tag=cct_ui_panels.CREATE_SCENARIO_COLLAPSING_HEADER,
                               default_open=True, open_on_double_click=False, open_on_arrow=False):
        dpg.add_input_text(tag=SCENARIO_NAME_INPUT_TEXT, label="Scenario Name", default_value="")
        dpg.add_input_text(tag=SCENARIO_DESCRIPTION_INPUT_TEXT, label="Scenario Description", multiline=True, tab_input=False)
        dpg.add_spacer(height=5)
        dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE, height=300, width=450, directory_selector=True, show=False,
                            callback=callback_on_scenario_source_folder_selected,
                            default_path=hrsa_cct_config.get_file_dialog_default_path(),
                            cancel_callback=file_dialog_cancel_callback)
        dpg.add_checkbox(tag=USE_SCENARIO_TEMPLATE_CHECKBOX, label="Use Scenario Template", default_value=True, callback=callback_on_use_scenario_template_checkbox_clicked)
        dpg.add_spacer(height=5)
        dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER, label="Select Source Scenario Folder...",
                       callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE))
        dpg.add_text(tag=SCENARIO_DIRECTORY_PATH_TEXT_SOURCE)
        dpg.add_spacer(height=5)
        dpg.add_button(tag=COPY_SCENARIO_INFORMATION_BUTTON, label="Create Scenario", callback=callback_on_create_scenario_by_copy_button_clicked)
        dpg.add_separator()
    # endregion Create Scenario UI

    # region Select Scenario UI
    with dpg.collapsing_header(label="Select Scenario",
                               tag=cct_ui_panels.SELECT_SCENARIO_COLLAPSING_HEADER,
                               default_open=True, open_on_double_click=False, open_on_arrow=False):
        dpg.add_button(label="Refresh Scenario List", indent=20, tag=CSU_REFRESH_SCENARIO_LIST_BUTTON,
                       callback=refresh_scenario_list, show=False)
        dpg.add_text(CSU_SELECT_SCENARIO_TEXT, tag=CSU_SELECTED_SCENARIO_TEXT_TAG, indent=40)
        dpg.add_listbox(tag=CSU_SELECT_SCENARIO_LISTBOX, items=scenario_list, num_items=10,
                        callback=callback_on_scenario_selected, default_value="", indent=40)
        dpg.add_button(label="Edit Selected Scenario", tag=CSU_EDIT_SELECTED_SCENARIO_BUTTON, indent=20,
                       callback=callback_on_scenario_selected, show=False)

        dpg.add_separator()

    # with dpg.group(show=False):
    #     dpg.add_spacer(height=10)
    #     dpg.add_text("OR")
    #     dpg.add_spacer(height=10)
    #
    # with dpg.collapsing_header(label="Select Scenario Folder", tag=CSU_SELECT_SCENARIO_FOLDER_COLLAPSING_HEADER,
    #                            indent=20, default_open=True, show=False):
    #     dpg.add_button(label="Select Scenario Folder...", tag=CSU_SELECT_SCENARIO_FOLDER_BUTTON, indent=20, callback=callback_on_scenario_folder_button_clicked)
    #     dpg.add_text("", indent=20, tag=CSU_SELECTED_SCENARIO_FOLDER_TEXT)

    # endregion Select Scenario UI


def init_data():
    refresh_scenario_list()
    callback_on_use_scenario_template_checkbox_clicked()


if sys.flags.dev_mode:
    print("cct_scenario_ui.__init__()")
