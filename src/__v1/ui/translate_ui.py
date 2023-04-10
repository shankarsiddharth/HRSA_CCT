import copy
import json
import os
import pathlib
import re
import shutil
import sys

import dearpygui.dearpygui as dpg
from google.cloud import translate
from google.oauth2 import service_account

from __v1 import hrsa_cct_config, cct_ui_panels, cct_advanced_options_ui
from __v1 import hrsa_cct_constants
from __v1 import hrsa_cct_globals
from __v1 import patient_info_translate
from __v1.hrsa_cct_globals import log
from hrsa_data.scenario_data.scenario_information.scenario_information import ScenarioInformation

project_id = ''
clientTranslate = None


def initialize_translate():
    global project_id, clientTranslate
    if hrsa_cct_config.is_google_cloud_credentials_file_found():
        try:
            credentials = service_account.Credentials.from_service_account_file(hrsa_cct_config.get_google_cloud_credentials_file_path())
            clientTranslate = translate.TranslationServiceClient(credentials=credentials)

            gc_project_id = ''
            with open(hrsa_cct_config.get_google_cloud_credentials_file_path(), 'r', encoding='utf-8') as f:
                data = json.load(f)
                if gc_project_id == '':
                    project_id = data['project_id']
        except Exception as e:
            log.error(str(e))
            if "401" in str(e):
                log.error("Error initializing Google Cloud Translate: Please check your Google Cloud credentials JSON file.")
            elif "503" in str(e):
                log.error("Error initializing Google Cloud Translate: Please check your internet connection.")
                log.error("Also, make sure that the firewall is not blocking the connection to Google Cloud APIs.")
            else:
                log.error("Error initializing Google Cloud Translate: Please check your Google Cloud credentials JSON file.")


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
NEW_DATA_DIRECTORY_PATH_TEXT: str = "NEW_DATA_DIRECTORY_PATH_TEXT"
SOURCE_SCENARIO_DIRECTORY_PATH_TEXT: str = "SOURCE_SCENARIO_DIRECTORY_PATH_TEXT"
TRANSLATE_TEXT_BUTTON: str = "TRANSLATE_TEXT_BUTTON"
LANGUAGE_LISTBOX: str = "LANGUAGE_LISTBOX"
DESTINATION_SECTION_GROUP: str = "DESTINATION_SECTION_GROUP"
LANGUAGE_LISTBOX_GROUP: str = "LANGUAGE_LISTBOX_GROUP"
SOURCE_SECTION_GROUP: str = "SOURCE_SECTION_GROUP"


def callback_on_source_scenario_folder_selected(sender, app_data):
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


def translate_text(text="I want to translate this text.", language="es"):
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
    if project_id == '':
        log.error("Google Cloud Project ID is not set.")
        return

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
    # Translate the scenario information JSON file
    scenario_information_json_path = os.path.join(new_scenario_path_language_code, hrsa_cct_constants.SCENARIO_INFORMATION_JSON_FILE_NAME)
    scenario_information: ScenarioInformation = ScenarioInformation.load_from_json_file(scenario_information_json_path)
    if len(str(scenario_information.localized_name)) != 0:
        scenario_information.localized_name = translate_text(text=scenario_information.localized_name, language=selected_language)
    if len(str(scenario_information.description)) != 0:
        scenario_information.description = translate_text(text=scenario_information.description, language=selected_language)
    ScenarioInformation.save_to_json_file(scenario_information, scenario_information_json_path)
    # Translate the patient information JSON file
    patient_information_json_path = os.path.join(new_scenario_path_language_code, hrsa_cct_constants.PATIENT_INFORMATION_JSON_FILE_NAME)
    if os.path.exists(patient_information_json_path):
        patient_info_translate.translate_patient_info(patient_information_json_path)
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
                log.trace("path_to_add: " + path_to_add)
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
        if not hrsa_cct_globals.connect_to_cloud:
            file_ink.close()
            continue
        file_ink.seek(0, 0)
        data = file_ink.read()
        file_ink.close()
        # Sort the dialogue text list by descending order of length
        # i.e. The largest text will be translated and replaced first
        # This step is required to avoid replacing the text in the middle of the string
        #   If the text is replaced in the middle of the string then the translation will be incorrect,
        #       because the text will be split with source language and translated language text
        dialogue_text_list.sort(key=len, reverse=True)
        # Translate and replace the text in the sorted list order
        for dialogue_text_list_element in dialogue_text_list:
            try:
                translated_text = translate_text(text=dialogue_text_list_element, language=selected_language)
                log.info("Translated Text: " + translated_text)
                total_characters_translated = total_characters_translated + len(dialogue_text_list_element)
                data = data.replace(dialogue_text_list_element, translated_text)
            except Exception as e:
                log.error(str(e))
                log.error("Error Occurred while translating text: " + dialogue_text_list_element)
        with open(new_file_path, "w", encoding="utf-8") as file:
            file.write(data)
    log_text = "Translation Complete! total_characters_translated : " + str(total_characters_translated)
    log.info(log_text)


def callback_on_show_file_dialog_clicked(item_tag):
    dpg.configure_item(item_tag, show=True, modal=True)


def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


def init_ui():
    with dpg.collapsing_header(tag=cct_ui_panels.TRANSLATE_COLLAPSING_HEADER,
                               label="Translation", default_open=False,
                               show=hrsa_cct_config.is_google_cloud_credentials_file_found()):
        dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False,
                            callback=callback_on_source_scenario_folder_selected,
                            default_path=hrsa_cct_config.get_file_dialog_default_path(),
                            cancel_callback=file_dialog_cancel_callback)
        dpg.add_button(tag=cct_advanced_options_ui.SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER, label="Select Scenario Folder...",
                       callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER))
        with dpg.group(tag=SOURCE_SECTION_GROUP, horizontal=True, show=False):
            dpg.add_text("Selected Source Language Folder (en) : ")
            dpg.add_text(tag=SOURCE_SCENARIO_DIRECTORY_PATH_TEXT)
        with dpg.group(tag=LANGUAGE_LISTBOX_GROUP, horizontal=True, show=False):
            dpg.add_text("Language To Translate: ")
            dpg.add_listbox(tag=LANGUAGE_LISTBOX, items=hrsa_cct_globals.language_list,
                            callback=set_new_language_code, default_value="")
        with dpg.group(tag=DESTINATION_SECTION_GROUP, horizontal=True, show=False):
            dpg.add_text("Destination Language Folder: ")
            dpg.add_text(tag=NEW_DATA_DIRECTORY_PATH_TEXT)
        dpg.add_button(tag=TRANSLATE_TEXT_BUTTON, label="Translate Data", show=False, callback=callback_on_translate_text_clicked)
        dpg.add_separator()


if sys.flags.dev_mode:
    print("translate_ui.__init__()")
