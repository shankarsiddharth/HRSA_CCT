import os
import subprocess
import sys
import threading

import dearpygui.dearpygui as dpg

from __v1 import hrsa_cct_constants as hcc, hrsa_cct_globals as hcg, hrsa_cct_config, cct_ui_panels, cct_advanced_options_ui
from __v1.hrsa_cct_globals import hfsc, hfs, log

ink_file_process_threads = dict()
thread_counter = 0

# UI Constants
SIF_FILE_DIALOG_FOR_SCENARIO_FOLDER: str = 'SIF_FILE_DIALOG_FOR_SCENARIO_FOLDER'
SIF_SCENARIO_DIRECTORY_PATH_TEXT: str = 'SIF_SCENARIO_DIRECTORY_PATH_TEXT'

OPEN_BREAK_ROOM_DIALOGUE_INK_FILE_BUTTON: str = 'OPEN_BREAK_ROOM_DIALOGUE_INK_FILE_BUTTON'
OPEN_PATIENT_ROOM_DIALOGUE_INK_FILE_BUTTON: str = 'OPEN_PATIENT_ROOM_DIALOGUE_INK_FILE_BUTTON'
OPEN_BREAK_ROOM_FEEDBACK_INK_FILE_BUTTON: str = 'OPEN_BREAK_ROOM_FEEDBACK_INK_FILE_BUTTON'
OPEN_PATIENT_ROOM_FEEDBACK_INK_FILE_BUTTON: str = 'OPEN_PATIENT_ROOM_FEEDBACK_INK_FILE_BUTTON'

SIF_BREAK_ROOM_DIALOGUE_INK_FILE_PATH_TEXT: str = 'SIF_BREAK_ROOM_DIALOGUE_INK_FILE_PATH_TEXT'
SIF_PATIENT_ROOM_DIALOGUE_INK_FILE_PATH_TEXT: str = 'SIF_PATIENT_ROOM_DIALOGUE_INK_FILE_PATH_TEXT'
SIF_BREAK_ROOM_FEEDBACK_INK_FILE_PATH_TEXT: str = 'SIF_BREAK_ROOM_FEEDBACK_INK_FILE_PATH_TEXT'
SIF_PATIENT_ROOM_FEEDBACK_INK_FILE_PATH_TEXT: str = 'SIF_PATIENT_ROOM_FEEDBACK_INK_FILE_PATH_TEXT'

bin_folder = hfs.get_default_binary_folder_path()
inky_windows_path = os.path.join(bin_folder, hfsc.BINARY_INKY_FOLDER_NAME, hfsc.WINDOWS_BINARY_FOLDER_NAME, hfsc.DEFAULT_WINDOWS_INKY_EXECUTABLE_FILE_NAME)

break_room_dialogue_ink_file_path: str = ''
patient_room_dialogue_ink_file_path: str = ''
break_room_feedback_ink_file_path: str = ''
patient_room_feedback_ink_file_path: str = ''


def set_scenario_path(scenario_path):
    source_scenario_language_code_path = os.path.join(scenario_path, hcg.default_language_code)
    dpg.configure_item(SIF_SCENARIO_DIRECTORY_PATH_TEXT, default_value=source_scenario_language_code_path)
    global break_room_dialogue_ink_file_path, patient_room_dialogue_ink_file_path, break_room_feedback_ink_file_path, patient_room_feedback_ink_file_path
    break_room_dialogue_ink_file_path = os.path.join(source_scenario_language_code_path, hcc.BREAK_ROOM_NAME, hcc.DIALOGUE_INK_FILE_NAME)
    patient_room_dialogue_ink_file_path = os.path.join(source_scenario_language_code_path, hcc.PATIENT_ROOM_NAME, hcc.DIALOGUE_INK_FILE_NAME)
    break_room_feedback_ink_file_path = os.path.join(source_scenario_language_code_path, hcc.FEEDBACK_ROOM_NAME, hcc.FEEDBACK_TYPE_BREAK_ROOM_NAME,
                                                     hcc.FEEDBACK_INK_FILE_NAME)
    patient_room_feedback_ink_file_path = os.path.join(source_scenario_language_code_path, hcc.FEEDBACK_ROOM_NAME, hcc.FEEDBACK_TYPE_PATIENT_ROOM_NAME,
                                                       hcc.FEEDBACK_INK_FILE_NAME)

    dpg.configure_item(SIF_BREAK_ROOM_DIALOGUE_INK_FILE_PATH_TEXT, default_value=break_room_dialogue_ink_file_path)
    dpg.configure_item(SIF_PATIENT_ROOM_DIALOGUE_INK_FILE_PATH_TEXT, default_value=patient_room_dialogue_ink_file_path)
    dpg.configure_item(SIF_BREAK_ROOM_FEEDBACK_INK_FILE_PATH_TEXT, default_value=break_room_feedback_ink_file_path)
    dpg.configure_item(SIF_PATIENT_ROOM_FEEDBACK_INK_FILE_PATH_TEXT, default_value=patient_room_feedback_ink_file_path)


def _open_break_room_dialogue_ink_file(sender, app_data, user_data):
    global break_room_dialogue_ink_file_path
    # _open_ink_file(break_room_dialogue_ink_file_path)
    _open_ink_file_in_thread(hcc.BREAK_ROOM_NAME, break_room_dialogue_ink_file_path)


def _open_patient_room_dialogue_ink_file(sender, app_data, user_data):
    global patient_room_dialogue_ink_file_path
    # _open_ink_file(patient_room_dialogue_ink_file_path)
    _open_ink_file_in_thread(hcc.PATIENT_ROOM_NAME, patient_room_dialogue_ink_file_path)


def _open_break_room_feedback_ink_file(sender, app_data, user_data):
    global break_room_feedback_ink_file_path
    # _open_ink_file(break_room_feedback_ink_file_path)
    _open_ink_file_in_thread(hcc.FEEDBACK_TYPE_BREAK_ROOM_NAME, break_room_feedback_ink_file_path)


def _open_patient_room_feedback_ink_file(sender, app_data, user_data):
    global patient_room_feedback_ink_file_path
    # _open_ink_file(patient_room_feedback_ink_file_path)
    _open_ink_file_in_thread(hcc.FEEDBACK_TYPE_PATIENT_ROOM_NAME, patient_room_feedback_ink_file_path)


def _open_ink_file(ink_file_path: str):
    if ink_file_path is None or ink_file_path == '':
        return
    cmd_string = inky_windows_path + " " + ink_file_path
    completed_process_result = subprocess.run([inky_windows_path, ink_file_path],
                                              capture_output=True, text=True)
    log.debug("cmd_string: " + cmd_string)
    log.debug("stdout: " + completed_process_result.stdout)
    log.debug("stderr: " + completed_process_result.stderr)
    log.debug("returncode: " + str(completed_process_result.returncode))


def _open_ink_file_in_thread(ink_file_type: str, ink_file_path: str):
    if ink_file_path is None or ink_file_path == '':
        return
    # if ink_file_type not in ink_file_process_threads:
    #     thread = threading.Thread(target=_open_ink_file, args=(ink_file_path,))
    #     ink_file_process_threads[ink_file_type] = thread
    #     thread.start()
    global thread_counter
    thread_counter += 1
    thread = threading.Thread(target=_open_ink_file, args=(ink_file_path,))
    ink_file_process_threads[thread_counter] = thread
    thread.start()


def _callback_on_scenario_folder_selected(sender, app_data):
    selected_file_path = str(app_data['file_path_name'])
    source_scenario_folder_path = os.path.normpath(selected_file_path)
    # source_scenario_language_code_path = os.path.join(source_scenario_folder_path, hcg.default_language_code)
    # new_data_path = os.path.abspath(source_scenario_folder_path)
    # log.info("source_scenario_language_code_path: " + source_scenario_language_code_path)
    # set_scenario_path(source_scenario_language_code_path)
    set_scenario_path(source_scenario_folder_path)


def _callback_on_show_file_dialog_clicked(item_tag):
    dpg.configure_item(item_tag, show=True, modal=True)


def wait_for_all_ink_threads():
    threads_list = threading.enumerate()
    for thread in threads_list:
        print("thread: " + str(thread.name))
        thread.join()


def file_dialog_cancel_callback(sender, app_data):
    pass


def init_ui():
    with dpg.collapsing_header(label="Ink Files", tag=cct_ui_panels.SHOW_INK_FILES_COLLAPSING_HEADER, default_open=False):
        dpg.add_file_dialog(tag=SIF_FILE_DIALOG_FOR_SCENARIO_FOLDER, height=300, width=450, directory_selector=True, show=False,
                            callback=_callback_on_scenario_folder_selected,
                            default_path=hrsa_cct_config.get_file_dialog_default_path(),
                            cancel_callback=file_dialog_cancel_callback)
        dpg.add_button(tag=cct_advanced_options_ui.SIF_SHOW_FILE_DIALOG_BUTTON_SCENARIO_FOLDER, label="Select Scenario Folder...",
                       callback=lambda s, a: _callback_on_show_file_dialog_clicked(item_tag=SIF_FILE_DIALOG_FOR_SCENARIO_FOLDER))
        dpg.add_text(tag=SIF_SCENARIO_DIRECTORY_PATH_TEXT)

        # dpg.add_text('')
        dpg.add_text("Break Room Ink File", bullet=True)
        dpg.add_button(label="Open Break Room Dialogue Ink File", tag=OPEN_BREAK_ROOM_DIALOGUE_INK_FILE_BUTTON, callback=_open_break_room_dialogue_ink_file, indent=20)
        dpg.add_text(tag=SIF_BREAK_ROOM_DIALOGUE_INK_FILE_PATH_TEXT, indent=20)
        # dpg.add_text('')
        dpg.add_text("Patient Room Ink File", bullet=True)
        dpg.add_button(label="Open Patient Room Dialogue Ink File", tag=OPEN_PATIENT_ROOM_DIALOGUE_INK_FILE_BUTTON, callback=_open_patient_room_dialogue_ink_file, indent=20)
        dpg.add_text(tag=SIF_PATIENT_ROOM_DIALOGUE_INK_FILE_PATH_TEXT, indent=20)
        # dpg.add_text('')
        dpg.add_text("Break Room Feedback Ink File", bullet=True)
        dpg.add_button(label="Open Break Room Feedback Ink File", tag=OPEN_BREAK_ROOM_FEEDBACK_INK_FILE_BUTTON, callback=_open_break_room_feedback_ink_file, indent=20)
        dpg.add_text(tag=SIF_BREAK_ROOM_FEEDBACK_INK_FILE_PATH_TEXT, indent=20)
        # dpg.add_text('')
        dpg.add_text("Patient Room Feedback Ink File", bullet=True)
        dpg.add_button(label="Open Patient Room Feedback Ink File", tag=OPEN_PATIENT_ROOM_FEEDBACK_INK_FILE_BUTTON, callback=_open_patient_room_feedback_ink_file, indent=20)
        dpg.add_text(tag=SIF_PATIENT_ROOM_FEEDBACK_INK_FILE_PATH_TEXT, indent=20)
        dpg.add_separator()


# if __name__ == '__main__':
#     _open_ink_file(r"C:\GAppLab\hrsa_cct\HRSAData_Old\Scenario1\en-US\BreakRoom\dialogue.ink")

if sys.flags.dev_mode:
    print("show_ink_files_ui.__init__()")
