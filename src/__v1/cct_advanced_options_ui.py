import sys

PIU_OPEN_FILE_DIALOG_BUTTON: str = "PIU_OPEN_FILE_DIALOG_BUTTON"
SCU_OPEN_FILE_DIALOG_BUTTON: str = "SCU_OPEN_FILE_DIALOG_BUTTON"
SIF_SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER: str = "SIF_SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER"

COMPILE_INK_SCRIPTS_BUTTON: str = "COMPILE_INK_SCRIPTS_BUTTON"

PIU_SCENARIO_PATIENT_INFO_JSON_PATH_TEXT: str = 'PIU_SCENARIO_DIRECTORY_PATH_TEXT'
SCU_SCENARIO_CONFIG_JSON_PATH_TEXT: str = 'SCU_SCENARIO_CONFIG_JSON_PATH_TEXT'
SIF_SCENARIO_DIRECTORY_PATH_TEXT: str = 'SIF_SCENARIO_DIRECTORY_PATH_TEXT'
AG_SCENARIO_DIRECTORY_PATH_TEXT: str = "AG_SCENARIO_DIRECTORY_PATH_TEXT"

advanced_options_delegate_list: list = list()


def add_advanced_options_delegate(delegate):
    advanced_options_delegate_list.append(delegate)


def remove_advanced_options_delegate(delegate):
    advanced_options_delegate_list.remove(delegate)


def on_advanced_options_clicked(should_show_advanced_options):
    for delegate in advanced_options_delegate_list:
        delegate(should_show_advanced_options)


if sys.flags.dev_mode:
    print("cct_file_folder_selector_ui.__init__()")
