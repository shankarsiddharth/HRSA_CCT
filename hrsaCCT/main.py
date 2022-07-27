from email.policy import default
import os
import json
import subprocess
from unicodedata import name
import dearpygui.dearpygui as dpg
from google.oauth2 import service_account
from google.cloud import texttospeech
from google.cloud import translate
from shutil import copytree, ignore_patterns
import re

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

# Google Cloud Configuration Data
# Get Credentials from JSON file
credentials = service_account.Credentials.from_service_account_file("./decent-lambda-354120-0d9c66891965.json")
# Instantiates a client
client = texttospeech.TextToSpeechClient(credentials=credentials)
clientTranslate = translate.TranslationServiceClient(credentials=credentials)

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
FILE_DIALOG_FOR_NEW_DATA_FOLDER: str = "FILE_DIALOG_FOR_NEW_DATA_FOLDER"
FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER: str = "FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_NEW_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_NEW_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER"
NEW_DATA_DIRECTORY_PATH_TEXT: str = "NEW_DATA_DIRECTORY_PATH_TEXT"
SOURCE_SCENARIO_DIRECTORY_PATH_TEXT: str = "SOURCE_SCENARIO_DIRECTORY_PATH_TEXT"
TRANSLATE_TEXT_BUTTON: str = "TRANSLATE_TEXT_BUTTON"
LANGUAGE_LISTBOX: str = "LANGUAGE_LISTBOX"

# Global Variable
data_path = ""
scenario_path = ""
room_dialogue_data = dict()
character_voice_config_data = dict()
ink_file_path_list = []
new_data_path = ""
source_scenario_path = ""
selected_language = "es"
regStr = '\".*?\"'
new_language_code = ""
new_data_path_language_code = ""
language_list = [
    'en-US',
    'es'
]


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


def generate_audio_files():
    global room_dialogue_data, character_voice_config_data
    # Break Room Audio Generation
    audio_dialogue_data = room_dialogue_data[BREAK_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)
    # Patient Room Audio Generation
    audio_dialogue_data = room_dialogue_data[PATIENT_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)
    # Feedback Break Room Audio Generation
    audio_dialogue_data = room_dialogue_data[FEEDBACK_TYPE_BREAK_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)
    # Feedback Patient Room Audio Generation
    audio_dialogue_data = room_dialogue_data[FEEDBACK_TYPE_PATIENT_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)


def generate_audio_files_for_room(audio_dialogue_data):
    global character_voice_config_data
    for dict_key in audio_dialogue_data:
        dialogue_data = audio_dialogue_data[dict_key]
        character_type = dialogue_data["character_type"].lower()
        character_voice_config = character_voice_config_data[character_type]
        gender_text = character_voice_config["gender"].upper()
        generate_audio_gc_tts(dialogue_data["dialogue_text"],
                              dialogue_data["output_audio_file_path"],
                              character_voice_config["language_code"],
                              gender_text,
                              character_voice_config["voice_name"])


def compile_ink_files():
    global ink_file_path_list
    for ink_file_path in ink_file_path_list:
        splitext_data = os.path.splitext(ink_file_path)
        json_file_path = splitext_data[0] + ".json"
        # TODO: Get Proper Path of this executable when packaging this program as .exe
        inklecate_windows = "./inklecate_windows/inklecate.exe"
        cmd_string = inklecate_windows + " -o" + " " + json_file_path + " " + ink_file_path
        completed_process_result = subprocess.run([inklecate_windows, "-o", json_file_path, ink_file_path],
                                                  capture_output=True, text=True)
        print("cmd_string: ", cmd_string)
        print("stdout: ", completed_process_result.stdout)
        print("stderr: ", completed_process_result.stderr)
        print("check_returncode: ", completed_process_result.check_returncode())


def callback_on_generate_audio_clicked():
    # Check for the Voice Configuration File
    global scenario_path, character_voice_config_data
    character_voice_config_file_path = os.path.join(scenario_path, CHARACTER_VOICE_CONFIG_JSON_FILE_NAME)
    with open(character_voice_config_file_path, 'r', encoding='UTF-8') as json_file:
        character_voice_config_data = json.load(json_file)
    global room_dialogue_data
    room_dialogue_data = dict()
    # Process Break Room Dialogue Ink Script
    process_dialogue_ink_file_for_room(BREAK_ROOM_NAME)
    # Process Patient Room Dialogue Ink Script
    process_dialogue_ink_file_for_room(PATIENT_ROOM_NAME)
    # Process Break Room Feedback Ink Script
    process_feedback_ink_file_for_room(FEEDBACK_TYPE_BREAK_ROOM_NAME)
    # Process Patient Room Feedback Ink Script
    process_feedback_ink_file_for_room(FEEDBACK_TYPE_PATIENT_ROOM_NAME)
    print(room_dialogue_data)
    json_object = json.dumps(room_dialogue_data)
    print(json_object)
    # Compile all ink files to JSON
    compile_ink_files()
    # Process For Audio Generation
    generate_audio_files()


def process_dialogue_ink_file_for_room(room_name):
    global ink_file_path_list
    room_folder_path = os.path.join(scenario_path, room_name)
    audio_folder_path = os.path.join(room_folder_path, AUDIO_FOLDER_NAME)
    print(audio_folder_path)
    file_path = os.path.join(room_folder_path, DIALOGUE_INK_FILE_NAME)
    parse_ink_script(audio_folder_path, file_path, room_name)
    ink_file_path_list.append(file_path)


def process_feedback_ink_file_for_room(feedback_room_type):
    global ink_file_path_list
    feedback_folder_path = os.path.join(scenario_path, FEEDBACK_ROOM_NAME)
    room_folder_path = os.path.join(feedback_folder_path, feedback_room_type)
    audio_folder_path = os.path.join(room_folder_path, AUDIO_FOLDER_NAME)
    print(audio_folder_path)
    file_path = os.path.join(room_folder_path, FEEDBACK_INK_FILE_NAME)
    parse_ink_script(audio_folder_path, file_path, feedback_room_type)
    ink_file_path_list.append(file_path)


def parse_ink_script(audio_folder_path, file_path, room_name):
    global room_dialogue_data
    audio_dialogue_data = dict()
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
                print("string_to_parse: ", string_to_parse)
                text_to_display = string_to_parse.split("#")[0].strip()
                # TODO: Check the length of the dialogue text and display error to the user
                if len(text_to_display) > MAX_DIALOGUE_TEXT_CHARACTER_COUNT:
                    # TODO: Display error message by collecting this error data in a collection and display in the end
                    continue
                string_without_name = string_to_parse.split(":", 1)
                print("string_without_name: ", string_without_name)
                # TODO: Error Check for all the string operations
                split_1 = string_without_name[1].split("\"")
                print("split_1: ", split_1)
                dialogue_string = split_1[1].strip()
                print("dialogue_string: ", dialogue_string)
                split_3 = split_1[2].strip()
                print("split_3: ", split_3)
                split_4 = split_3.split("#")
                print("split_4: ", split_4)
                audio_file_name = split_4[1].strip()
                audio_file_name_with_extension = audio_file_name + ".mp3"
                print("Dialogue Text: ", dialogue_string)
                print("Audio File Name: ", audio_file_name)
                audio_file_path = os.path.join(audio_folder_path, audio_file_name_with_extension)
                print(audio_file_path)
                character_type = split_4[2].strip()
                # TODO: Create a Dict with audio file names as the key
                # and contains a dictionary of text, character_type, audio_file_path
                if audio_file_name in audio_dialogue_data:
                    # TODO: Error duplicate audio names
                    continue
                else:
                    dialogue_data = dict()
                    dialogue_data["dialogue_text"] = dialogue_string
                    dialogue_data["character_type"] = character_type
                    dialogue_data["output_audio_file_path"] = audio_file_path
                    audio_dialogue_data[audio_file_name] = dialogue_data
                    # TODO: Error Handling: check the character type validity and log the error
                    # For example, the BreakRoom only contains conversation between MedicalStudent & Player
                    # if there is trainer as character in the break room script then it's not valid
    room_dialogue_data[room_name] = audio_dialogue_data


def generate_audio_gc_tts(dialogue_text, audio_file_path, language_code, in_gender_text, voice_name):
    ssml_gender = texttospeech.SsmlVoiceGender.FEMALE
    if in_gender_text == "MALE":
        ssml_gender = texttospeech.SsmlVoiceGender.MALE
    elif in_gender_text == "NEUTRAL":
        ssml_gender = texttospeech.SsmlVoiceGender.NEUTRAL  # NOT Supported by Google Cloud TTS yet

    # TODO: Handle Network Exceptions
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=dialogue_text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=ssml_gender,
        name=voice_name
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

def callback_on_new_data_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global new_data_path
    new_data_path = os.path.normpath(str(app_data['file_path_name']))
    print(new_data_path)
    dpg.configure_item(NEW_DATA_DIRECTORY_PATH_TEXT, default_value=new_data_path)
    dpg.configure_item(LANGUAGE_LISTBOX, show=True)

def callback_on_source_scenario_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global source_scenario_path
    source_scenario_path = os.path.normpath(str(app_data['file_path_name']))
    print(source_scenario_path)
    dpg.configure_item(SOURCE_SCENARIO_DIRECTORY_PATH_TEXT, default_value=source_scenario_path)

def set_new_language_code(sender):
    global new_language_code
    global new_data_path
    global new_data_path_language_code
    new_language_code = dpg.get_value(sender)
    print(new_language_code)
    new_data_path_language_code = os.path.normpath(new_data_path + '/' + new_language_code)
    dpg.configure_item(NEW_DATA_DIRECTORY_PATH_TEXT, default_value=new_data_path_language_code)
    dpg.configure_item(TRANSLATE_TEXT_BUTTON, show=True)


def translate_text(text="I want to translate this text.", project_id="decent-lambda-354120", language="es"):
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"

    response = clientTranslate.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": language,
        }
    )

    for translation in response.translations:
        return translation.translated_text

def callback_on_translate_text_clicked():
    global new_data_path
    #copy directory
    print(data_path)
    print(new_data_path)
    copytree(data_path, new_data_path, ignore=ignore_patterns('*.mp3', '*.wav'))
    #find ink files
    ink_files_list = []
    for root, dirs, files in os.walk(new_data_path):
        for file in files:
            if file.endswith(".ink"):
                pathToAdd = os.path.join(root, file)
                ink_files_list.append(pathToAdd)
                print(pathToAdd)
    #translate
    dialogueList = []
    for newFilePath in ink_files_list:
        file_ink = open(newFilePath, 'r+')
        lines = file_ink.readlines()
        for line in lines:
            dialogue = re.search(regStr, line)
            if dialogue:
                dialogueCheck = dialogue.group(0).replace('"', '')
                if dialogueCheck not in dialogueList:
                    dialogueList.append(dialogueCheck)

        file_ink.seek(0,0)
        data = file_ink.read()
        #print(data) 
        file_ink.close()
        for dialogueItem in dialogueList:
            translatedDialogue = translate_text(text=dialogueItem, language=selected_language)
            #print(translatedDialogue)
            data = data.replace(dialogueItem, translatedDialogue)
        with open(newFilePath, 'w', encoding='utf-8') as file:
            file.write(data)
    print ("done!")


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

        with dpg.collapsing_header(label="Choose a location to create the Translated Data Folder", default_open=True):
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False, callback=callback_on_source_scenario_folder_selected)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER, label="Select Source Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER))
            dpg.add_text(tag=SOURCE_SCENARIO_DIRECTORY_PATH_TEXT)
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_NEW_DATA_FOLDER, height=300, width=450, directory_selector=True, show=False, callback=callback_on_new_data_folder_selected)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_NEW_DATA_FOLDER, label="Select new location for Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_NEW_DATA_FOLDER))
            dpg.add_text(tag=NEW_DATA_DIRECTORY_PATH_TEXT)
            dpg.add_listbox(tag=LANGUAGE_LISTBOX, label="Language", items=language_list, callback=set_new_language_code, show=False)
            dpg.add_button(tag=TRANSLATE_TEXT_BUTTON, label="Translate Data", show=False, callback=callback_on_translate_text_clicked)
            dpg.add_separator()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window(HRSA_CCT_TOOL, True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
