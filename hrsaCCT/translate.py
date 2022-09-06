import os
import re
import shutil
import copy

import dearpygui.dearpygui as dpg
from google.cloud import translate
from google.oauth2 import service_account

import hrsa_cct_globals


credentials = service_account.Credentials.from_service_account_file("./decent-lambda-354120-0d9c66891965.json")
clientTranslate = translate.TranslationServiceClient(credentials=credentials)

new_data_path = ""
source_scenario_language_code_path = ""
selected_language = "es"
regStr = '\".*?\"'
new_language_code = ""
new_scenario_path_language_code = ""

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
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global source_scenario_language_code_path
    global new_data_path
    source_scenario_folder_path = os.path.normpath(str(app_data['file_path_name']))
    source_scenario_language_code_path = os.path.join(source_scenario_folder_path, hrsa_cct_globals.default_language_code)
    new_data_path = os.path.abspath(source_scenario_folder_path)
    print("source_scenario_language_code_path: ", source_scenario_language_code_path)
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
    print("new_language_code: ", new_language_code)
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
    print("Translating : " + text + " - to " + language)
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
    global new_scenario_path_language_code
    global source_scenario_language_code_path
    # copy directory
    print(source_scenario_language_code_path)
    print(new_scenario_path_language_code)
    # TODO: Add scenario_information.json once the translation functionality is complete for that file
    shutil.copytree(source_scenario_language_code_path, new_scenario_path_language_code,
                    ignore=shutil.ignore_patterns('*.mp3', '*.wav', 'feedback.json', 'dialogue.json'))
    # find ink files
    ink_files_list = []
    for root, dirs, files in os.walk(new_scenario_path_language_code):
        for file in files:
            if file.endswith(".ink"):
                path_to_add = os.path.join(root, file)
                ink_files_list.append(path_to_add)
                print(path_to_add)
    # translate
    dialogue_list = []
    for newFilePath in ink_files_list:
        file_ink = open(newFilePath, 'r+')
        lines = file_ink.readlines()
        for line in lines:
            dialogue = re.search(regStr, line)
            if dialogue:
                dialogue_check = dialogue.group(0).replace('"', '')
                if dialogue_check not in dialogue_list:
                    dialogue_list.append(dialogue_check)

        file_ink.seek(0, 0)
        data = file_ink.read()
        # print(data)
        file_ink.close()
        for dialogueItem in dialogue_list:
            translated_dialogue = translate_text(text=dialogueItem, language=selected_language)
            # print(translatedDialogue)
            data = data.replace(dialogueItem, translated_dialogue)
        with open(newFilePath, 'w', encoding='utf-8') as file:
            file.write(data)
    print("done!")
