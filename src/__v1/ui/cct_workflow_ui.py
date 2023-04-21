import sys

import dearpygui.dearpygui as dpg

from __v1 import cct_advanced_options_ui as caou
from __v1 import hrsa_cct_globals, cct_ui_panels

# Workflow Options - Constants
CHOOSE_WORKFLOW_RADIO_BUTTON: str = "CHOOSE_WORKFLOW_RADIO_BUTTON"
CREATE_SCENARIO_BY_COPYING_EXISTING_OPTION: str = "Create Scenario"
EDIT_EXISTING_SCENARIO_OPTION: str = "Edit Scenario"
TRANSFER_SCENARIO_TO_DEVICE_OPTION: str = "Transfer to Device"
SHOW_ALL_MODULES: str = "Show All Modules"
CWU_SHOW_ADVANCED_OPTIONS: str = "CWU_SHOW_ADVANCED_OPTIONS"
WORKFLOW_OPTION_LIST: list = [
    CREATE_SCENARIO_BY_COPYING_EXISTING_OPTION,
    EDIT_EXISTING_SCENARIO_OPTION,
    TRANSFER_SCENARIO_TO_DEVICE_OPTION
]

DEFAULT_WORKFLOW_OPTION: str = CREATE_SCENARIO_BY_COPYING_EXISTING_OPTION

if hrsa_cct_globals.is_debug:
    WORKFLOW_OPTION_LIST.append(SHOW_ALL_MODULES)
    DEFAULT_WORKFLOW_OPTION: str = SHOW_ALL_MODULES


def _set_visibility_for_all_ui(is_visible: bool = False):
    dpg.configure_item(cct_ui_panels.CREATE_SCENARIO_COLLAPSING_HEADER, show=is_visible)
    # dpg.configure_item(cct_ui_panels.COPY_SCENARIO_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.SELECT_SCENARIO_COLLAPSING_HEADER, show=is_visible)

    set_edit_ui_visibility(is_visible)

    dpg.configure_item(cct_ui_panels.TRANSFER_TO_DEVICE_COLLAPSING_HEADER, show=is_visible)


def show_all_modules_ui():
    _set_visibility_for_all_ui(True)


def hide_all_modules_ui():
    _set_visibility_for_all_ui(False)


def show_create_scenario_by_copying_existing_scenario_ui():
    hide_all_modules_ui()
    dpg.configure_item(cct_ui_panels.CREATE_SCENARIO_COLLAPSING_HEADER, show=True)
    # dpg.configure_item(cct_ui_panels.COPY_SCENARIO_COLLAPSING_HEADER, show=True)


def set_edit_ui_visibility(is_visible: bool = False):
    dpg.configure_item(cct_ui_panels.CCT_PATIENT_INFO_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.CCT_SCENARIO_CONFIG_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.SHOW_INK_FILES_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.AUDIO_GENERATION_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.TRANSLATE_COLLAPSING_HEADER, show=is_visible)


def show_transfer_to_device_ui():
    hide_all_modules_ui()
    dpg.configure_item(cct_ui_panels.TRANSFER_TO_DEVICE_COLLAPSING_HEADER, show=True)


def show_edit_existing_scenario_ui():
    hide_all_modules_ui()
    dpg.configure_item(cct_ui_panels.SELECT_SCENARIO_COLLAPSING_HEADER, show=True)


def callback_on_choose_workflow_radio_button_clicked(sender, app_data, user_data):
    if app_data == CREATE_SCENARIO_BY_COPYING_EXISTING_OPTION:
        show_create_scenario_by_copying_existing_scenario_ui()
    elif app_data == EDIT_EXISTING_SCENARIO_OPTION:
        show_edit_existing_scenario_ui()
    elif app_data == TRANSFER_SCENARIO_TO_DEVICE_OPTION:
        show_transfer_to_device_ui()
    elif app_data == SHOW_ALL_MODULES:
        show_all_modules_ui()


def set_advanced_options_visibility(should_show_advanced_options):
    dpg.configure_item(caou.PIU_OPEN_FILE_DIALOG_BUTTON, show=should_show_advanced_options)
    dpg.configure_item(caou.SCU_OPEN_FILE_DIALOG_BUTTON, show=should_show_advanced_options)
    dpg.configure_item(caou.SIF_SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, show=should_show_advanced_options)
    dpg.configure_item(caou.SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, show=should_show_advanced_options)
    dpg.configure_item(caou.SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER, show=should_show_advanced_options)
    dpg.configure_item(caou.PIU_SCENARIO_PATIENT_INFO_JSON_PATH_TEXT, show=should_show_advanced_options)
    dpg.configure_item(caou.SCU_SCENARIO_CONFIG_JSON_PATH_TEXT, show=should_show_advanced_options)
    dpg.configure_item(caou.SIF_SCENARIO_DIRECTORY_PATH_TEXT, show=should_show_advanced_options)
    dpg.configure_item(caou.AG_SCENARIO_DIRECTORY_PATH_TEXT, show=should_show_advanced_options)
    caou.on_advanced_options_clicked(should_show_advanced_options)


def callback_on_show_advanced_options_clicked(sender, app_data, user_data):
    hrsa_cct_globals.show_advanced_options = dpg.get_value(CWU_SHOW_ADVANCED_OPTIONS)
    set_advanced_options_visibility(hrsa_cct_globals.show_advanced_options)


def init_data():
    # Set the default workflow
    default_workflow = dpg.get_value(CHOOSE_WORKFLOW_RADIO_BUTTON)
    callback_on_choose_workflow_radio_button_clicked(None, default_workflow, None)
    callback_on_show_advanced_options_clicked(None, None, None)


def init_ui():
    # Choose Workflow UI
    with dpg.collapsing_header(label="Choose Workflow", default_open=True):
        with dpg.group(horizontal=True):
            dpg.add_radio_button(items=WORKFLOW_OPTION_LIST, horizontal=True,
                                 tag=CHOOSE_WORKFLOW_RADIO_BUTTON, default_value=DEFAULT_WORKFLOW_OPTION, callback=callback_on_choose_workflow_radio_button_clicked)
            dpg.add_checkbox(label="Show Advanced Options", tag=CWU_SHOW_ADVANCED_OPTIONS, default_value=hrsa_cct_globals.show_advanced_options,
                             callback=callback_on_show_advanced_options_clicked)
        dpg.add_spacer(height=10)
        dpg.add_separator()


if sys.flags.dev_mode:
    print("cct_workflow_ui.__init__()")
