from google.oauth2 import service_account
from google.cloud import texttospeech
import dearpygui.dearpygui as dpg
import os
import json
import subprocess
import copy
import hrsa_cct_constants
import hrsa_cct_globals
from hrsa_cct_globals import log

# Google Cloud Configuration Data
# Get Credentials from JSON file
credentials = service_account.Credentials.from_service_account_file("./decent-lambda-354120-0d9c66891965.json")
# Instantiates a client
client = texttospeech.TextToSpeechClient(credentials=credentials)

scenario_language_code_folder_path = ""
scenario_path_root = ""
room_dialogue_data = dict()
character_voice_config_data = dict()
ink_file_path_list = []
gender_list = ["MALE", "FEMALE"]
voice_list = []

# GUI Element Tags
SCENARIO_DIRECTORY_PATH_TEXT: str = "SCENARIO_DIRECTORY_PATH_TEXT"
GENERATE_AUDIO_BUTTON: str = "GENERATE_AUDIO_BUTTON"
SAVE_AUDIO_SETTINGS_BUTTON: str = "CONFIGURE_AUDIO_BUTTON"
CHARACTER_SELECT_LISTBOX: str = "CHARACTER_SELECT_LISTBOX"
LANGUAGE_CODE_TEXT: str = "LANGUAGE_CODE_TEXT"
AUDIO_GENDER_TEXT: str = "AUDIO_GENDER_TEXT"
AUDIO_VOICE_LIST: str = "AUDIO_VOICE_LIST"
FILE_DIALOG_FOR_SCENARIO_FOLDER: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER"
AG_LANGUAGE_LISTBOX_GROUP: str = "AG_LANGUAGE_LISTBOX_GROUP"
AG_LANGUAGE_LISTBOX: str = "AG_LANGUAGE_LISTBOX"
SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT: str = "SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT"


def callback_on_scenario_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    folder_language_list = list()
    global scenario_path_root
    scenario_path_root = os.path.normpath(str(app_data['file_path_name']))
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT, default_value=scenario_path_root)
    for file in os.listdir(scenario_path_root):
        directory_path = os.path.join(scenario_path_root, file)
        if os.path.isdir(directory_path):
            if file in hrsa_cct_globals.language_list:
                folder_language_list.append(file)
    new_language_list = copy.deepcopy(hrsa_cct_globals.language_list)
    for language_code in new_language_list:
        if language_code.casefold() == hrsa_cct_globals.none_language_code:
            continue
        if language_code not in folder_language_list:
            new_language_list.remove(language_code)

    dpg.configure_item(AG_LANGUAGE_LISTBOX, items=new_language_list)
    dpg.set_value(AG_LANGUAGE_LISTBOX, hrsa_cct_globals.none_language_code)
    callback_on_language_code_selected(AG_LANGUAGE_LISTBOX)
    dpg.configure_item(AG_LANGUAGE_LISTBOX_GROUP, show=True)


def callback_on_language_code_selected(sender):
    selected_language_code = dpg.get_value(AG_LANGUAGE_LISTBOX)
    if selected_language_code.casefold() != hrsa_cct_globals.none_language_code:
        global scenario_language_code_folder_path
        scenario_language_code_folder_path = os.path.join(scenario_path_root, selected_language_code)
        print("scenario_path_audio: ", scenario_language_code_folder_path)
        global character_voice_config_data
        character_voice_config_file_path = os.path.join(scenario_language_code_folder_path, hrsa_cct_constants.CHARACTER_VOICE_CONFIG_JSON_FILE_NAME)
        with open(character_voice_config_file_path, 'r', encoding='UTF-8') as json_file:
            character_voice_config_data = json.load(json_file)
        dpg.configure_item(SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, default_value=scenario_language_code_folder_path)
        dpg.configure_item(SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, show=True)
        new_button_label = "Generate Audio (" + selected_language_code + ")"
        dpg.configure_item(GENERATE_AUDIO_BUTTON, label=new_button_label)
        dpg.configure_item(GENERATE_AUDIO_BUTTON, show=True)
    else:
        dpg.configure_item(SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, default_value="")
        dpg.configure_item(SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, show=False)
        dpg.configure_item(GENERATE_AUDIO_BUTTON, show=False)
    # dpg.configure_item(CHARACTER_SELECT_LISTBOX, items=list(character_voice_config_data.keys()))
    # dpg.configure_item(AUDIO_GENDER_TEXT, items=gender_list)
    # dpg.configure_item(LANGUAGE_CODE_TEXT, items=language_list)


def generate_audio_files():
    global room_dialogue_data, character_voice_config_data
    # Break Room Audio Generation
    log.info('Processing Break Room Audio files')
    audio_dialogue_data = room_dialogue_data[hrsa_cct_constants.BREAK_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)
    # Patient Room Audio Generation
    log.info('Processing Patient Room Audio files')
    audio_dialogue_data = room_dialogue_data[hrsa_cct_constants.PATIENT_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)
    # Feedback Break Room Audio Generation
    log.info('Processing Feedback room - Break Room Audio files')
    audio_dialogue_data = room_dialogue_data[hrsa_cct_constants.FEEDBACK_TYPE_BREAK_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)
    # Feedback Patient Room Audio Generation
    log.info('Processing Feedback room - Patient Room Audio files')
    audio_dialogue_data = room_dialogue_data[hrsa_cct_constants.FEEDBACK_TYPE_PATIENT_ROOM_NAME]
    generate_audio_files_for_room(audio_dialogue_data)
    log.info('Audio Generation Complete')


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
    generate_audio(path=scenario_language_code_folder_path)


def generate_audio(path=""):
    # Check for the Voice Configuration File
    global scenario_language_code_folder_path
    scenario_language_code_folder_path = path
    global room_dialogue_data
    room_dialogue_data = dict()
    # Process Break Room Dialogue Ink Script
    log.info('Processing Break Room ink file')
    process_dialogue_ink_file_for_room(hrsa_cct_constants.BREAK_ROOM_NAME)
    # Process Patient Room Dialogue Ink Script
    log.info('Processing Patient Room ink file')
    process_dialogue_ink_file_for_room(hrsa_cct_constants.PATIENT_ROOM_NAME)
    # Process Break Room Feedback Ink Script
    log.info('Processing Feedback Room - Break Room ink file')
    process_feedback_ink_file_for_room(hrsa_cct_constants.FEEDBACK_TYPE_BREAK_ROOM_NAME)
    # Process Patient Room Feedback Ink Script
    log.info('Processing Feedback Room - Patient Room ink file')
    process_feedback_ink_file_for_room(hrsa_cct_constants.FEEDBACK_TYPE_PATIENT_ROOM_NAME)
    print(room_dialogue_data)
    json_object = json.dumps(room_dialogue_data)
    print(json_object)
    # Compile all ink files to JSON
    compile_ink_files()
    # Process For Audio Generation
    generate_audio_files()


def process_dialogue_ink_file_for_room(room_name):
    global ink_file_path_list
    room_folder_path = os.path.join(scenario_language_code_folder_path, room_name)
    audio_folder_path = os.path.join(room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    print(audio_folder_path)
    file_path = os.path.join(room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    print(file_path)
    parse_ink_script(audio_folder_path, file_path, room_name)
    ink_file_path_list.append(file_path)


def process_feedback_ink_file_for_room(feedback_room_type):
    global ink_file_path_list
    feedback_folder_path = os.path.join(scenario_language_code_folder_path, hrsa_cct_constants.FEEDBACK_ROOM_NAME)
    room_folder_path = os.path.join(feedback_folder_path, feedback_room_type)
    audio_folder_path = os.path.join(room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    print(audio_folder_path)
    file_path = os.path.join(room_folder_path, hrsa_cct_constants.FEEDBACK_INK_FILE_NAME)
    parse_ink_script(audio_folder_path, file_path, feedback_room_type)
    ink_file_path_list.append(file_path)


def parse_ink_script(audio_folder_path, file_path, room_name):
    global room_dialogue_data
    audio_dialogue_data = dict()
    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        line_number = 0
        for line in lines:
            line_number = line_number + 1
            # Log line number to Visual Logger - cutelog
            log.debug(line_number)
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
                if len(text_to_display) > hrsa_cct_constants.MAX_DIALOGUE_TEXT_CHARACTER_COUNT:
                    # TODO: Display error message by collecting this error data in a collection and display in the end
                    log_text = str(line_number) + ' : ' + 'Length exceeds max character count'
                    log.warning(log_text)
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
                    log_text = str(line_number) + ' : ' + 'Duplicate Audio file names, ' + audio_file_name
                    log.warning(log_text)
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
        log_text = "Audio File Written : " + audio_file_path
        print(log_text)
        log.debug(log_text)


def display_character_info(sender):
    selected_character = dpg.get_value(sender)
    character_data = character_voice_config_data[selected_character]
    dpg.configure_item(LANGUAGE_CODE_TEXT, default_value=character_data["language_code"])
    dpg.configure_item(AUDIO_GENDER_TEXT, default_value=character_data["gender"])
    voices = client.list_voices(language_code=character_data["language_code"])
    voice_list.clear()
    for voice in voices.voices:
        voice_list.append(voice.name)
    dpg.configure_item(AUDIO_VOICE_LIST, items=voice_list, default_value=character_data["voice_name"])


def save_audio_settings():
    print(character_voice_config_data)
