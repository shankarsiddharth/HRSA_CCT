import dearpygui.dearpygui as dpg
import json
import os
from google.oauth2 import service_account
from google.cloud import texttospeech

# Google Cloud Configuration Data
# Get Credentials from JSON file
credentials = service_account.Credentials.from_service_account_file("./decent-lambda-354120-0d9c66891965.json")
# Instantiates a client
client = texttospeech.TextToSpeechClient(credentials=credentials)


# GUI Element Tags
HRSA_CCT_TOOL: str = "HRSA_CCT_TOOL"
SCENARIO_NAME_INPUT_TEXT: str = "SCENARIO_NAME_INPUT_TEXT"
SCENARIO_DESCRIPTION_INPUT_TEXT: str = "SCENARIO_DESCRIPTION_INPUT_TEXT"
CREATE_SCENARIO_INFORMATION_BUTTON: str = "CREATE_SCENARIO_INFORMATION_BUTTON"
FILE_DIALOG: str = "FILE_DIALOG"
FILE_DIALOG_FOR_DATA_FOLDER: str = "FILE_DIALOG_FOR_DATA_FOLDER"
FILE_DIALOG_FOR_SCENARIO_FOLDER: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER"
DATA_DIRECTORY_PATH_TEXT: str = "DATA_DIRECTORY_PATH_TEXT"
SCENARIO_DIRECTORY_PATH_TEXT: str = "SCENARIO_DIRECTORY_PATH_TEXT"
GENERATE_AUDIO_BUTTON: str = "GENERATE_AUDIO_BUTTON"

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
    scenario_information_json_path = os.path.join(scenario_path, "scenario_information.json")
    with open(scenario_information_json_path, "w") as output_file:
        output_file.write(scenario_information_json_object)
    # Break Room
    break_room_folder_path = os.path.join(scenario_path, "BreakRoom")
    os.mkdir(break_room_folder_path)
    audio_folder = os.path.join(break_room_folder_path, "Audio")
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_folder_path, "dialogue.ink")
    open(file_path, 'a').close()
    # Patient Room
    patient_room_folder_path = os.path.join(scenario_path, "PatientRoom")
    os.mkdir(patient_room_folder_path)
    audio_folder = os.path.join(patient_room_folder_path, "Audio")
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_folder_path, "dialogue.ink")
    open(file_path, 'a').close()
    # Feedback Room
    feedback_room_folder_path = os.path.join(scenario_path, "FeedbackRoom")
    os.mkdir(feedback_room_folder_path)
    # Break Room Feedback
    break_room_feedback_folder_path = os.path.join(feedback_room_folder_path, "BreakRoomFeedback")
    os.mkdir(break_room_feedback_folder_path)
    audio_folder = os.path.join(break_room_feedback_folder_path, "Audio")
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_feedback_folder_path, "feedback.ink")
    open(file_path, 'a').close()
    # Patient Room Feedback
    patient_room_feedback_folder_path = os.path.join(feedback_room_folder_path, "PatientRoomFeedback")
    os.mkdir(patient_room_feedback_folder_path)
    audio_folder = os.path.join(patient_room_feedback_folder_path, "Audio")
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_feedback_folder_path, "feedback.ink")
    open(file_path, 'a').close()


def callback_on_data_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global data_path
    data_path = os.path.normpath(str(app_data['file_path_name']))
    print(data_path)
    dpg.configure_item(DATA_DIRECTORY_PATH_TEXT, default_value=data_path)


def callback_on_scenario_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global scenario_path
    scenario_path = os.path.normpath(str(app_data['file_path_name']))
    print(scenario_path)
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT, default_value=scenario_path)
    dpg.configure_item(GENERATE_AUDIO_BUTTON, show=True)


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


def callback_on_generate_audio_clicked():
    # Read Break Room Dialogue Ink Script
    break_room_folder_path = os.path.join(scenario_path, "BreakRoom")
    print(break_room_folder_path)
    audio_folder = os.path.join(break_room_folder_path, "Audio")
    print(audio_folder)
    file_path = os.path.join(break_room_folder_path, "dialogue.ink")
    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        for line in lines:
            string_to_parse = line.strip()
            if not string_to_parse:
                continue
            elif string_to_parse.startswith("->"):
                continue
            elif string_to_parse.startswith("*"):
                continue
            elif string_to_parse.startswith("==="):
                continue
            else:
                print(string_to_parse)
                string_without_name = string_to_parse.split(":")
                # TODO: Error Check for all the string operations
                split_1 = string_without_name[1].split("\"")
                dialogue_string = split_1[1].strip()
                split_3 = split_1[2].strip()
                split_4 = split_3.split("#")
                audio_file_name = split_4[1].strip()
                audio_file_name_with_extension = audio_file_name + ".mp3"
                print("Dialogue Text: ", dialogue_string)
                print("Audio File Name: ", audio_file_name)
                audio_file_path = os.path.join(audio_folder, audio_file_name_with_extension)
                print(audio_file_path)
                generate_wavenet(dialogue_string, audio_file_path)


def generate_wavenet(dialogue_text, audio_file_path):
    # TODO: Handle Network Exceptions
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=dialogue_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="en-US-Wavenet-D"
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    print("Sending Google Cloud TTS Request....")
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(audio_file_path, "wb") as output_audio_file:
        # Write the response to the output file.
        output_audio_file.write(response.audio_content)
        print("Audio File Written : ", audio_file_path)


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
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False, callback=callback_on_scenario_folder_selected)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, label="Select Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SCENARIO_FOLDER))
            dpg.add_text(tag=SCENARIO_DIRECTORY_PATH_TEXT)
            dpg.add_button(tag=GENERATE_AUDIO_BUTTON, label="Generate Audio", show=False, callback=callback_on_generate_audio_clicked)
            dpg.add_separator()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(HRSA_CCT_TOOL, True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
