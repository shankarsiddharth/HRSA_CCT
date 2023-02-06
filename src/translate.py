import json
import os
import re
import shutil
import copy
import pathlib

import dearpygui.dearpygui as dpg
from google.cloud import translate
from google.oauth2 import service_account

import hrsa_cct_constants
import hrsa_cct_globals
from hrsa_cct_globals import log

credentials = service_account.Credentials.from_service_account_file(hrsa_cct_constants.GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE_PATH)
clientTranslate = translate.TranslationServiceClient(credentials=credentials)

new_data_path = ""
source_scenario_language_code_path = ""
selected_language = "es"
new_language_code = ""
new_scenario_path_language_code = ""
total_characters_translated = 0
total_characters_to_translate = 0

# GUI Element Tags
FILE_DIALOG_FOR_NEW_DATA_FOLDER: str = "FILE_DIALOG_FOR_NEW_DATA_FOLDER"
FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER: str = "FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_NEW_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_NEW_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER"
NEW_DATA_DIRECTORY_PATH_TEXT: str = "NEW_DATA_DIRECTORY_PATH_TEXT"
SOURCE_SCENARIO_DIRECTORY_PATH_TEXT: str = "SOURCE_SCENARIO_DIRECTORY_PATH_TEXT"
TRANSLATE_TEXT_BUTTON: str = "TRANSLATE_TEXT_BUTTON"
LANGUAGE_LISTBOX: str = "LANGUAGE_LISTBOX"
DESTINATION_SECTION_GROUP: str = "DESTINATION_SECTION_GROUP"
LANGUAGE_LISTBOX_GROUP: str = "LANGUAGE_LISTBOX_GROUP"
SOURCE_SECTION_GROUP: str = "SOURCE_SECTION_GROUP"


def callback_on_source_scenario_folder_selected(sender, app_data):
    log.debug("Sender: " + str(sender), False)
    log.debug("App Data: " + str(app_data), False)
    global source_scenario_language_code_path
    global new_data_path
    source_scenario_folder_path = os.path.normpath(str(app_data['file_path_name']))
    source_scenario_language_code_path = os.path.join(source_scenario_folder_path, hrsa_cct_globals.default_language_code)
    new_data_path = os.path.abspath(source_scenario_folder_path)
    log.info("source_scenario_language_code_path: " + source_scenario_language_code_path)
    new_language_list = copy.deepcopy(hrsa_cct_globals.language_list)
    if hrsa_cct_globals.default_language_code in new_language_list:
        new_language_list.remove(hrsa_cct_globals.default_language_code)
    dpg.configure_item(SOURCE_SECTION_GROUP, show=True)
    dpg.configure_item(SOURCE_SCENARIO_DIRECTORY_PATH_TEXT, default_value=source_scenario_language_code_path)
    dpg.configure_item(NEW_DATA_DIRECTORY_PATH_TEXT, default_value=new_data_path)
    dpg.configure_item(LANGUAGE_LISTBOX, items=new_language_list)
    dpg.set_value(LANGUAGE_LISTBOX, hrsa_cct_globals.none_language_code)
    set_new_language_code(LANGUAGE_LISTBOX)
    dpg.configure_item(LANGUAGE_LISTBOX_GROUP, show=True)


def set_new_language_code(sender):
    global new_language_code
    global new_data_path
    global new_scenario_path_language_code
    new_language_code = dpg.get_value(LANGUAGE_LISTBOX)
    log.info("new_language_code: " + new_language_code)
    if (new_language_code.casefold() != hrsa_cct_globals.none_language_code.casefold()) \
            and (new_language_code.casefold() != hrsa_cct_globals.default_language_code.casefold()):
        new_scenario_path_language_code = os.path.join(new_data_path, new_language_code)
        dpg.configure_item(NEW_DATA_DIRECTORY_PATH_TEXT, default_value=new_scenario_path_language_code)
        dpg.configure_item(DESTINATION_SECTION_GROUP, show=True)
        dpg.configure_item(TRANSLATE_TEXT_BUTTON, show=True)
    else:
        dpg.configure_item(DESTINATION_SECTION_GROUP, show=False)
        dpg.configure_item(TRANSLATE_TEXT_BUTTON, show=False)


def translate_text(text="I want to translate this text.", project_id="decent-lambda-354120", language="es"):
    location = "global"
    parent = f"projects/{project_id}/locations/{location}"
    log.info("Translating : " + text + " - to " + language)
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
    global total_characters_translated
    total_characters_translated = 0
    global total_characters_to_translate
    total_characters_to_translate = 0
    global new_scenario_path_language_code
    global source_scenario_language_code_path
    # Delete the directory if it exists
    new_language_dir_path = pathlib.Path(new_scenario_path_language_code)
    if new_language_dir_path.exists() and new_language_dir_path.is_dir():
        shutil.rmtree(new_language_dir_path, ignore_errors=True)
    # copy directory
    log.info("Source Language Scenario Path: " + source_scenario_language_code_path)
    log.info("New Language Scenario Path: " + new_scenario_path_language_code)
    # TODO: Add scenario_information.json once the translation functionality is complete for that file
    # TODO: add dirs_exist_ok=True to copytree and test the functionality
    # TODO: if the directory exist delete the entire directory and proceed with translation
    shutil.copytree(source_scenario_language_code_path,
                    new_scenario_path_language_code,
                    ignore=shutil.ignore_patterns('*.mp3', '*.wav',
                                                  hrsa_cct_constants.DIALOGUE_INK_JSON_FILE_NAME,
                                                  hrsa_cct_constants.FEEDBACK_INK_JSON_FILE_NAME),
                    dirs_exist_ok=True)
    # get and process the scenario information file
    scenario_information_json_path = os.path.join(new_scenario_path_language_code, hrsa_cct_constants.SCENARIO_INFORMATION_JSON_FILE_NAME)
    if os.path.exists(scenario_information_json_path):
        scenario_information_file_content = ""
        with open(scenario_information_json_path, "r", encoding="utf-8") as file:
            scenario_information_file_content = file.read()
        if len(str(scenario_information_file_content)) != 0:
            scenario_information_json = json.loads(scenario_information_file_content)
            scenario_localized_name = scenario_information_json['localized_name']
            scenario_description = scenario_information_json['description']
            scenario_detail = scenario_information_json['detail']
            # translate scenario information file
            localized_name_translated = translate_text(text=scenario_localized_name, language=selected_language)
            description_translated = translate_text(text=scenario_description, language=selected_language)
            detail_translated = translate_text(text=scenario_detail, language=selected_language)
            scenario_information_json['localized_name'] = localized_name_translated
            scenario_information_json['description'] = description_translated
            scenario_information_json['detail'] = detail_translated
            scenario_information_json_encoded = json.dumps(scenario_information_json, indent=4, ensure_ascii=False).encode("utf-8")
            scenario_information_json_decoded_string = scenario_information_json_encoded.decode()
            # save translated scenario information json file
            with open(scenario_information_json_path, "w", encoding="utf-8") as output_file:
                output_file.write(scenario_information_json_decoded_string)
        else:
            # TODO: Error log important file content missing
            pass
    else:
        # TODO: Error log important file missing
        pass
    # find ink files for translation
    ink_files_list = []
    for root, dirs, files in os.walk(new_scenario_path_language_code):
        for file in files:
            if file.endswith(".ink"):
                path_to_add = os.path.join(root, file)
                ink_files_list.append(path_to_add)
                log.trace("path_to_add: " + path_to_add, False)
    # translate ink files
    dialogue_text_list = list()
    for new_file_path in ink_files_list:
        file_ink = open(new_file_path, 'r+')
        lines = file_ink.readlines()
        for line in lines:
            line_to_process = line.strip()
            if line_to_process.startswith('*'):  # Check & process option lines
                match_list = re.findall(hrsa_cct_globals.option_regular_expression, line_to_process)
                if len(match_list) >= 1:
                    match_group_tuple = match_list[0]
                    if len(match_group_tuple) >= 3:
                        option_text = match_group_tuple[1]
                        # TODO: Remove the option characters from the options
                        option_match_list = re.findall(hrsa_cct_globals.option_display_text_regular_expression, option_text)
                        if len(option_match_list) >= 1:
                            option_text_without_option_index = option_match_list[0]
                            option_text_without_option_index = str(option_text_without_option_index).strip()
                            if option_text_without_option_index not in dialogue_text_list:
                                dialogue_text_list.append(option_text_without_option_index)
                        else:
                            # TODO: log parse error
                            pass
                        option_feedback_text = match_group_tuple[2]
                        if option_feedback_text not in dialogue_text_list:
                            dialogue_text_list.append(option_feedback_text)
                    else:
                        # TODO: log parsing error
                        pass
                else:
                    # TODO: log parsing error
                    # TODO: If it is a feedback room text then ignore
                    pass
            elif line_to_process.startswith('='):  # Ignore section headers
                pass
            elif line_to_process.startswith('->'):  # Ignore section redirection lines
                pass
            elif len(line_to_process) == 0:  # Ignore empty lines
                pass
            else:
                dialogue_text = re.search(hrsa_cct_globals.dialogue_regular_expression, line_to_process)
                if dialogue_text:
                    dialogue_check = dialogue_text.group(0).replace('"', '')
                    if dialogue_check not in dialogue_text_list:
                        dialogue_text_list.append(dialogue_check)
        # Count Characters to translate
        for dialogue_text_list_element in dialogue_text_list:
            total_characters_to_translate = total_characters_to_translate + len(dialogue_text_list_element)
        log_text = "total_characters_to_translate : " + str(total_characters_to_translate)
        log.info(log_text)
        continue
        file_ink.seek(0, 0)
        data = file_ink.read()
        # print(data)
        # log.trace(data, False)
        file_ink.close()
        for dialogue_text_list_element in dialogue_text_list:
            translated_text = translate_text(text=dialogue_text_list_element, language=selected_language)
            log.info("Translated Text: " + translated_text)
            total_characters_translated = total_characters_translated + len(dialogue_text_list_element)
            data = data.replace(dialogue_text_list_element, translated_text)
        with open(new_file_path, "w", encoding="utf-8") as file:
            file.write(data)
    log_text = "Translation Complete! total_characters_translated : " + str(total_characters_translated)
    log.info(log_text)
