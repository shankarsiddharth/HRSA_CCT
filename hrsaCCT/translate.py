import os
import dearpygui.dearpygui as dpg
from google.cloud import translate
from google.oauth2 import service_account
from shutil import copytree, ignore_patterns
import re
import audio_generation

credentials = service_account.Credentials.from_service_account_file("./decent-lambda-354120-0d9c66891965.json")
clientTranslate = translate.TranslationServiceClient(credentials=credentials)

FILE_DIALOG_FOR_NEW_DATA_FOLDER: str = "FILE_DIALOG_FOR_NEW_DATA_FOLDER"
FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER: str = "FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER"
SHOW_FILE_DIALOG_BUTTON_NEW_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_NEW_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER"
NEW_DATA_DIRECTORY_PATH_TEXT: str = "NEW_DATA_DIRECTORY_PATH_TEXT"
SOURCE_SCENARIO_DIRECTORY_PATH_TEXT: str = "SOURCE_SCENARIO_DIRECTORY_PATH_TEXT"
TRANSLATE_TEXT_BUTTON: str = "TRANSLATE_TEXT_BUTTON"
LANGUAGE_LISTBOX: str = "LANGUAGE_LISTBOX"

new_data_path = ""
source_scenario_path = ""
selected_language = "es"
regStr = '\".*?\"'
new_language_code = ""
new_scenario_path_language_code = ""
language_list = [
    'en-US',
    'es'
]

def callback_on_source_scenario_folder_selected(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)
    global source_scenario_path
    global new_data_path
    source_scenario_path = os.path.normpath(str(app_data['file_path_name']))
    new_data_path = os.path.dirname(source_scenario_path)
    print(source_scenario_path)
    dpg.configure_item(SOURCE_SCENARIO_DIRECTORY_PATH_TEXT, default_value=source_scenario_path)
    dpg.configure_item(NEW_DATA_DIRECTORY_PATH_TEXT, default_value=new_data_path)
    dpg.configure_item(LANGUAGE_LISTBOX, show=True)

def set_new_language_code(sender):
    global new_language_code
    global new_data_path
    global new_scenario_path_language_code
    new_language_code = dpg.get_value(sender)
    print(new_language_code)
    new_scenario_path_language_code = os.path.normpath(new_data_path + '/' + new_language_code)
    dpg.configure_item(NEW_DATA_DIRECTORY_PATH_TEXT, default_value=new_scenario_path_language_code)
    dpg.configure_item(TRANSLATE_TEXT_BUTTON, show=True)


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
    global source_scenario_path
    #copy directory
    print(source_scenario_path)
    print(new_scenario_path_language_code)
    copytree(source_scenario_path, new_scenario_path_language_code, ignore=ignore_patterns('*.mp3', '*.wav'))
    #find ink files
    ink_files_list = []
    for root, dirs, files in os.walk(new_scenario_path_language_code):
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
    print("generating audio files...")
    audio_generation.generate_audio(path=new_scenario_path_language_code)