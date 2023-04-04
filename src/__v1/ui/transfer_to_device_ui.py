import os.path
import sys

import dearpygui.dearpygui as dpg
from adbutils import adb

from __v1 import cct_ui_panels, hrsa_cct_config, hrsa_cct_globals

connected_devices = []
target_devices = []
scenario_list = []
selected_scenario_list = []

TTD_SELECT_APK_FILE_DIALOG: str = 'TTD_SELECT_APK_FILE_DIALOG'
TOD_DEVICES_GROUP: str = 'TOD_DEVICES_GROUP'
TOD_MESSAGE_TEXT: str = 'TOD_MESSAGE_TEXT'

HRSA_DATA_ROOT_PATH: str = '/storage/emulated/0/HRSAData/'

TOD_SCENARIO_LIST_WINDOW: str = "TOD_SCENARIO_LIST_WINDOW"


def kill_adb_server():
    adb.server_kill()


def _select_target_device(sender, app_data, user_data):
    global target_devices
    if user_data not in target_devices:
        target_devices.append(user_data)


def _toggle_media_transfer(sender, app_data, user_data):
    global target_devices
    if len(target_devices) <= 0:
        print("No target devices selected!")
    for info in target_devices:
        print(info)
        try:
            device = adb.device(serial=info)
            if user_data:
                device.shell("svc usb setFunctions mtp")
                device = adb.device(serial=info)  # need reconnect
                device.shell("svc usb setScreenUnlockedFunctions mtp")
            else:
                device.shell("svc usb setScreenUnlockedFunctions")
                device = adb.device(serial=info)  # need reconnect
                device.shell("svc usb setFunctions")
        except RuntimeError as e:
            print(e)


def _callback_transfer_scenario_data(sender, app_data, user_data):
    global target_devices, selected_scenario_list
    for serial in target_devices:
        device = adb.device(serial=serial)
        for scenario in selected_scenario_list:
            try:
                # check or create the HRSA_DATA_ROOT_PATH at the target device
                if not _adb_util_check_file_exist(device, HRSA_DATA_ROOT_PATH):
                    print(HRSA_DATA_ROOT_PATH + ' not exist.')
                    if not _adb_util_create_file(device, HRSA_DATA_ROOT_PATH):
                        raise Exception("Failed to create HRSAData folder in the target device.")
                # delete the previous data folder
                scenario_target_path = HRSA_DATA_ROOT_PATH + scenario + '/'
                if _adb_util_check_file_exist(device, scenario_target_path):
                    _adb_util_delete_file(device, scenario_target_path)
                # copy the data
                scenario_source_path = _retrieve_scenario_path(scenario) + '.zip'
                scenario_target_path = HRSA_DATA_ROOT_PATH + scenario + '.zip'
                if _adb_util_check_file_exist(device, scenario_target_path):
                    _adb_util_delete_file(device, scenario_target_path)
                print(scenario_source_path)
                print(scenario_target_path)
                device.sync.push(scenario_source_path, scenario_target_path, mode=0o777)
                _adb_util_unzip_file(device, scenario_target_path)
            except Exception as e:
                print(e)


def _install_latest_package(sender, app_data, user_data):
    dpg.configure_item(TTD_SELECT_APK_FILE_DIALOG, show=True)


def _callback_load_apk_file(sender, app_data, user_data):
    global target_devices
    if len(target_devices) <= 0:
        print("No target devices selected!")
    for info in target_devices:
        device = adb.device(serial=info.serial)
        device.install(app_data["file_path_name"], silent=True)


def file_dialog_cancel_callback(sender, app_data, user_data):
    pass


def init_ui():
    with dpg.collapsing_header(label="Transfer to Device", tag=cct_ui_panels.TRANSFER_TO_DEVICE_COLLAPSING_HEADER,
                               default_open=True):
        with dpg.group(horizontal=True, indent=20):
            dpg.add_text('Devices')
            dpg.add_button(label='Refresh', callback=refresh_device_list)
            dpg.add_button(label='Select All', callback=toggle_select_all, user_data=True)
            dpg.add_button(label='Unselect All', callback=toggle_select_all, user_data=False)
        with dpg.group(tag=TOD_DEVICES_GROUP, indent=40):
            pass
        dpg.add_text('No Device Connected!', tag=TOD_MESSAGE_TEXT, indent=40)
        dpg.add_button(label='Install Latest Package', callback=_install_latest_package, user_data=True)

        dpg.add_separator()
        dpg.add_child_window(width=500, height=225, tag=TOD_SCENARIO_LIST_WINDOW)
        dpg.add_button(label='Enable Media Transfer', callback=_toggle_media_transfer, user_data=True)
        dpg.add_button(label='Transfer Scenarios', callback=_callback_transfer_scenario_data, user_data=True)

        # file selection dialog start
        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_callback_load_apk_file, tag=TTD_SELECT_APK_FILE_DIALOG, modal=True,
                             cancel_callback=file_dialog_cancel_callback):
            dpg.add_file_extension(".apk", color=(255, 255, 0, 255))
        # file selection dialog end

        dpg.add_separator()


def toggle_select_all(sender, app_data, user_data):
    global connected_devices
    for device in connected_devices:
        dpg.set_value(create_device_checkbox_tag(device.serial), user_data)
    global target_devices
    target_devices = connected_devices if user_data else []


def create_device_checkbox_tag(device_id):
    return 'TOD_DEVICE_CHECKBOX_' + str(device_id)


def refresh_device_list():
    # Clear device list
    dpg.delete_item(TOD_DEVICES_GROUP, children_only=True)
    # Get connected devices
    global connected_devices
    connected_devices = adb.device_list()
    for device in connected_devices:
        device_label = f"{device.serial} ({device.prop.model})"
        dpg.add_checkbox(label=device_label,
                         tag=create_device_checkbox_tag(device.serial),
                         parent=TOD_DEVICES_GROUP,
                         source="bool_value", callback=_select_target_device,
                         user_data=device.serial)
    # Show message if no device connected and hide message if there is at least one device connected
    dpg.configure_item(TOD_MESSAGE_TEXT, show=(len(connected_devices) <= 0))


def create_scenario_checkbox_tag(scenario_name):
    return 'TOD_SCENARIO_CHECKBOX_' + str(scenario_name)


def _select_target_scenario(sender, app_data, user_data):
    print(sender, app_data, user_data)
    global selected_scenario_list
    if app_data:
        if user_data not in selected_scenario_list:
            selected_scenario_list.append(user_data)
    else:
        selected_scenario_list.remove(user_data)


def refresh_scenario_list():
    dpg.delete_item(TOD_SCENARIO_LIST_WINDOW, children_only=True)
    global scenario_list
    if hrsa_cct_config.is_user_hrsa_data_folder_found():
        scenario_list = hrsa_cct_config.get_scenario_list()
    else:
        scenario_list = list()
    for scenario in scenario_list:
        dpg.add_checkbox(label=scenario,
                         tag=create_scenario_checkbox_tag(scenario),
                         parent=TOD_SCENARIO_LIST_WINDOW,
                         source="bool_value", callback=_select_target_scenario,
                         user_data=scenario)


def _retrieve_scenario_path(scenario_name):
    return os.path.join(hrsa_cct_config.get_user_hrsa_data_folder_path(), scenario_name)


def _adb_util_check_file_exist(device, file_path):
    cmd_str = '[ -e {0} ]'.format(file_path)
    ret = device.shell2(cmd_str)
    print(cmd_str + ' => ' + str(ret.returncode))
    return ret.returncode == 0


def _adb_util_create_file(device, file_path):
    cmd_str = 'mkdir -m 777 {}'.format(file_path)
    ret = device.shell2(cmd_str)
    print(cmd_str + ' => ' + str(ret.returncode))
    return ret.returncode == 0


def _adb_util_delete_file(device, file_path):
    cmd_str = 'rm -r {}'.format(file_path)
    ret = device.shell2(cmd_str)
    print(cmd_str + ' => ' + str(ret.returncode))
    return ret.returncode == 0


def _adb_util_unzip_file(device, file_path: str):
    unzip_dst_path = file_path[:file_path.rfind('/')]
    cmd_str = 'unzip  {0} -d {1}'.format(file_path, unzip_dst_path)
    ret = device.shell2(cmd_str)
    print(cmd_str + ' => ' + str(ret.returncode))
    return ret.returncode == 0


def init_data():
    refresh_device_list()
    refresh_scenario_list()


if sys.flags.dev_mode:
    print("transfer_to_device_ui.__init__()")
