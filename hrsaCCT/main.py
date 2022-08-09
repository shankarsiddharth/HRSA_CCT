from email.policy import default
import os
import json
import subprocess
from unicodedata import name
import dearpygui.dearpygui as dpg
import audio_generation
import translate

# TODO: Split into modules and change the global data variable to function return values

# Constants
BREAK_ROOM_NAME = "BreakRoom"
PATIENT_ROOM_NAME = "PatientRoom"
FEEDBACK_ROOM_NAME = "FeedbackRoom"
FEEDBACK_TYPE_BREAK_ROOM_NAME = "BreakRoomFeedback"
FEEDBACK_TYPE_PATIENT_ROOM_NAME = "PatientRoomFeedback"
DIALOGUE_INK_FILE_NAME = "dialogue.ink"
FEEDBACK_INK_FILE_NAME = "feedback.ink"
AUDIO_FOLDER_NAME = "Audio"
SCENARIO_INFORMATION_JSON_FILE_NAME = "scenario_information.json"
CHARACTER_VOICE_CONFIG_JSON_FILE_NAME = "character_voice_config.json"
MAX_DIALOGUE_TEXT_CHARACTER_COUNT = 275  # 300 / 250

# GUI Element Tags
HRSA_CCT_TOOL: str = "HRSA_CCT_TOOL"
SCENARIO_NAME_INPUT_TEXT: str = "SCENARIO_NAME_INPUT_TEXT"
SCENARIO_DESCRIPTION_INPUT_TEXT: str = "SCENARIO_DESCRIPTION_INPUT_TEXT"
CREATE_SCENARIO_INFORMATION_BUTTON: str = "CREATE_SCENARIO_INFORMATION_BUTTON"
FILE_DIALOG: str = "FILE_DIALOG"
FILE_DIALOG_FOR_DATA_FOLDER: str = "FILE_DIALOG_FOR_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER"
DATA_DIRECTORY_PATH_TEXT: str = "DATA_DIRECTORY_PATH_TEXT"

# Global Variable
data_path = ""
scenario_path = ""

def create_scenario_folders(scenario_name, scenario_information_json_object) -> None:
    global data_path, scenario_path
    # Scenario Folder
    scenario_path = os.path.join(data_path, scenario_name)
    print("scenario_path: ", scenario_path)
    os.mkdir(scenario_path)
    # Scenario Information JSON
    scenario_information_json_path = os.path.join(scenario_path, SCENARIO_INFORMATION_JSON_FILE_NAME)
    with open(scenario_information_json_path, "w") as output_file:
        output_file.write(scenario_information_json_object)
    # Break Room
    break_room_folder_path = os.path.join(scenario_path, BREAK_ROOM_NAME)
    os.mkdir(break_room_folder_path)
    audio_folder = os.path.join(break_room_folder_path, AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_folder_path, DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Patient Room
    patient_room_folder_path = os.path.join(scenario_path, PATIENT_ROOM_NAME)
    os.mkdir(patient_room_folder_path)
    audio_folder = os.path.join(patient_room_folder_path, AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_folder_path, DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Feedback Room
    feedback_room_folder_path = os.path.join(scenario_path, FEEDBACK_ROOM_NAME)
    os.mkdir(feedback_room_folder_path)
    # Break Room Feedback
    break_room_feedback_folder_path = os.path.join(feedback_room_folder_path, FEEDBACK_TYPE_BREAK_ROOM_NAME)
    os.mkdir(break_room_feedback_folder_path)
    audio_folder = os.path.join(break_room_feedback_folder_path, AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_feedback_folder_path, FEEDBACK_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Patient Room Feedback
    patient_room_feedback_folder_path = os.path.join(feedback_room_folder_path, FEEDBACK_TYPE_PATIENT_ROOM_NAME)
    os.mkdir(patient_room_feedback_folder_path)
    audio_folder = os.path.join(patient_room_feedback_folder_path, AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_feedback_folder_path, FEEDBACK_INK_FILE_NAME)
    open(file_path, 'a').close()


def callback_on_data_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global data_path
    data_path = os.path.normpath(str(app_data['file_path_name']))
    print(data_path)
    dpg.configure_item(DATA_DIRECTORY_PATH_TEXT, default_value=data_path)

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
    scenario_information = dict()
    scenario_information["name"] = scenario_name
    scenario_information["description"] = scenario_description
    scenario_information_json_object = json.dumps(scenario_information, indent=4)
    create_scenario_folders(scenario_name, scenario_information_json_object)


def main() -> None:
    dpg.create_context()
    dpg.create_viewport(title='HRSA Content Creation Tool', width=600, height=600)

    with dpg.window(label="HRSA CCT", tag=HRSA_CCT_TOOL, width=500, height=500):
        with dpg.collapsing_header(label="Choose a location to create the Data Folder", default_open=True):
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_DATA_FOLDER, height=300, width=450, directory_selector=True, show=False, callback=callback_on_data_folder_selected)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER, label="Select Data Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_DATA_FOLDER))
            dpg.add_text(tag=DATA_DIRECTORY_PATH_TEXT)
            dpg.add_separator()

        with dpg.collapsing_header(label="Create Scenario", default_open=True):
            dpg.add_input_text(tag=SCENARIO_NAME_INPUT_TEXT, label="Scenario Name", default_value="")
            dpg.add_input_text(tag=SCENARIO_DESCRIPTION_INPUT_TEXT, label="Scenario Description", multiline=True, tab_input=False)
            dpg.add_button(tag=CREATE_SCENARIO_INFORMATION_BUTTON, label="Create Scenario Folder", callback=callback_on_create_scenario_button_clicked)
            dpg.add_separator()

        with dpg.collapsing_header(label="Choose the Scenario Folder for Audio Generation", default_open=True):
            dpg.add_file_dialog(tag=audio_generation.FILE_DIALOG_FOR_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False, 
                            callback=audio_generation.callback_on_scenario_folder_selected)
            dpg.add_button(tag=audio_generation.SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, label="Select Scenario Folder",
                            callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=audio_generation.FILE_DIALOG_FOR_SCENARIO_FOLDER))
            dpg.add_text(tag=audio_generation.SCENARIO_DIRECTORY_PATH_TEXT)
            with dpg.collapsing_header(label="Configure Character Voice Settings", default_open=False):
                dpg.add_listbox(tag=audio_generation.CHARACTER_SELECT_LISTBOX, label="Choose Character", show=True, callback=audio_generation.display_character_info)
                dpg.add_listbox(tag=audio_generation.LANGUAGE_CODE_TEXT, label="Language Code")
                dpg.add_listbox(tag=audio_generation.AUDIO_GENDER_TEXT, label="Gender")
                dpg.add_listbox(tag=audio_generation.AUDIO_VOICE_LIST, label="Voice")
                dpg.add_button(tag=audio_generation.SAVE_AUDIO_SETTINGS_BUTTON, label="Save voice settings", show=True, callback=audio_generation.save_audio_settings)
            dpg.add_button(tag=audio_generation.GENERATE_AUDIO_BUTTON, label="Generate Audio", show=False, callback=audio_generation.callback_on_generate_audio_clicked)
            dpg.add_separator()

        with dpg.collapsing_header(label="Choose a location to create the Translated Data Folder", default_open=True):
            dpg.add_file_dialog(tag=translate.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False, 
                            callback=translate.callback_on_source_scenario_folder_selected)
            dpg.add_button(tag=translate.SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER, label="Select Source Scenario Folder",
                            callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=translate.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER))
            dpg.add_text(label="Source", tag=translate.SOURCE_SCENARIO_DIRECTORY_PATH_TEXT)
            dpg.add_text(label="Destination", tag=translate.NEW_DATA_DIRECTORY_PATH_TEXT)
            dpg.add_listbox(tag=translate.LANGUAGE_LISTBOX, label="Language", items=audio_generation.language_list, callback=translate.set_new_language_code, show=False)
            dpg.add_button(tag=translate.TRANSLATE_TEXT_BUTTON, label="Translate Data", show=False, callback=translate.callback_on_translate_text_clicked)
            dpg.add_separator()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(HRSA_CCT_TOOL, True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
