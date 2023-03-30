import configparser
import os
import pathlib

import hrsa_cct_constants as hcc
from __v1 import hrsa_cct_globals
from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_logger.app_logger import AppLogger

cct_config = configparser.ConfigParser()
cct_logger = AppLogger()
cct_file_system = AppFileSystem()
cct_file_system_constants = AppFileSystemConstants()

__FILE_DIALOG_DEFAULT_PATH__ = ''
__GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__ = ''
__USER_HRSA_DATA_FOLDER_PATH__ = ''
__is_sa_pk_file_found__ = False
__is_user_hrsa_data_folder_found__ = False

root_folder_path = cct_file_system.get_root_folder_path()
default_hrsa_data_folder_path = os.path.join(root_folder_path, cct_file_system_constants.HRSA_DATA_WORKSPACE_FOLDER_NAME)
cct_config_folder_path = os.path.join(root_folder_path, hcc.CCT_CONFIG_FOLDER_NAME)
cct_ini_file_path = os.path.join(cct_config_folder_path, hcc.CCT_CONFIG_FILE_NAME)
dpg_ini_file_path = os.path.join(cct_config_folder_path, hcc.DPG_CONFIG_FILE_NAME)

gc_ini_file = pathlib.Path(cct_ini_file_path)


def get_file_dialog_default_path():
    return __FILE_DIALOG_DEFAULT_PATH__


def update_file_dialog_default_path(file_dialog_default_path: str):
    global __FILE_DIALOG_DEFAULT_PATH__
    __FILE_DIALOG_DEFAULT_PATH__ = file_dialog_default_path


def get_google_cloud_credentials_file_path():
    return __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__


def get_user_hrsa_data_folder_path():
    return __USER_HRSA_DATA_FOLDER_PATH__


def is_google_cloud_credentials_file_found():
    return __is_sa_pk_file_found__


def is_user_hrsa_data_folder_found():
    return __is_user_hrsa_data_folder_found__


def read_config_file():
    global __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__, __USER_HRSA_DATA_FOLDER_PATH__, __FILE_DIALOG_DEFAULT_PATH__
    global __is_sa_pk_file_found__, __is_user_hrsa_data_folder_found__
    if gc_ini_file.exists():
        cct_config.read(cct_ini_file_path)
        if cct_config.has_section('CONFIG'):
            if cct_config.has_option('CONFIG', 'GOOGLE_CLOUD_CREDENTIALS_FILE_PATH'):
                # Path to Service Account Key JSON File
                __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__ = cct_config['CONFIG']['GOOGLE_CLOUD_CREDENTIALS_FILE_PATH']
            if cct_config.has_option('CONFIG', 'USER_HRSA_DATA_FOLDER_PATH'):
                # Path to User HRSA Data Folder
                __USER_HRSA_DATA_FOLDER_PATH__ = cct_config['CONFIG']['USER_HRSA_DATA_FOLDER_PATH']
                __FILE_DIALOG_DEFAULT_PATH__ = __USER_HRSA_DATA_FOLDER_PATH__
    else:
        # Path to Service Account Key JSON File
        __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__ = os.path.join(cct_config_folder_path,
                                                              cct_file_system_constants.DEFAULT_CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE_NAME)

    if __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__ != '':
        sa_pk_file = pathlib.Path(__GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__)
        if sa_pk_file.exists():
            __is_sa_pk_file_found__ = True

    if __USER_HRSA_DATA_FOLDER_PATH__ != '':
        user_hrsa_data_folder = pathlib.Path(__USER_HRSA_DATA_FOLDER_PATH__)
        if user_hrsa_data_folder.exists():
            __is_user_hrsa_data_folder_found__ = True

    if not __is_sa_pk_file_found__:
        __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__ = ''
        hrsa_cct_globals.log.error("Google Cloud Service Account Key JSON file not found. Please select the file.")
    if not __is_user_hrsa_data_folder_found__:
        __FILE_DIALOG_DEFAULT_PATH__ = root_folder_path
        hrsa_cct_globals.log.error("User HRSA Data Folder not found. Please select the folder.")


def save_config_file():
    global gc_ini_file

    if not gc_ini_file.exists():
        cct_config['CONFIG'] = {}
    else:
        cct_config.read(cct_ini_file_path)

    if __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__ != '':
        cct_config['CONFIG']['GOOGLE_CLOUD_CREDENTIALS_FILE_PATH'] = __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__
    if __USER_HRSA_DATA_FOLDER_PATH__ != '':
        cct_config['CONFIG']['USER_HRSA_DATA_FOLDER_PATH'] = __USER_HRSA_DATA_FOLDER_PATH__
    with open(cct_ini_file_path, 'w') as configfile:
        cct_config.write(configfile)


def update_google_cloud_credentials_file_path(json_file_path):
    global __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__, __is_sa_pk_file_found__
    __is_sa_pk_file_found__ = True
    __GOOGLE_CLOUD_CREDENTIALS_FILE_PATH__ = json_file_path
    save_config_file()
    read_config_file()


def update_user_hrsa_data_folder_path(folder_path):
    global __USER_HRSA_DATA_FOLDER_PATH__, __FILE_DIALOG_DEFAULT_PATH__
    global __is_user_hrsa_data_folder_found__
    __is_user_hrsa_data_folder_found__ = True
    __USER_HRSA_DATA_FOLDER_PATH__ = folder_path
    __FILE_DIALOG_DEFAULT_PATH__ = __USER_HRSA_DATA_FOLDER_PATH__
    save_config_file()


def get_version_file_string() -> str:
    global root_folder_path
    VERSION_FILE_NAME = 'version'
    version_file_path = os.path.join(root_folder_path, VERSION_FILE_NAME)
    version_file = pathlib.Path(version_file_path)
    if version_file.exists():
        with open(version_file_path, 'r') as version_file:
            version_string = version_file.read()
            return version_string
    else:
        return ''


def get_scenario_list():
    global __USER_HRSA_DATA_FOLDER_PATH__
    if __USER_HRSA_DATA_FOLDER_PATH__ != '':
        user_hrsa_data_folder = pathlib.Path(__USER_HRSA_DATA_FOLDER_PATH__)
        if user_hrsa_data_folder.exists():
            scenario_list = []
            for scenario_folder in user_hrsa_data_folder.iterdir():
                if scenario_folder.is_dir():
                    scenario_list.append(scenario_folder.name)
            return scenario_list
    return list()


read_config_file()
