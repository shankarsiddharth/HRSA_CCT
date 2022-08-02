from google.oauth2 import service_account
from google.cloud import texttospeech
import dearpygui.dearpygui as dpg
import os
import json
import subprocess

# Google Cloud Configuration Data
# Get Credentials from JSON file
credentials = service_account.Credentials.from_service_account_file("./decent-lambda-354120-0d9c66891965.json")
# Instantiates a client
client = texttospeech.TextToSpeechClient(credentials=credentials)

scenario_path_audio = ""
room_dialogue_data = dict()
character_voice_config_data = dict()
ink_file_path_list = []

# Constants
SCENARIO_DIRECTORY_PATH_TEXT: str = "SCENARIO_DIRECTORY_PATH_TEXT"
GENERATE_AUDIO_BUTTON: str = "GENERATE_AUDIO_BUTTON"
FILE_DIALOG_FOR_SCENARIO_FOLDER: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER"
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

def callback_on_scenario_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global scenario_path_audio
    scenario_path_audio = os.path.normpath(str(app_data['file_path_name']))
    print(scenario_path_audio)
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT, default_value=scenario_path_audio)
    dpg.configure_item(GENERATE_AUDIO_BUTTON, show=True)

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
    generate_audio(path=scenario_path_audio)

def generate_audio(path=""):
    # Check for the Voice Configuration File
    global scenario_path_audio, character_voice_config_data
    scenario_path_audio = path
    character_voice_config_file_path = os.path.join(scenario_path_audio, CHARACTER_VOICE_CONFIG_JSON_FILE_NAME)
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
    room_folder_path = os.path.join(scenario_path_audio, room_name)
    audio_folder_path = os.path.join(room_folder_path, AUDIO_FOLDER_NAME)
    print(audio_folder_path)
    file_path = os.path.join(room_folder_path, DIALOGUE_INK_FILE_NAME)
    print(file_path)
    parse_ink_script(audio_folder_path, file_path, room_name)
    ink_file_path_list.append(file_path)


def process_feedback_ink_file_for_room(feedback_room_type):
    global ink_file_path_list
    feedback_folder_path = os.path.join(scenario_path_audio, FEEDBACK_ROOM_NAME)
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