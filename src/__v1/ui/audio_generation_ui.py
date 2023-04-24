import copy
import json
import os
import re
import subprocess
import sys

import dearpygui.dearpygui as dpg
from google.cloud import texttospeech
from google.cloud.texttospeech_v1 import ListVoicesResponse
from google.oauth2 import service_account

from __v1 import hrsa_cct_config, cct_ui_panels, cct_advanced_options_ui
from __v1 import hrsa_cct_constants
from __v1 import hrsa_cct_globals
from __v1.hrsa_cct_globals import log, hfsc, hfs

voices = ListVoicesResponse()
client = None
is_credentials_initialized = False

def initialize_audio_generation():
    global voices, client, is_credentials_initialized
    # Google Cloud Configuration Data
    # Get Credentials from JSON file
    if hrsa_cct_config.is_google_cloud_credentials_file_found():
        try:
            path_string = os.path.abspath(hrsa_cct_config.get_google_cloud_credentials_file_path())
            credentials = service_account.Credentials.from_service_account_file(path_string)
            # Instantiates a client
            client = texttospeech.TextToSpeechClient(credentials=credentials)
            # TODO: Error Handling / Add a function and a function call to cache the data from service on each application run
            voices = client.list_voices()
            log.success("Google Credentials Initialized Successfully.")
            is_credentials_initialized = True
        except Exception as e:
            is_credentials_initialized = False
            log.error(str(e))
            if "401" in str(e):
                log.error("Error while initializing Google Cloud Text-to-Speech Client: - Please check if the Google Cloud Credentials JSON file is valid")
            elif "503" in str(e):
                log.error("Error while initializing Google Cloud Translate: Please check your internet connection.")
                log.error("Also, make sure that the firewall is not blocking the connection to Google Cloud APIs.")
            else:
                log.error("Error while initializing Google Cloud Text-to-Speech Client: Please check your Google Cloud credentials JSON file.")


scenario_language_code_folder_path = ""
scenario_path_root = ""
room_dialogue_data = dict()
character_voice_config_data = dict()
new_character_voice_config_data = dict()
character_voice_config_file_path = ""
ink_file_path_list = list()
audio_folder_path_list = list()
# TODO: Move this into a global constant
gender_list = ["MALE", "FEMALE"]
voice_list = list()

is_parsing_successful: bool = False
is_audio_generation_successful: bool = False
total_characters_for_audio_generation = 0

# GUI Element Tags
GENERATE_AUDIO_BUTTON: str = "GENERATE_AUDIO_BUTTON"
PARSE_INK_SCRIPTS_BUTTON: str = "PARSE_INK_SCRIPTS_BUTTON"
COMPILE_INK_SCRIPTS_BUTTON: str = "COMPILE_INK_SCRIPTS_BUTTON"
SAVE_AUDIO_SETTINGS_BUTTON: str = "CONFIGURE_AUDIO_BUTTON"
# CHARACTER_SELECT_LISTBOX: str = "CHARACTER_SELECT_LISTBOX"
# LANGUAGE_CODE_TEXT: str = "LANGUAGE_CODE_TEXT"
# AUDIO_GENDER_TEXT: str = "AUDIO_GENDER_TEXT"
# AUDIO_VOICE_LIST: str = "AUDIO_VOICE_LIST"
FILE_DIALOG_FOR_SCENARIO_FOLDER: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER"
AG_LANGUAGE_LISTBOX_GROUP: str = "AG_LANGUAGE_LISTBOX_GROUP"
AG_LANGUAGE_LISTBOX: str = "AG_LANGUAGE_LISTBOX"
AG_SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT: str = "AG_SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT"
VOICE_CONFIG_SECTION: str = "VOICE_CONFIG_SECTION"

AG_PLAYER_TITLE_GROUP: str = "AG_PLAYER_TITLE_GROUP"
AG_PLAYER_VOICE_CONFIGURATION_GROUP: str = "AG_PLAYER_VOICE_CONFIGURATION_GROUP"
AG_MEDICAL_STUDENT_TITLE_GROUP: str = "AG_MEDICAL_STUDENT_TITLE_GROUP"
AG_MEDICAL_STUDENT_VOICE_CONFIGURATION_GROUP: str = "AG_MEDICAL_STUDENT_VOICE_CONFIGURATION_GROUP"
AG_PATIENT_TITLE_GROUP: str = "AG_PATIENT_TITLE_GROUP"
AG_PATIENT_VOICE_CONFIGURATION_GROUP: str = "AG_PATIENT_VOICE_CONFIGURATION_GROUP"
AG_TRAINER_TITLE_GROUP: str = "AG_TRAINER_TITLE_GROUP"
AG_TRAINER_VOICE_CONFIGURATION_GROUP: str = "AG_TRAINER_VOICE_CONFIGURATION_GROUP"

AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE: str = "language code"
AG_VOICE_CONFIG_UI_SECTION_GENDER: str = "gender"
AG_VOICE_CONFIG_UI_SECTION_VOICE: str = "voice"


def _get_character_voice_config_ui_tag(character: str, section: str, ui_type: str):
    ui_obj_tag = "AG_{0}_{1}_{2}".format(character, section, ui_type).upper().replace(" ", "_")
    # print(ui_obj_tag)
    return ui_obj_tag


# region Show Advanced Options
def on_advanced_options_button_clicked(should_show_advanced_options):
    if should_show_advanced_options:
        if dpg.get_item_configuration(GENERATE_AUDIO_BUTTON)['show']:
            dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=True)
    else:
        dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=False)


cct_advanced_options_ui.add_advanced_options_delegate(on_advanced_options_button_clicked)


# endregion Show Advanced Options

def callback_on_scenario_folder_selected(sender, app_data):
    folder_language_list = list()
    global scenario_path_root
    scenario_path_root = os.path.normpath(str(app_data['file_path_name']))
    dpg.configure_item(cct_advanced_options_ui.AG_SCENARIO_DIRECTORY_PATH_TEXT, default_value=scenario_path_root)
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
    log.trace("Selected Scenario Folder for Audio Generation: " + scenario_path_root)


def callback_on_language_code_selected(sender):
    selected_language_code = dpg.get_value(AG_LANGUAGE_LISTBOX)
    if selected_language_code.casefold() != hrsa_cct_globals.none_language_code:
        global scenario_language_code_folder_path
        scenario_language_code_folder_path = os.path.join(scenario_path_root, selected_language_code)
        log.debug("scenario_path_audio: " + scenario_language_code_folder_path)
        global character_voice_config_data, character_voice_config_file_path
        character_voice_config_file_path = os.path.join(scenario_language_code_folder_path, hrsa_cct_constants.CHARACTER_VOICE_CONFIG_JSON_FILE_NAME)
        log.debug("character_voice_config_file_path: " + character_voice_config_file_path)
        with open(character_voice_config_file_path, 'r', encoding='UTF-8') as json_file:
            character_voice_config_data = json.load(json_file)
            global new_character_voice_config_data
            new_character_voice_config_data = copy.deepcopy(character_voice_config_data)
            log.debug("character_voice_config_data : " + str(character_voice_config_data))
        dpg.configure_item(AG_SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, default_value=scenario_language_code_folder_path)
        dpg.configure_item(AG_SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, show=True)
        new_button_label = "Generate Audio (" + selected_language_code + ")"
        dpg.configure_item(GENERATE_AUDIO_BUTTON, label=new_button_label)
        dpg.configure_item(PARSE_INK_SCRIPTS_BUTTON, show=True)
        dpg.configure_item(GENERATE_AUDIO_BUTTON, show=True)
        if hrsa_cct_globals.show_advanced_options:
            dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=True)
        # TODO: Voice Configuration
        # selected_character = dpg.get_value(CHARACTER_SELECT_LISTBOX)
        dpg.configure_item(VOICE_CONFIG_SECTION, show=True)
        character_list = list(character_voice_config_data.keys())
        if len(character_list) >= 1:
            if 'version' in character_list:
                character_list.remove('version')

            for character_name in character_list:
                # print("display_character_info {0}".format(character_name))
                display_character_info(character_name)
                dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, 'list'), items=gender_list)
                dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, 'list'),
                                   items=hrsa_cct_globals.audio_generation_language_list)
            # display_character_info(CHARACTER_SELECT_LISTBOX)
        else:
            # TODO: Log Error
            pass
        log.trace("Selected Language for Audio Generation: " + selected_language_code)
    else:
        dpg.configure_item(AG_SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, default_value="")
        dpg.configure_item(AG_SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, show=False)
        dpg.configure_item(PARSE_INK_SCRIPTS_BUTTON, show=False)
        dpg.configure_item(GENERATE_AUDIO_BUTTON, show=False)
        dpg.configure_item(VOICE_CONFIG_SECTION, show=False)
        if hrsa_cct_globals.show_advanced_options:
            dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=False)
        log.trace("Selected Language for Audio Generation: " + selected_language_code)


def callback_on_change_language_code(sender, app_data, user_data):
    character_name = user_data["node"]
    selected_language_code = dpg.get_value(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"))
    selected_character_gender = dpg.get_value(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"))
    if str(selected_language_code).lower() != str(hrsa_cct_globals.none_language_code).lower():
        voice_list.clear()
        global voices
        for voice in voices.voices:
            for language_code in voice.language_codes:
                if str(selected_language_code).lower() == str(language_code).lower():
                    ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)
                    if str(ssml_gender.name).upper() == str(selected_character_gender).upper():
                        voice_list.append(voice.name)
                else:
                    # TODO: Log Error
                    pass
        if len(voice_list) >= 1:
            dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), items=voice_list, default_value=voice_list[0])
        dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"), show=True)
        dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), show=True)
        dpg.configure_item(SAVE_AUDIO_SETTINGS_BUTTON, show=True)
        dpg.configure_item(PARSE_INK_SCRIPTS_BUTTON, show=True)
        dpg.configure_item(GENERATE_AUDIO_BUTTON, show=True)
        if hrsa_cct_globals.show_advanced_options:
            dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=True)
    else:
        # TODO: Handle (none) case
        dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"), show=False)
        dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), show=False)
        dpg.configure_item(SAVE_AUDIO_SETTINGS_BUTTON, show=False)
        dpg.configure_item(PARSE_INK_SCRIPTS_BUTTON, show=False)
        dpg.configure_item(GENERATE_AUDIO_BUTTON, show=False)
        if hrsa_cct_globals.show_advanced_options:
            dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=False)


def callback_on_gender_selected(sender, app_data, user_data):
    character_name = user_data["node"]
    character_language_code = dpg.get_value(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"))
    character_gender = dpg.get_value(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"))
    global voice_list
    voice_list.clear()
    global voices
    for voice in voices.voices:
        for language_code in voice.language_codes:
            if str(language_code).lower() == str(character_language_code).lower():
                ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)
                if str(ssml_gender.name).upper() == str(character_gender).upper():
                    voice_list.append(voice.name)
    if len(voice_list) >= 1:
        dpg.configure_item(_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), items=voice_list, default_value=voice_list[0])
    pass


def display_character_info(selected_character):
    global character_voice_config_data
    character_data = character_voice_config_data[selected_character]
    dpg.set_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "text"), character_data["language_code"])
    dpg.set_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_GENDER, "text"), character_data["gender"])
    dpg.set_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_VOICE, "text"), character_data["voice_name"])

    dpg.configure_item(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"), default_value=character_data["language_code"])
    dpg.configure_item(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"), default_value=character_data["gender"])
    character_language_code = character_data["language_code"]
    global voice_list
    voice_list.clear()
    global voices
    for voice in voices.voices:
        for language_code in voice.language_codes:
            if str(language_code).lower() == str(character_language_code).lower():
                ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender)
                if str(ssml_gender.name).upper() == str(character_data["gender"]).upper():
                    voice_list.append(voice.name)
    dpg.configure_item(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), items=voice_list,
                       default_value=character_data["voice_name"])
    dpg.configure_item(SAVE_AUDIO_SETTINGS_BUTTON, show=True)
    dpg.configure_item(PARSE_INK_SCRIPTS_BUTTON, show=True)
    dpg.configure_item(GENERATE_AUDIO_BUTTON, show=True)
    if hrsa_cct_globals.show_advanced_options:
        dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=True)


def save_audio_settings(sender):
    for selected_character in ["player", "medicalstudent", "trainer", "patient"]:
        language_code = dpg.get_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"))
        audio_gender = dpg.get_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"))
        voice_model = dpg.get_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"))

        dpg.set_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "text"), language_code)
        dpg.set_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_GENDER, "text"), audio_gender)
        dpg.set_value(_get_character_voice_config_ui_tag(selected_character, AG_VOICE_CONFIG_UI_SECTION_VOICE, "text"), voice_model)
        global character_voice_config_data, new_character_voice_config_data
        if str(language_code).lower() != str(hrsa_cct_globals.none_language_code).lower():
            new_character_voice_config_data[selected_character]['language_code'] = language_code
            new_character_voice_config_data[selected_character]['gender'] = audio_gender
            new_character_voice_config_data[selected_character]['voice_name'] = voice_model
            log.debug("character_voice_config_data : " + str(character_voice_config_data))
            log.debug("new_character_voice_config_data : " + str(new_character_voice_config_data))
            character_voice_config_json_object = json.dumps(new_character_voice_config_data, indent=4)
            global character_voice_config_file_path
            with open(character_voice_config_file_path, 'w') as output_json_file:
                output_json_file.write(character_voice_config_json_object)
            character_voice_config_data = new_character_voice_config_data
            log.success("Voice Configuration for Audio Generation Saved")
        else:
            # TODO: Log Error
            pass


def generate_audio_files():
    global room_dialogue_data, character_voice_config_data
    global is_audio_generation_successful
    is_audio_generation_successful = True
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
    if is_audio_generation_successful:
        log.trace('Audio Generation process Completed')


def generate_audio_files_for_room(audio_dialogue_data):
    global character_voice_config_data
    for dict_key in audio_dialogue_data:
        dialogue_data = audio_dialogue_data[dict_key]
        character_type = dialogue_data["character_type"].lower()
        character_voice_config = character_voice_config_data[character_type]
        gender_text = character_voice_config["gender"].upper()
        global total_characters_for_audio_generation
        total_characters_for_audio_generation = total_characters_for_audio_generation + len(dialogue_data["dialogue_text"])
        if hrsa_cct_globals.connect_to_cloud:
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
        bin_folder = hfs.get_default_binary_folder_path()
        inklecate_windows_path = os.path.join(bin_folder, hfsc.BINARY_INKLECATE_FOLDER_NAME, hfsc.WINDOWS_BINARY_FOLDER_NAME, hfsc.DEFAULT_WINDOWS_INKLECATE_EXECUTABLE_FILE_NAME)
        cmd_string = inklecate_windows_path + " -o" + " " + json_file_path + " " + ink_file_path
        completed_process_result = subprocess.run([inklecate_windows_path, "-o", json_file_path, ink_file_path],
                                                  capture_output=True, text=True)
        log.trace("cmd_string: " + cmd_string)
        log.trace("stdout: " + completed_process_result.stdout)
        log.trace("stderr: " + completed_process_result.stderr)
        log.trace("returncode: " + str(completed_process_result.returncode))


def callback_on_parse_ink_scripts_clicked():
    global scenario_language_code_folder_path
    global is_parsing_successful
    is_parsing_successful = True
    log.clear_log()
    parse_all_ink_scripts(path=scenario_language_code_folder_path)
    if is_parsing_successful:
        log.clear_log()
        log.success("Ink Files Check Successful.")
    else:
        log.error("Ink Files Check Failed. Please see the logs above for more details.")


def callback_on_compile_ink_scripts_clicked():
    # Compile all ink files to JSON
    compile_ink_files()
    log.trace('Complete - compile_ink_files')
    log.success("Ink Files Compilation Successful.")


def validate_audio_files() -> bool:
    global audio_folder_path_list, ink_file_path_list
    for index, audio_folder_path in enumerate(audio_folder_path_list):
        total_audio_files = len([name for name in os.listdir(audio_folder_path) if (os.path.isfile(os.path.join(audio_folder_path, name)) and name.endswith('.mp3'))])
        regex = r"#Audio_*"
        with open(ink_file_path_list[index], "r", encoding="utf-8") as f:
            test_str = f.read()
        matches = re.finditer(regex, test_str, re.MULTILINE)
        total_matches_sum = sum(1 for _ in matches)
        if total_audio_files != total_matches_sum:
            log.error("Total Audio Files: " + str(total_audio_files))
            log.error("Total Ink Audio Tags: " + str(total_matches_sum))
            log.error("Audio Files and Ink Audio Tags do not match")
            log.error("Audio Folder Path: " + audio_folder_path)
            log.error("Ink File Path: " + ink_file_path_list[index])
            log.error("Please check the Ink file and Audio Folder Path")
            return False
        else:
            log.info("Verified Number of Audio Files and Ink Audio Tags")
            return True


def callback_on_generate_audio_clicked():
    global is_audio_generation_successful
    # Check for the Voice Configuration File
    dpg.configure_item(PARSE_INK_SCRIPTS_BUTTON, show=False)
    dpg.configure_item(GENERATE_AUDIO_BUTTON, show=False)
    if hrsa_cct_globals.show_advanced_options:
        dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=False)

    # Process For Audio Generation
    callback_on_parse_ink_scripts_clicked()
    if is_parsing_successful:
        callback_on_compile_ink_scripts_clicked()
        generate_audio_files()
        if is_audio_generation_successful:
            log.info('Complete - generate_audio_files')
            log_text = "total_characters_for_audio_generation : " + str(total_characters_for_audio_generation)
            log.info(log_text)
            if hrsa_cct_globals.connect_to_cloud:
                is_audio_files_valid = validate_audio_files()
                if is_audio_files_valid:
                    log.info('Complete - validate_audio_files')
                    log.clear_log()
                    log.success('Audio Generation Completed')
                else:
                    log.error("Audio Files Check Failed.")
            else:
                log.info('Skipping Audio Validation - Not Connected to Cloud')
        else:
            log.error("=====================================================================================")
            log.error("Audio Generation Failed - Cannot Generate Audio Files for One or More Dialogue Texts")
            log.error("Please, make sure you are connected to the internet and try again.")
            log.error("If connection is not the issue, check if the Google Credentials File is valid.")
            log.error("=====================================================================================")
    else:
        log.error("Ink Files Check Failed - Cannot Generate Audio Files")

    dpg.configure_item(PARSE_INK_SCRIPTS_BUTTON, show=True)
    dpg.configure_item(GENERATE_AUDIO_BUTTON, show=True)
    if hrsa_cct_globals.show_advanced_options:
        dpg.configure_item(COMPILE_INK_SCRIPTS_BUTTON, show=True)


def parse_all_ink_scripts(path=""):
    global total_characters_for_audio_generation
    total_characters_for_audio_generation = 0
    # Check for the Voice Configuration File
    global scenario_language_code_folder_path
    scenario_language_code_folder_path = path
    global room_dialogue_data
    room_dialogue_data = dict()
    global ink_file_path_list
    ink_file_path_list.clear()
    global audio_folder_path_list
    audio_folder_path_list.clear()
    # Process Break Room Dialogue Ink Script
    log.info('Processing Break Room ink file')
    process_dialogue_ink_file_for_room(hrsa_cct_constants.BREAK_ROOM_NAME)
    log.info('Complete - Processing Break Room ink file')
    # Process Patient Room Dialogue Ink Script
    log.info('Processing Patient Room ink file')
    process_dialogue_ink_file_for_room(hrsa_cct_constants.PATIENT_ROOM_NAME)
    log.info('Complete - Processing Patient Room ink file')
    # Process Break Room Feedback Ink Script
    log.info('Processing Feedback Room - Break Room ink file')
    process_feedback_ink_file_for_room(hrsa_cct_constants.FEEDBACK_TYPE_BREAK_ROOM_NAME)
    log.info('Complete - Processing Feedback Room - Break Room ink file')
    # Process Patient Room Feedback Ink Script
    log.info('Processing Feedback Room - Patient Room ink file')
    process_feedback_ink_file_for_room(hrsa_cct_constants.FEEDBACK_TYPE_PATIENT_ROOM_NAME)
    log.info('Complete - Processing Feedback Room - Patient Room ink file')
    json_object = json.dumps(room_dialogue_data)
    log.trace("Room Dialogue Dict: " + json_object)


def process_dialogue_ink_file_for_room(room_name):
    global ink_file_path_list
    room_folder_path = os.path.join(scenario_language_code_folder_path, room_name)
    audio_folder_path = os.path.join(room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    log.debug("Audio Folder Path: " + audio_folder_path)
    file_path = os.path.join(room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    log.info("Dialogue Ink File Path: " + file_path)
    parse_ink_script(audio_folder_path, file_path, room_name)
    audio_folder_path_list.append(audio_folder_path)
    ink_file_path_list.append(file_path)


def process_feedback_ink_file_for_room(feedback_room_type):
    global ink_file_path_list
    feedback_folder_path = os.path.join(scenario_language_code_folder_path, hrsa_cct_constants.FEEDBACK_ROOM_NAME)
    room_folder_path = os.path.join(feedback_folder_path, feedback_room_type)
    audio_folder_path = os.path.join(room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    log.debug("Audio Folder Path: " + audio_folder_path)
    file_path = os.path.join(room_folder_path, hrsa_cct_constants.FEEDBACK_INK_FILE_NAME)
    log.info("Feedback Ink File Path: " + file_path)
    parse_ink_script(audio_folder_path, file_path, feedback_room_type)
    audio_folder_path_list.append(audio_folder_path)
    ink_file_path_list.append(file_path)


def parse_ink_script(audio_folder_path, file_path, room_name):
    global room_dialogue_data, is_parsing_successful
    audio_dialogue_data = dict()
    with open(file_path, 'r', encoding='UTF-8') as file:
        lines = file.readlines()
        line_number = 0
        for line in lines:
            line_number = line_number + 1
            # Log line number to Visual Logger - cutelog
            log.trace(str(line_number))
            string_to_parse = line.strip()
            if not string_to_parse:
                continue
            elif string_to_parse.startswith("==="):
                continue
            elif string_to_parse.startswith("->"):
                continue
            elif string_to_parse.startswith("*"):
                # TODO : #Highpriority Check the option string for the option letter/text
                # TODO : Throw error if it has any option characters
                # TODO : Check for valid emotion tags
                if room_name == hrsa_cct_constants.FEEDBACK_TYPE_BREAK_ROOM_NAME or room_name == hrsa_cct_constants.FEEDBACK_TYPE_PATIENT_ROOM_NAME:
                    # Check for valid feedback option
                    match_list = re.findall(hrsa_cct_globals.feedback_option_regular_expression, string_to_parse)
                    if len(match_list) != 1:
                        log_text = str(line_number) + ' : ' + 'Not a valid feedback option. ' \
                                                              'Feedback option can be in the range 1-5' \
                                                              'eg. (\'1\' \'5\')'
                        log.warning(log_text)
                else:
                    match_list = re.findall(hrsa_cct_globals.option_regular_expression, string_to_parse)
                    if len(match_list) >= 1:
                        match_group_tuple = match_list[0]
                        if len(match_group_tuple) >= 3:
                            option_text = match_group_tuple[1]
                            option_text_without_spaces = "".join(option_text.split())
                            if option_text_without_spaces.startswith(tuple(hrsa_cct_globals.option_text_prefixes)):
                                # TODO : Check for other tags
                                pass
                            else:
                                log_text = str(line_number) + ' : ' + 'Not a valid option index. ' \
                                                                      'Option index can be in the range A-E or 1-5 and should have a dot character after the index. ' \
                                                                      'eg. (\'A.\' \'E.\' \'1.\' \'5.\')'
                                log.warning(log_text)
                    else:
                        # TODO: Log Error Wrong formatting for Option text
                        # TODO: If it is a feedback room text then ignore
                        log_text = "Line Number : " + str(line_number) + ' : ' + " Wrong formatting for Option text"
                        log.warning(log_text)
                    continue
            else:
                try:
                    log.trace("string_to_parse: " + string_to_parse)
                    text_to_display = string_to_parse.split("#")[0].strip()
                    # TODO: Check the length of the dialogue text and display error to the user
                    if len(text_to_display) > hrsa_cct_constants.MAX_DIALOGUE_TEXT_CHARACTER_COUNT:
                        # TODO: Display error message by collecting this error data in a collection and display in the end
                        log_text = str(line_number) + ' : ' + 'Length exceeds max character count'
                        log.warning(log_text)
                    string_without_name = string_to_parse.split(":", 1)
                    log.trace("string_without_name: " + str(string_without_name))
                    # TODO: Error Check for all the string operations
                    split_1 = string_without_name[1].split("\"")
                    log.trace("split_1: " + str(split_1))
                    dialogue_string = split_1[1].strip()
                    log.trace("dialogue_string: " + dialogue_string)
                    split_3 = split_1[2].strip()
                    log.trace("split_3: " + str(split_3))
                    split_4 = split_3.split("#")
                    log.trace("split_4: " + str(split_4))
                    audio_file_name = split_4[1].strip()
                    audio_file_name_with_extension = audio_file_name + ".mp3"
                    log.debug("Dialogue Text: " + str(dialogue_string))
                    log.debug("Audio File Name: " + str(audio_file_name))
                    audio_file_path = os.path.join(audio_folder_path, audio_file_name_with_extension)
                    log.debug("Audio File Path: " + str(audio_file_path))
                    character_type = split_4[2].strip()
                except Exception as e:
                    log.error("---------------------------------------------------------------------------------------------------------")
                    log_text = 'Line Number : ' + str(line_number) + ' : ' + 'Error parsing ink file, ' + str(e)
                    log.error(log_text)
                    log_text = "^ Make sure the line number :" + str(line_number) + " is in the correct format"
                    log.error(log_text)
                    log_text = "^ The format is as follows:"
                    log.error(log_text)
                    log_text = "\t<Character Name> : \"<Dialogue Text>\" #<Audio File Name> #<Character Type>"
                    log.error(log_text)
                    log_text = "^ Examples are as follows:"
                    log.error(log_text)
                    log_text = "\tMedicalStudent: \"Hello, Good Morning Doctor\" #Audio_1 #MedicalStudent"
                    log.error(log_text)
                    log_text = "\tPatient: \"Hello, Good Morning Doctor\" #Audio_1 #Patient"
                    log.error(log_text)
                    log_text = "\tPlayer: \"Hello, Good Morning\" #Audio_1 #Player"
                    log.error(log_text)
                    log_text = "\tTrainer: \"You responded with a positive remark.\" #Audio_1 #Trainer #Left"
                    log.error(log_text)
                    log_text = "\tTrainer: \"You responded with a negative remark.\" #Audio_1 #Trainer #Right"
                    log.error(log_text)
                    log.error("---------------------------------------------------------------------------------------------------------")
                    is_parsing_successful = False
                    continue
                # Create a Dict with audio file names as the key
                # and contains a dictionary of text, character_type, audio_file_path
                if audio_file_name in audio_dialogue_data:
                    # TODO: Error duplicate audio names
                    log.error("---------------------------------------------------------------------------------------------------------")
                    log_text = str(line_number) + ' : ' + 'Duplicate Audio file names, ' + audio_file_name
                    log.error(log_text)
                    log.error("---------------------------------------------------------------------------------------------------------")
                    is_parsing_successful = False
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
    global is_audio_generation_successful
    # TODO: Change the 'MALE' & 'FEMALE' string check into a global constant check
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

    log.trace("Sending Google Cloud TTS Request....")
    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    try:
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # The response's audio_content is binary.
        with open(audio_file_path, "wb") as output_audio_file:
            # Write the response to the output file.
            output_audio_file.write(response.audio_content)
            log_text = "Audio File Written : " + audio_file_path
            log.info(log_text)
    except Exception as e:
        log.trace(str(e))
        log.error("---------------------------------------------------------------------------------------------------------")
        log.error("Google Cloud TTS Request Failed for the following dialogue text:")
        log.error(dialogue_text)
        log.error(audio_file_path)
        log.error("---------------------------------------------------------------------------------------------------------")
        is_audio_generation_successful = False


def callback_on_show_file_dialog_clicked(item_tag):
    dpg.configure_item(item_tag, show=True, modal=True)


def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


def init_ui():
    with dpg.collapsing_header(tag=cct_ui_panels.AUDIO_GENERATION_COLLAPSING_HEADER,
                               label="Audio Generation", default_open=False, open_on_double_click=False, open_on_arrow=False,
                               show=hrsa_cct_config.is_google_cloud_credentials_file_found()):
        dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False,
                            callback=callback_on_scenario_folder_selected,
                            default_path=hrsa_cct_config.get_file_dialog_default_path(),
                            cancel_callback=file_dialog_cancel_callback)
        dpg.add_button(tag=cct_advanced_options_ui.SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, label="Select Scenario Folder...",
                       callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SCENARIO_FOLDER))
        dpg.add_text(tag=cct_advanced_options_ui.AG_SCENARIO_DIRECTORY_PATH_TEXT)
        with dpg.group(tag=AG_LANGUAGE_LISTBOX_GROUP, horizontal=True, show=False):
            dpg.add_text("Audio Generation Language: ")
            dpg.add_listbox(tag=AG_LANGUAGE_LISTBOX, items=hrsa_cct_globals.language_list,
                            callback=callback_on_language_code_selected, default_value="")
        dpg.add_text(tag=AG_SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, show=False)
        # TODO: Voice Configuration
        with dpg.collapsing_header(indent=50, tag=VOICE_CONFIG_SECTION, label="Configure Character Voice Settings", default_open=False, show=False):
            # region Player Voice Configuration
            character_name = "Player"
            with dpg.group(tag=AG_PLAYER_TITLE_GROUP, horizontal=True, show=True):
                dpg.add_text("Player:")
                dpg.add_text("Language", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "text"), indent=100)
                dpg.add_text("Gender", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "text"), indent=260)
                dpg.add_text("Voice", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "text"), indent=460)

            with dpg.group(tag=AG_PLAYER_VOICE_CONFIGURATION_GROUP, horizontal=True, show=True, indent=40):
                dpg.add_text(AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE)
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"), width=100,
                                label='', num_items=4, callback=callback_on_change_language_code, user_data={"node": character_name})
                dpg.add_text('Gender')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"), width=100,
                                label='', num_items=3, show=True, callback=callback_on_gender_selected, user_data={"node": character_name})
                dpg.add_text('Voice')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), width=150,
                                label="", num_items=10)
            # endregion Player Voice Configuration

            # region Medical Student Voice Configuration
            character_name = "MedicalStudent"
            with dpg.group(tag=AG_MEDICAL_STUDENT_TITLE_GROUP, horizontal=True, show=True):
                dpg.add_text("MedicalStudent:")
                dpg.add_text("Language", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "text"), indent=120)
                dpg.add_text("Gender", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "text"), indent=260)
                dpg.add_text("Voice", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "text"), indent=460)
            with dpg.group(tag=AG_MEDICAL_STUDENT_VOICE_CONFIGURATION_GROUP, horizontal=True, show=True, indent=40):
                dpg.add_text(AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE)
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"), width=100,
                                label='', num_items=4, callback=callback_on_change_language_code, user_data={"node": character_name})
                dpg.add_text('Gender')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"), width=100,
                                label="", num_items=3, show=True, callback=callback_on_gender_selected, user_data={"node": character_name})
                dpg.add_text('Voice')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), width=150,
                                label="", num_items=10)
            # endregion Medical Student Voice Configuration

            # region Patient Voice Configuration
            character_name = "Patient"
            with dpg.group(tag=AG_PATIENT_TITLE_GROUP, horizontal=True, show=True):
                dpg.add_text("Patient:")
                dpg.add_text("Language", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "text"), indent=100)
                dpg.add_text("Gender", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "text"), indent=260)
                dpg.add_text("Voice", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "text"), indent=460)
            with dpg.group(tag=AG_PATIENT_VOICE_CONFIGURATION_GROUP, horizontal=True, show=True, indent=40):
                dpg.add_text(AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE)
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"), width=100,
                                label='', num_items=4, callback=callback_on_change_language_code, user_data={"node": character_name})
                dpg.add_text('Gender')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"), width=100,
                                label="", num_items=3, show=True, callback=callback_on_gender_selected, user_data={"node": character_name})
                dpg.add_text('Voice')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), width=150,
                                label="", num_items=10)
            # endregion Patient Voice Configuration

            # region Trainer Voice Configuration
            character_name = "Trainer"
            with dpg.group(tag=AG_TRAINER_TITLE_GROUP, horizontal=True, show=True):
                dpg.add_text("Trainer:")
                dpg.add_text("Language", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "text"), indent=100)
                dpg.add_text("Gender", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "text"), indent=260)
                dpg.add_text("Voice", tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "text"), indent=460)
            with dpg.group(tag=AG_TRAINER_VOICE_CONFIGURATION_GROUP, horizontal=True, show=True, indent=40):
                dpg.add_text(AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE)
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_LANGUAGE_CODE, "list"), width=100,
                                label='', num_items=4, callback=callback_on_change_language_code, user_data={"node": character_name})
                dpg.add_text('Gender')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_GENDER, "list"), width=100,
                                label="", num_items=3, show=True, callback=callback_on_gender_selected, user_data={"node": character_name})
                dpg.add_text('Voice')
                dpg.add_listbox(tag=_get_character_voice_config_ui_tag(character_name, AG_VOICE_CONFIG_UI_SECTION_VOICE, "list"), width=150,
                                label="", num_items=10)
            # endregion Trainer Voice Configuration

            dpg.add_button(tag=SAVE_AUDIO_SETTINGS_BUTTON, label="Save voice settings", show=True, callback=save_audio_settings)
        dpg.add_button(tag=PARSE_INK_SCRIPTS_BUTTON, label="Check Ink Scripts", show=False,
                       callback=callback_on_parse_ink_scripts_clicked)
        dpg.add_button(tag=COMPILE_INK_SCRIPTS_BUTTON, label="Compile Ink Scripts", show=False,
                       callback=callback_on_compile_ink_scripts_clicked)
        dpg.add_button(tag=GENERATE_AUDIO_BUTTON, label="Generate Audio", show=False, callback=callback_on_generate_audio_clicked)
        dpg.add_separator()


if sys.flags.dev_mode:
    print("audio_generation_ui.__init__()")
