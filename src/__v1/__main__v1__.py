import json
import os
import shutil
from dataclasses import asdict

import dearpygui.dearpygui as dpg

from __v1 import hrsa_cct_config, cct_ui_panels, hrsa_cct_constants, hrsa_cct_globals
from __v1.hrsa_cct_globals import log
from __v1.ui import cct_patient_info_ui, cct_scenario_config_ui, cct_workflow_ui, cct_scenario_ui, audio_generation_ui, translate_ui, show_ink_files_ui
from __v1.ui import transfer_to_device_ui
from app_version import app_version
from hrsa_data.scenario_data.scenario_information.scenario_information import ScenarioInformation

# debug build parameters
is_debug: bool = hrsa_cct_globals.is_debug

# TODO: Split into modules and change the global data variable to function return values

# DearPyGUI's Viewport Constants
VIEWPORT_TITLE = "HRSA Content Creation Tool"
VIEWPORT_WIDTH = 1200
VIEWPORT_HEIGHT = 900  # 700

# GUI Element Tags
SCENARIO_NAME_INPUT_TEXT: str = "SCENARIO_NAME_INPUT_TEXT"
SCENARIO_DESCRIPTION_INPUT_TEXT: str = "SCENARIO_DESCRIPTION_INPUT_TEXT"
CREATE_SCENARIO_INFORMATION_BUTTON: str = "CREATE_SCENARIO_INFORMATION_BUTTON"
FILE_DIALOG: str = "FILE_DIALOG"
FILE_DIALOG_FOR_DATA_FOLDER: str = "FILE_DIALOG_FOR_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER"
DATA_DIRECTORY_PATH_TEXT: str = "DATA_DIRECTORY_PATH_TEXT"
DATA_DIRECTORY_ERROR_TEXT: str = "DATA_DIRECTORY_ERROR_TEXT"
FILE_DIALOG_FOR_GOOGLE_CLOUD_CREDENTIALS: str = "FILE_DIALOG_FOR_GOOGLE_CLOUD_CREDENTIALS"
SHOW_FILE_DIALOG_BUTTON_GOOGLE_CLOUD_CREDENTIALS: str = "SHOW_FILE_DIALOG_BUTTON_GOOGLE_CLOUD_CREDENTIALS"
GOOGLE_CLOUD_CREDENTIALS_FILE_PATH_TEXT: str = "GOOGLE_CLOUD_CREDENTIALS_FILE_PATH_TEXT"
GOOGLE_CLOUD_CREDENTIALS_ERROR_TEXT: str = "GOOGLE_CLOUD_CREDENTIALS_ERROR_TEXT"
FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER"
SCENARIO_DIRECTORY_PATH_TEXT_SOURCE: str = "SCENARIO_DIRECTORY_PATH_TEXT_SOURCE"
FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_DESTINATION_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_DESTINATION_FOLDER"
SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION: str = "SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION"
COPY_SCENARIO_INFORMATION_BUTTON: str = "COPY_SCENARIO_INFORMATION_BUTTON"


def create_scenario_folders(scenario_name, scenario_information_json_object) -> bool:
    # Scenario Folder
    scenario_path_root = os.path.join(hrsa_cct_config.get_user_hrsa_data_folder_path(), scenario_name)
    log.info("scenario_path_root: " + scenario_path_root)
    # TODO: Check if the a scenario name already exists and display error information to the user
    try:
        os.mkdir(scenario_path_root)
    except FileExistsError:
        log.error("Scenario folder already exists: " + scenario_name)
        return False
    # Default Language Folder
    default_language_folder = os.path.join(scenario_path_root, hrsa_cct_globals.default_language_code)
    log.info("default_language_folder: " + default_language_folder)
    os.mkdir(default_language_folder)
    hrsa_cct_globals.scenario_path = os.path.abspath(default_language_folder)
    # Scenario Information JSON
    scenario_information_json_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.SCENARIO_INFORMATION_JSON_FILE_NAME)
    log.info("scenario_information_json_path: " + scenario_information_json_path)
    with open(scenario_information_json_path, "w", encoding="utf-8") as output_file:
        output_file.write(scenario_information_json_object)
    # Break Room
    break_room_folder_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.BREAK_ROOM_NAME)
    os.mkdir(break_room_folder_path)
    audio_folder = os.path.join(break_room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Patient Room
    patient_room_folder_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.PATIENT_ROOM_NAME)
    os.mkdir(patient_room_folder_path)
    audio_folder = os.path.join(patient_room_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_folder_path, hrsa_cct_constants.DIALOGUE_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Feedback Room
    feedback_room_folder_path = os.path.join(hrsa_cct_globals.scenario_path, hrsa_cct_constants.FEEDBACK_ROOM_NAME)
    os.mkdir(feedback_room_folder_path)
    # Break Room Feedback
    break_room_feedback_folder_path = os.path.join(feedback_room_folder_path, hrsa_cct_constants.FEEDBACK_TYPE_BREAK_ROOM_NAME)
    os.mkdir(break_room_feedback_folder_path)
    audio_folder = os.path.join(break_room_feedback_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(break_room_feedback_folder_path, hrsa_cct_constants.FEEDBACK_INK_FILE_NAME)
    open(file_path, 'a').close()
    # Patient Room Feedback
    patient_room_feedback_folder_path = os.path.join(feedback_room_folder_path, hrsa_cct_constants.FEEDBACK_TYPE_PATIENT_ROOM_NAME)
    os.mkdir(patient_room_feedback_folder_path)
    audio_folder = os.path.join(patient_room_feedback_folder_path, hrsa_cct_constants.AUDIO_FOLDER_NAME)
    os.mkdir(audio_folder)
    file_path = os.path.join(patient_room_feedback_folder_path, hrsa_cct_constants.FEEDBACK_INK_FILE_NAME)
    open(file_path, 'a').close()
    log.info("New Scenario Created. Scenario Name: " + scenario_name)

    hrsa_cct_globals.app_data = dict(file_path_name=scenario_path_root)
    hrsa_cct_globals.scenario_path_destination = os.path.normpath(scenario_path_root)
    # callback_on_scenario_destination_folder_selected(FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION, hrsa_cct_globals.app_data)
    return True


def callback_on_data_folder_selected(sender, app_data):
    data_path = os.path.normpath(str(app_data['file_path_name']))
    log.info('Data Folder Path: ' + data_path)
    hrsa_cct_config.update_user_hrsa_data_folder_path(data_path)
    # TODO : Error Checking of Valid Data Folder
    if hrsa_cct_config.is_user_hrsa_data_folder_found():
        log.info('Data Folder Selected')
        dpg.configure_item(DATA_DIRECTORY_PATH_TEXT, default_value=hrsa_cct_config.get_user_hrsa_data_folder_path(), show=True)
        dpg.configure_item(DATA_DIRECTORY_ERROR_TEXT, show=False)
    else:
        log.error('Data Folder Not Found')
        dpg.configure_item(DATA_DIRECTORY_ERROR_TEXT, show=False)
        dpg.configure_item(DATA_DIRECTORY_ERROR_TEXT, show=True)


def callback_on_google_cloud_credentials_file_selected(sender, app_data):
    json_file_path = os.path.normpath(str(app_data['file_path_name']))
    hrsa_cct_config.update_google_cloud_credentials_file_path(json_file_path)
    audio_generation_ui.initialize_audio_generation()
    translate_ui.initialize_translate()
    if hrsa_cct_config.is_google_cloud_credentials_file_found():
        dpg.configure_item(GOOGLE_CLOUD_CREDENTIALS_FILE_PATH_TEXT, default_value=hrsa_cct_config.get_google_cloud_credentials_file_path(),
                           show=True)
        log.info('Google Cloud Credentials File Selected')
        dpg.configure_item(GOOGLE_CLOUD_CREDENTIALS_ERROR_TEXT, show=False)
        dpg.configure_item(cct_ui_panels.AUDIO_GENERATION_COLLAPSING_HEADER, show=True)
        dpg.configure_item(cct_ui_panels.TRANSLATE_COLLAPSING_HEADER, show=True)
    else:
        dpg.configure_item(GOOGLE_CLOUD_CREDENTIALS_FILE_PATH_TEXT, show=False)
        dpg.configure_item(GOOGLE_CLOUD_CREDENTIALS_ERROR_TEXT, show=True)
        dpg.configure_item(cct_ui_panels.AUDIO_GENERATION_COLLAPSING_HEADER, show=False)
        dpg.configure_item(cct_ui_panels.TRANSLATE_COLLAPSING_HEADER, show=False)


def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


# def callback_on_select_data_folder_button_clicked():
#     dpg.configure_item(FILE_DIALOG_FOR_DATA_FOLDER, show=True, modal=True)
#
#
# def callback_show_file_dialog_scenario_folder():
#     dpg.configure_item(FILE_DIALOG_FOR_SCENARIO_FOLDER, show=True, modal=True)


def callback_on_show_file_dialog_clicked(item_tag):
    dpg.configure_item(item_tag, show=True, modal=True)


def callback_on_create_scenario_button_clicked() -> None:
    on_create_scenario_button_clicked()


def on_create_scenario_button_clicked() -> bool:
    scenario_name = dpg.get_value(SCENARIO_NAME_INPUT_TEXT)
    scenario_description = dpg.get_value(SCENARIO_DESCRIPTION_INPUT_TEXT)
    if scenario_name == "" or scenario_description == "":
        log.error("Scenario Name or Scenario Description cannot be Empty")
        return False

    scenario_information: ScenarioInformation = ScenarioInformation()
    scenario_information.name = scenario_name
    scenario_information.localized_name = scenario_name
    scenario_information.description = scenario_description
    scenario_information_json_object = json.dumps(asdict(scenario_information), indent=4)
    return create_scenario_folders(scenario_name, scenario_information_json_object)


def callback_on_scenario_source_folder_selected(sender, app_data):
    hrsa_cct_globals.scenario_path_source = os.path.normpath(str(app_data['file_path_name']))
    log.info("Source Scenario Path: " + hrsa_cct_globals.scenario_path_source)
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT_SOURCE, default_value=hrsa_cct_globals.scenario_path_source)


def callback_on_scenario_destination_folder_selected(sender, app_data):
    log.info("Destination Scenario Path: " + hrsa_cct_globals.scenario_path_destination)
    dpg.configure_item(SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION, default_value=hrsa_cct_globals.scenario_path_destination)


def callback_on_copy_scenario_button_clicked():
    on_copy_scenario_button_clicked()


def on_copy_scenario_button_clicked():
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=False)
    shutil.copytree(hrsa_cct_globals.scenario_path_source, hrsa_cct_globals.scenario_path_destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('*.mp3', '*.wav', 'scenario_information.json', 'feedback.json', 'dialogue.json', 'es-US'))
    log.info("Scenario Folder Copy Complete from: " + hrsa_cct_globals.scenario_path_source + "\tto: " + hrsa_cct_globals.scenario_path_destination)
    dpg.configure_item(COPY_SCENARIO_INFORMATION_BUTTON, show=True)

    cct_scenario_ui.set_current_scenario_path(hrsa_cct_globals.scenario_path_destination)

    # audio_generation_ui.callback_on_scenario_folder_selected(audio_generation_ui.FILE_DIALOG_FOR_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    # translate_ui.callback_on_source_scenario_folder_selected(translate_ui.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, hrsa_cct_globals.app_data)
    # cct_patient_info_ui.set_scenario_path(hrsa_cct_globals.scenario_path_destination)
    # cct_scenario_config_ui.set_scenario_path(hrsa_cct_globals.scenario_path_destination)
    # show_ink_files_ui.set_scenario_path(hrsa_cct_globals.scenario_path_destination)


def callback_on_create_scenario_by_copy_button_clicked():
    if hrsa_cct_globals.scenario_path_source is None \
            or hrsa_cct_globals.scenario_path_source == "" \
            or len(hrsa_cct_globals.scenario_path_source) == 0:
        log.error("Please, Select Source Scenario Folder and Try Again")
        return None
    is_scenario_created = on_create_scenario_button_clicked()
    if is_scenario_created:
        on_copy_scenario_button_clicked()


def save_init():
    dpg.save_init_file(hrsa_cct_config.dpg_ini_file_path)


def callback_on_connect_to_cloud_checkbox_clicked(sender, app_data, user_data):
    hrsa_cct_globals.connect_to_cloud = dpg.get_value("connect_to_cloud")


def __exit_callback__(sender, app_data, user_data):
    # log.info("User clicked on the Close Window button.")
    # show_ink_files_ui.wait_for_all_ink_threads()
    log.close_ui()
    transfer_to_device_ui.kill_adb_server()


def main() -> None:
    dpg.create_context()
    # light_theme_id = themes.create_theme_imgui_light()
    # dark_theme_id = themes.create_theme_imgui_dark()
    # dpg.bind_theme(dark_theme_id)

    if not is_debug:
        dpg.configure_app(manual_callback_management=False, docking=True, docking_space=True, load_init_file=hrsa_cct_config.dpg_ini_file_path)
    else:
        dpg.configure_app(manual_callback_management=True, docking=True, docking_space=True, load_init_file=hrsa_cct_config.dpg_ini_file_path)

    dpg.create_viewport(
        title=VIEWPORT_TITLE, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT,
        small_icon=hrsa_cct_globals.hfs.default_app_icon_small_file_path,
        large_icon=hrsa_cct_globals.hfs.default_app_icon_large_file_path,
    )

    dpg.set_exit_callback(callback=__exit_callback__)

    with dpg.window(label="HRSA CCT", tag=hrsa_cct_constants.HRSA_CCT_TOOL, width=VIEWPORT_WIDTH, height=VIEWPORT_HEIGHT, no_title_bar=True, no_close=True):
        # region Debug UI
        dpg.add_button(label="Save Init", callback=save_init, show=is_debug)
        dpg.add_checkbox(label="Connect to Cloud", tag="connect_to_cloud", show=is_debug,
                         default_value=hrsa_cct_globals.connect_to_cloud,
                         callback=callback_on_connect_to_cloud_checkbox_clicked)
        # endregion Debug UI

        # region App Config UI
        with dpg.collapsing_header(label="Google Cloud Credentials File", default_open=True):
            with dpg.file_dialog(tag=FILE_DIALOG_FOR_GOOGLE_CLOUD_CREDENTIALS, directory_selector=False, height=300, width=450, show=False,
                                 callback=callback_on_google_cloud_credentials_file_selected,
                                 default_path=hrsa_cct_config.get_file_dialog_default_path(),
                                 cancel_callback=file_dialog_cancel_callback):
                dpg.add_file_extension(".json", color=(255, 255, 0, 255))
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_GOOGLE_CLOUD_CREDENTIALS, label="Select Google Cloud Credentials File",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_GOOGLE_CLOUD_CREDENTIALS))
            dpg.add_text(tag=GOOGLE_CLOUD_CREDENTIALS_FILE_PATH_TEXT, default_value=hrsa_cct_config.get_google_cloud_credentials_file_path(),
                         show=hrsa_cct_config.is_google_cloud_credentials_file_found())
            dpg.add_text(tag=GOOGLE_CLOUD_CREDENTIALS_ERROR_TEXT, default_value="Google Cloud Credentials File Not Found",
                         show=(not hrsa_cct_config.is_google_cloud_credentials_file_found()))
            dpg.add_separator()

        with dpg.collapsing_header(label="Choose a location of the HRSAData Folder", default_open=True):
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_DATA_FOLDER, height=300, width=450, directory_selector=True, show=False,
                                callback=callback_on_data_folder_selected,
                                default_path=hrsa_cct_config.get_file_dialog_default_path(),
                                cancel_callback=file_dialog_cancel_callback)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER, label="Select Data Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_DATA_FOLDER))
            dpg.add_text(tag=DATA_DIRECTORY_PATH_TEXT, default_value=hrsa_cct_config.get_user_hrsa_data_folder_path(),
                         show=hrsa_cct_config.is_user_hrsa_data_folder_found())
            dpg.add_text(tag=DATA_DIRECTORY_ERROR_TEXT, default_value="HRSA Data Folder Not Found",
                         show=(not hrsa_cct_config.is_user_hrsa_data_folder_found()))
            dpg.add_separator()
        # endregion App Config UI

        # Choose Workflow UI - Initialize
        cct_workflow_ui.init_ui()

        # region Create Scenario UI
        with dpg.collapsing_header(label="Create Scenario", tag=cct_ui_panels.CREATE_SCENARIO_COLLAPSING_HEADER, default_open=True):
            dpg.add_input_text(tag=SCENARIO_NAME_INPUT_TEXT, label="Scenario Name", default_value="")
            dpg.add_input_text(tag=SCENARIO_DESCRIPTION_INPUT_TEXT, label="Scenario Description", multiline=True, tab_input=False)
            dpg.add_spacer(height=5)
            dpg.add_file_dialog(tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE, height=300, width=450, directory_selector=True, show=False,
                                callback=callback_on_scenario_source_folder_selected,
                                default_path=hrsa_cct_config.get_file_dialog_default_path(),
                                cancel_callback=file_dialog_cancel_callback)
            dpg.add_button(tag=SHOW_FILE_DIALOG_BUTTON_SCENARIO_SOURCE_FOLDER, label="Select Source Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=FILE_DIALOG_FOR_SCENARIO_FOLDER_SOURCE))
            dpg.add_text(tag=SCENARIO_DIRECTORY_PATH_TEXT_SOURCE)
            dpg.add_spacer(height=5)
            dpg.add_button(tag=COPY_SCENARIO_INFORMATION_BUTTON, label="Create Scenario", callback=callback_on_create_scenario_by_copy_button_clicked)
            dpg.add_separator()
        # endregion Create Scenario UI

        # Select Scenario UI - Initialize
        cct_scenario_ui.init_ui()

        # Patient Info UI - Initialize
        cct_patient_info_ui.init_ui()

        # Scenario Config UI - Initialize
        cct_scenario_config_ui.init_ui()

        # Show Ink Files UI - Initialize
        show_ink_files_ui.init_ui()

        # region Audio Generation UI
        with dpg.collapsing_header(tag=cct_ui_panels.AUDIO_GENERATION_COLLAPSING_HEADER,
                                   label="Choose the Scenario Folder for Audio Generation", default_open=False, show=hrsa_cct_config.is_google_cloud_credentials_file_found()):
            dpg.add_file_dialog(tag=audio_generation_ui.FILE_DIALOG_FOR_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False,
                                callback=audio_generation_ui.callback_on_scenario_folder_selected,
                                default_path=hrsa_cct_config.get_file_dialog_default_path(),
                                cancel_callback=file_dialog_cancel_callback)
            dpg.add_button(tag=audio_generation_ui.SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, label="Select Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=audio_generation_ui.FILE_DIALOG_FOR_SCENARIO_FOLDER))
            dpg.add_text(tag=audio_generation_ui.SCENARIO_DIRECTORY_PATH_TEXT)
            with dpg.group(tag=audio_generation_ui.AG_LANGUAGE_LISTBOX_GROUP, horizontal=True, show=False):
                dpg.add_text("Audio Generation Language: ")
                dpg.add_listbox(tag=audio_generation_ui.AG_LANGUAGE_LISTBOX, items=hrsa_cct_globals.language_list,
                                callback=audio_generation_ui.callback_on_language_code_selected, default_value="")
            dpg.add_text(tag=audio_generation_ui.SCENARIO_LANGUAGE_CODE_DIRECTORY_PATH_TEXT, show=False)
            # TODO: Voice Configuration
            with dpg.collapsing_header(indent=50, tag=audio_generation_ui.VOICE_CONFIG_SECTION, label="Configure Character Voice Settings", default_open=True, show=False):
                dpg.add_listbox(tag=audio_generation_ui.CHARACTER_SELECT_LISTBOX, label="Choose Character", num_items=5, show=True,
                                callback=audio_generation_ui.display_character_info)
                dpg.add_listbox(tag=audio_generation_ui.LANGUAGE_CODE_TEXT, label="Language Code", num_items=4, callback=audio_generation_ui.callback_on_change_language_code)
                dpg.add_listbox(tag=audio_generation_ui.AUDIO_GENDER_TEXT, label="Gender", num_items=3, show=True, callback=audio_generation_ui.callback_on_gender_selected)
                dpg.add_listbox(tag=audio_generation_ui.AUDIO_VOICE_LIST, label="Voice", num_items=10, tracked=True)
                dpg.add_button(tag=audio_generation_ui.SAVE_AUDIO_SETTINGS_BUTTON, label="Save voice settings", show=True, callback=audio_generation_ui.save_audio_settings)
            dpg.add_button(tag=audio_generation_ui.GENERATE_AUDIO_BUTTON, label="Generate Audio", show=False, callback=audio_generation_ui.callback_on_generate_audio_clicked)
            dpg.add_separator()
        # endregion Audio Generation UI

        # region Translate UI
        with dpg.collapsing_header(tag=cct_ui_panels.TRANSLATE_COLLAPSING_HEADER,
                                   label="Choose a location to create the Translated Data Folder", default_open=False,
                                   show=hrsa_cct_config.is_google_cloud_credentials_file_found()):
            dpg.add_file_dialog(tag=translate_ui.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False,
                                callback=translate_ui.callback_on_source_scenario_folder_selected,
                                default_path=hrsa_cct_config.get_file_dialog_default_path(),
                                cancel_callback=file_dialog_cancel_callback)
            dpg.add_button(tag=translate_ui.SHOW_FILE_DIALOG_BUTTON_SOURCE_SCENARIO_FOLDER, label="Select Scenario Folder",
                           callback=lambda s, a: callback_on_show_file_dialog_clicked(item_tag=translate_ui.FILE_DIALOG_FOR_SOURCE_SCENARIO_FOLDER))
            with dpg.group(tag=translate_ui.SOURCE_SECTION_GROUP, horizontal=True, show=False):
                dpg.add_text("Selected Source Language Folder (en) : ")
                dpg.add_text(tag=translate_ui.SOURCE_SCENARIO_DIRECTORY_PATH_TEXT)
            with dpg.group(tag=translate_ui.LANGUAGE_LISTBOX_GROUP, horizontal=True, show=False):
                dpg.add_text("Language To Translate: ")
                dpg.add_listbox(tag=translate_ui.LANGUAGE_LISTBOX, items=hrsa_cct_globals.language_list,
                                callback=translate_ui.set_new_language_code, default_value="")
            with dpg.group(tag=translate_ui.DESTINATION_SECTION_GROUP, horizontal=True, show=False):
                dpg.add_text("Destination Language Folder: ")
                dpg.add_text(tag=translate_ui.NEW_DATA_DIRECTORY_PATH_TEXT)
            dpg.add_button(tag=translate_ui.TRANSLATE_TEXT_BUTTON, label="Translate Data", show=False, callback=translate_ui.callback_on_translate_text_clicked)
            dpg.add_separator()
        # endregion Translate UI

        # Transfer to Device UI
        transfer_to_device_ui.init_ui()

    log.on_init_and_render_ui()

    # Init Data for UIs
    cct_workflow_ui.init_data()  # Show Default Workflow UI
    cct_scenario_ui.init_data()
    cct_patient_info_ui.init_data()
    transfer_to_device_ui.init_data()

    dpg.setup_dearpygui()
    dpg.show_viewport()
    if is_debug:
        dpg.maximize_viewport()
    # dpg.set_primary_window(hrsa_cct_constants.HRSA_CCT_TOOL, True)

    if not is_debug:
        dpg.start_dearpygui()
    else:
        while dpg.is_dearpygui_running():
            jobs = dpg.get_callback_queue()  # retrieves and clears queue
            dpg.run_callbacks(jobs)
            dpg.render_dearpygui_frame()

    dpg.destroy_context()


def check_hrsa_config_files():
    global VIEWPORT_TITLE
    version_file_string = hrsa_cct_config.get_version_file_string()
    if version_file_string != '':
        VIEWPORT_TITLE = f"{VIEWPORT_TITLE} - {version_file_string}"
    else:
        VIEWPORT_TITLE = f"{VIEWPORT_TITLE} - {app_version.APP_VERSION_STRING}"
    hrsa_cct_config.read_config_file()
    if hrsa_cct_config.is_google_cloud_credentials_file_found():
        audio_generation_ui.initialize_audio_generation()
        translate_ui.initialize_translate()


if __name__ == "__main__":
    check_hrsa_config_files()
    main()
