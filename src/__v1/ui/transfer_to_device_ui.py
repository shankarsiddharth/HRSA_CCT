import sys

import dearpygui.dearpygui as dpg
from adbutils import adb

from __v1 import cct_ui_panels

target_devices = []

TTD_SELECT_APK_FILE_DIALOG: str = 'TTD_SELECT_APK_FILE_DIALOG'
TOD_DEVICES_GROUP: str = 'TOD_DEVICES_GROUP'
TOD_MESSAGE_TEXT: str = 'TOD_MESSAGE_TEXT'


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
        with dpg.group(tag=TOD_DEVICES_GROUP, indent=40):
            pass
        dpg.add_text('No Device Connected!', tag=TOD_MESSAGE_TEXT, indent=40)
        dpg.add_button(label='Install Latest Package', callback=_install_latest_package, user_data=True)
        dpg.add_button(label='Enable Media Transfer', callback=_toggle_media_transfer, user_data=True)

        # file selection dialog start
        with dpg.file_dialog(height=300, width=600, directory_selector=False, show=False,
                             callback=_callback_load_apk_file, tag=TTD_SELECT_APK_FILE_DIALOG, modal=True,
                             cancel_callback=file_dialog_cancel_callback):
            dpg.add_file_extension(".apk", color=(255, 255, 0, 255))
        # file selection dialog end

        dpg.add_separator()


def refresh_device_list():
    # Clear device list
    dpg.delete_item(TOD_DEVICES_GROUP, children_only=True)
    # Get connected devices
    connected_devices = adb.device_list()
    for device in connected_devices:
        device_label = f"{device.serial} ({device.prop.model})"
        dpg.add_checkbox(label=device_label,
                         parent=TOD_DEVICES_GROUP,
                         source="bool_value", callback=_select_target_device,
                         user_data=device.serial)
    # Show message if no device connected and hide message if there is at least one device connected
    dpg.configure_item(TOD_MESSAGE_TEXT, show=(len(connected_devices) <= 0))


def init_data():
    refresh_device_list()


if sys.flags.dev_mode:
    print("transfer_to_device_ui.__init__()")
