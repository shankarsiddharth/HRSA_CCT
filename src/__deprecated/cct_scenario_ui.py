import dearpygui.dearpygui as dpg

from __deprecated import cct_ui_panels, hrsa_cct_config

CSU_SELECT_SCENARIO_FROM_LIST_COLLAPSING_HEADER: str = "CSU_SELECT_SCENARIO_FROM_LIST_COLLAPSING_HEADER"
CSU_REFRESH_SCENARIO_LIST_BUTTON: str = "CSU_REFRESH_SCENARIO_LIST_BUTTON"
CSU_SELECT_SCENARIO_LISTBOX: str = "CSU_SELECT_SCENARIO_LISTBOX"
CSU_EDIT_SELECTED_SCENARIO_BUTTON: str = "CSU_EDIT_SELECTED_SCENARIO_BUTTON"
CSU_SELECT_SCENARIO_FOLDER_COLLAPSING_HEADER: str = "CSU_SELECT_SCENARIO_FOLDER_COLLAPSING_HEADER"
CSU_SELECT_SCENARIO_FOLDER_BUTTON: str = "CSU_SELECT_SCENARIO_FOLDER_BUTTON"
CSU_SELECTED_SCENARIO_FOLDER_TEXT: str = "CSU_SELECTED_SCENARIO_FOLDER_TEXT"

scenario_list: list = list()
current_scenario_name: str = ""


def get_scenario_list():
    global scenario_list

    if hrsa_cct_config.is_user_hrsa_data_folder_found():
        scenario_list = hrsa_cct_config.get_scenario_list()
    else:
        scenario_list = list()

    dpg.configure_item(CSU_SELECT_SCENARIO_LISTBOX, items=scenario_list)


def callback_on_scenario_selected(sender, app_data, user_data):
    global current_scenario_name
    scenario_name: str = dpg.get_value(CSU_SELECT_SCENARIO_LISTBOX)
    if scenario_name != "":
        current_scenario_name = scenario_name
    else:
        current_scenario_name = dpg.get_value(CSU_SELECT_SCENARIO_LISTBOX)


def callback_on_scenario_folder_button_clicked(sender, app_data, user_data):
    pass


def init_ui():
    with dpg.collapsing_header(label="Select Scenario", tag=cct_ui_panels.SELECT_SCENARIO_COLLAPSING_HEADER,
                               default_open=True):
        with dpg.collapsing_header(label="Choose Scenario from List", tag=CSU_SELECT_SCENARIO_FROM_LIST_COLLAPSING_HEADER,
                                   indent=20, default_open=True):
            dpg.add_button(label="Refresh Scenario List", indent=20, tag=CSU_REFRESH_SCENARIO_LIST_BUTTON,
                           callback=get_scenario_list)
            dpg.add_text("Select Scenario to Edit: ", indent=40)
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
