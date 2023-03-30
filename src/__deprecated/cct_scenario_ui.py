import os

import dearpygui.dearpygui as dpg

from __deprecated import cct_ui_panels, hrsa_cct_config, audio_generation, translate, show_ink_files, hrsa_cct_globals
from __deprecated.cct_patient_info_ui import cct_patient_info_ui
from __deprecated.cct_scenario_config import cct_scenario_config

CSU_SELECT_SCENARIO_FROM_LIST_COLLAPSING_HEADER: str = "CSU_SELECT_SCENARIO_FROM_LIST_COLLAPSING_HEADER"
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


def load_scenario_content(scenario_path: str):
    hrsa_cct_globals.scenario_path_destination = scenario_path
    audio_generation.callback_on_scenario_folder_selected(audio_generation.FILE_DIALOG_FOR_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    translate.callback_on_source_scenario_folder_selected(translate.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    cct_patient_info_ui.set_scenario_path(hrsa_cct_globals.scenario_path_destination)
    cct_scenario_config.set_scenario_path(hrsa_cct_globals.scenario_path_destination)
    show_ink_files.set_scenario_path(hrsa_cct_globals.scenario_path_destination)


def select_scenario_for_edit(scenario_name: str):
    scenario_path_root = os.path.join(hrsa_cct_config.get_user_hrsa_data_folder_path(), scenario_name)
    hrsa_cct_globals.app_data = dict(file_path_name=scenario_path_root)
    load_scenario_content(scenario_path_root)


def get_scenario_list():
    global scenario_list, current_scenario_name

    if hrsa_cct_config.is_user_hrsa_data_folder_found():
        scenario_list = hrsa_cct_config.get_scenario_list()
    else:
        scenario_list = list()

    dpg.configure_item(CSU_SELECT_SCENARIO_LISTBOX, items=scenario_list)

    current_scenario_name = dpg.get_value(CSU_SELECT_SCENARIO_LISTBOX)
    update_selected_scenario_in_ui()
    select_scenario_for_edit(current_scenario_name)


def update_selected_scenario_in_ui():
    global current_scenario_name
    text_to_display = CSU_SELECT_SCENARIO_TEXT + " (Selected: " + current_scenario_name + ")"
    dpg.configure_item(CSU_SELECTED_SCENARIO_TEXT_TAG, default_value=text_to_display)


def callback_on_scenario_selected(sender, app_data, user_data):
    global current_scenario_name
    scenario_name: str = dpg.get_value(CSU_SELECT_SCENARIO_LISTBOX)
    if scenario_name != "":
        current_scenario_name = scenario_name
    else:
        current_scenario_name = dpg.get_value(CSU_SELECT_SCENARIO_LISTBOX)

    update_selected_scenario_in_ui()
    select_scenario_for_edit(current_scenario_name)


def callback_on_scenario_folder_button_clicked(sender, app_data, user_data):
    pass


def init_ui():
    with dpg.collapsing_header(label="Select Scenario", tag=cct_ui_panels.SELECT_SCENARIO_COLLAPSING_HEADER,
                               default_open=True):
        with dpg.collapsing_header(label="Choose Scenario from List", tag=CSU_SELECT_SCENARIO_FROM_LIST_COLLAPSING_HEADER,
                                   indent=20, default_open=True):
            dpg.add_button(label="Refresh Scenario List", indent=20, tag=CSU_REFRESH_SCENARIO_LIST_BUTTON,
                           callback=get_scenario_list)
            dpg.add_text(CSU_SELECT_SCENARIO_TEXT, tag=CSU_SELECTED_SCENARIO_TEXT_TAG, indent=40)
            dpg.add_listbox(tag=CSU_SELECT_SCENARIO_LISTBOX, items=scenario_list, num_items=10,
                            callback=callback_on_scenario_selected, default_value="", indent=40)
            dpg.add_button(label="Edit Selected Scenario", tag=CSU_EDIT_SELECTED_SCENARIO_BUTTON, indent=20,
                           callback=callback_on_scenario_selected)

        dpg.add_spacer(height=10)
        dpg.add_text("OR")
        dpg.add_spacer(height=10)

        with dpg.collapsing_header(label="Select Scenario Folder", tag=CSU_SELECT_SCENARIO_FOLDER_COLLAPSING_HEADER,
                                   indent=20, default_open=True):
            dpg.add_button(label="Select Scenario Folder...", tag=CSU_SELECT_SCENARIO_FOLDER_BUTTON, indent=20, callback=callback_on_scenario_folder_button_clicked)
            dpg.add_text("", indent=20, tag=CSU_SELECTED_SCENARIO_FOLDER_TEXT)

        dpg.add_separator()


def init_data():
    get_scenario_list()
