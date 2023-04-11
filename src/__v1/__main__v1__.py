import os

import dearpygui.dearpygui as dpg

from __v1 import hrsa_cct_config, cct_ui_panels, hrsa_cct_constants, hrsa_cct_globals
from __v1.hrsa_cct_globals import log
from __v1.ui import cct_patient_info_ui, cct_scenario_config_ui, cct_workflow_ui, cct_scenario_ui, audio_generation_ui, translate_ui, show_ink_files_ui
from __v1.ui import transfer_to_device_ui
from app_font_registry.app_dpg_font_registry import AppFontRegistry
from app_theme.app_dpg_theme import AppTheme
from app_version import app_version

# debug build parameters
is_debug: bool = hrsa_cct_globals.is_debug

# TODO: Split into modules and change the global data variable to function return values

# DearPyGUI's Viewport Constants
VIEWPORT_TITLE = "HRSA Content Creation Tool"
VIEWPORT_WIDTH = 1200
VIEWPORT_HEIGHT = 900  # 700

# GUI Element Tags

FILE_DIALOG: str = "FILE_DIALOG"
FILE_DIALOG_FOR_DATA_FOLDER: str = "FILE_DIALOG_FOR_DATA_FOLDER"
SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_DATA_FOLDER"
DATA_DIRECTORY_PATH_TEXT: str = "DATA_DIRECTORY_PATH_TEXT"
DATA_DIRECTORY_ERROR_TEXT: str = "DATA_DIRECTORY_ERROR_TEXT"
FILE_DIALOG_FOR_GOOGLE_CLOUD_CREDENTIALS: str = "FILE_DIALOG_FOR_GOOGLE_CLOUD_CREDENTIALS"
SHOW_FILE_DIALOG_BUTTON_GOOGLE_CLOUD_CREDENTIALS: str = "SHOW_FILE_DIALOG_BUTTON_GOOGLE_CLOUD_CREDENTIALS"
GOOGLE_CLOUD_CREDENTIALS_FILE_PATH_TEXT: str = "GOOGLE_CLOUD_CREDENTIALS_FILE_PATH_TEXT"
GOOGLE_CLOUD_CREDENTIALS_ERROR_TEXT: str = "GOOGLE_CLOUD_CREDENTIALS_ERROR_TEXT"

FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION: str = "FILE_DIALOG_FOR_SCENARIO_FOLDER_DESTINATION"
SHOW_FILE_DIALOG_BUTTON_SCENARIO_DESTINATION_FOLDER: str = "SHOW_FILE_DIALOG_BUTTON_SCENARIO_DESTINATION_FOLDER"
SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION: str = "SCENARIO_DIRECTORY_PATH_TEXT_DESTINATION"

app_theme = AppTheme()
font_registry = AppFontRegistry()


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


def callback_on_show_file_dialog_clicked(item_tag):
    dpg.configure_item(item_tag, show=True, modal=True)


def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


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

    # Bind a theme to the dpg application context
    app_theme.on_render()
    dpg.bind_theme(app_theme.dark_theme)

    font_registry.on_render()
    dpg.bind_font(font_registry.default_font)

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

        # Create / Select Scenario UI - Initialize
        cct_scenario_ui.init_ui()

        # Patient Info UI - Initialize
        cct_patient_info_ui.init_ui()

        # Scenario Config UI - Initialize
        cct_scenario_config_ui.init_ui()

        # Show Ink Files UI - Initialize
        show_ink_files_ui.init_ui()

        # Show Audio Generation UI - Initialize
        audio_generation_ui.init_ui()

        # Show Translate UI - Initialize
        translate_ui.init_ui()

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
    # if is_debug:
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


def update_connect_to_cloud():
    if not hrsa_cct_globals.is_debug:
        hrsa_cct_globals.connect_to_cloud = True


if __name__ == "__main__":
    check_hrsa_config_files()
    update_connect_to_cloud()
    main()
