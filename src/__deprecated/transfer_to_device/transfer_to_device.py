import json
import os

import dearpygui.dearpygui as dpg
from adbutils import adb

from __deprecated import hrsa_cct_constants

target_devices = []

TOD_SELECT_APK_FILE_DIALOG: str = 'TOD_SELECT_APK_FILE_DIALOG'


def _select_target_device(sender, app_data, user_data):
    print(sender, app_data)
    global target_devices
    if user_data not in target_devices:
        target_devices.append(user_data)


def _toggle_media_transfer(sender, app_data, user_data):
    global target_devices
    if len(target_devices) <= 0:
        print("No target devices selected!")
    for info in target_devices:
        try:
            device = adb.device(serial=info.serial)
            if user_data:
                device.shell("svc usb setFunctions mtp")
                device = adb.device(serial=info.serial)  # need reconnect
                device.shell("svc usb setScreenUnlockedFunctions mtp")
            else:
                device.shell("svc usb setScreenUnlockedFunctions")
                device = adb.device(serial=info.serial)  # need reconnect
                device.shell("svc usb setFunctions")
        except RuntimeError as e:
            print(e)


def _install_latest_package(sender, app_data, user_data):
    dpg.configure_item(TOD_SELECT_APK_FILE_DIALOG, show=True)


def _callback_load_apk_file(sender, app_data, user_data):
    global target_devices
    if len(target_devices) <= 0:
        print("No target devices selected!")
    for info in target_devices:
        device = adb.device(serial=info.serial)
        device.install(app_data["file_path_name"], silent=True)


def init_ui():
    with dpg.collapsing_header(label="Transfer to Device", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        dpg.add_text('Devices', indent=20)
        connected_devices = adb.device_list()
        for device in connected_devices:
            print(device.serial, device.prop.model)
            dpg.add_checkbox(label=device.serial, source="bool_value", callback=_select_target_device,
                             user_data=device.serial)
        if len(connected_devices) == 0:
            dpg.add_text('No Device Connected!', indent=40)
        dpg.add_button(label='Install Latest Package', callback=_install_latest_package, user_data=True)
        dpg.add_button(label='Enable Media Transfer', callback=_toggle_media_transfer, user_data=True)

        # file selection dialog start
        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_callback_load_apk_file, tag=TOD_SELECT_APK_FILE_DIALOG, modal=True):
            dpg.add_file_extension(".apk", color=(255, 255, 0, 255))
        # file selection dialog end