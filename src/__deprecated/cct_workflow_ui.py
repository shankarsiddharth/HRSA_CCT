import dearpygui.dearpygui as dpg

from __deprecated import hrsa_cct_globals, cct_ui_panels

# Workflow Options - Constants
CHOOSE_WORKFLOW_RADIO_BUTTON: str = "CHOOSE_WORKFLOW_RADIO_BUTTON"
CREATE_SCENARIO_BY_COPYING_EXISTING_OPTION: str = "Create Scenario"
EDIT_EXISTING_SCENARIO_OPTION: str = "Edit Scenario"
TRANSFER_SCENARIO_TO_DEVICE_OPTION: str = "Transfer to Device"
SHOW_ALL_MODULES: str = "Show All Modules"
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
    dpg.configure_item(cct_ui_panels.COPY_SCENARIO_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.SELECT_SCENARIO_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.CCT_PATIENT_INFO_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.CCT_SCENARIO_CONFIG_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.SHOW_INK_FILES_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.AUDIO_GENERATION_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.TRANSLATE_COLLAPSING_HEADER, show=is_visible)
    dpg.configure_item(cct_ui_panels.TRANSFER_TO_DEVICE_COLLAPSING_HEADER, show=is_visible)


def show_all_modules_ui():
    _set_visibility_for_all_ui(True)


def hide_all_modules_ui():
    _set_visibility_for_all_ui(False)


def show_create_scenario_by_copying_existing_scenario_ui():
    show_all_modules_ui()
    dpg.configure_item(cct_ui_panels.TRANSFER_TO_DEVICE_COLLAPSING_HEADER, show=False)


def show_transfer_to_device_ui():
    hide_all_modules_ui()
    dpg.configure_item(cct_ui_panels.TRANSFER_TO_DEVICE_COLLAPSING_HEADER, show=True)


def show_edit_existing_scenario_ui():
    show_all_modules_ui()
    dpg.configure_item(cct_ui_panels.CREATE_SCENARIO_COLLAPSING_HEADER, show=False)
    dpg.configure_item(cct_ui_panels.COPY_SCENARIO_COLLAPSING_HEADER, show=False)
    dpg.configure_item(cct_ui_panels.TRANSFER_TO_DEVICE_COLLAPSING_HEADER, show=False)


def callback_on_choose_workflow_radio_button_clicked(sender, app_data, user_data):
    if app_data == CREATE_SCENARIO_BY_COPYING_EXISTING_OPTION:
        show_create_scenario_by_copying_existing_scenario_ui()
    elif app_data == EDIT_EXISTING_SCENARIO_OPTION:
        show_edit_existing_scenario_ui()
    elif app_data == TRANSFER_SCENARIO_TO_DEVICE_OPTION:
        show_transfer_to_device_ui()
    elif app_data == SHOW_ALL_MODULES:
        show_all_modules_ui()


def init_data():
    # Set the default workflow
    default_workflow = dpg.get_value(CHOOSE_WORKFLOW_RADIO_BUTTON)
    callback_on_choose_workflow_radio_button_clicked(None, default_workflow, None)


def init_ui():
    # Choose Workflow UI
    with dpg.collapsing_header(label="Choose Workflow", default_open=True):
        dpg.add_radio_button(items=WORKFLOW_OPTION_LIST, horizontal=True,
                             tag=CHOOSE_WORKFLOW_RADIO_BUTTON, default_value=DEFAULT_WORKFLOW_OPTION, callback=callback_on_choose_workflow_radio_button_clicked)
        dpg.add_separator()
