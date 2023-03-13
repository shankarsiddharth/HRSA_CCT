import configparser
import os
import pathlib

from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_logger.app_logger import AppLogger

sa_pk_file_path = ''
user_hrsa_data_folder_path = ''
is_sa_pk_file_found = False
is_user_hrsa_data_folder_found = False

cct_config = configparser.ConfigParser()
cct_logger = AppLogger()
cct_file_system = AppFileSystem()
cct_file_system_constants = AppFileSystemConstants()

root_folder_path = cct_file_system.get_root_folder_path()
default_hrsa_data_folder_path = os.path.join(root_folder_path, cct_file_system_constants.HRSA_DATA_WORKSPACE_FOLDER_NAME)
cct_config_folder_path = os.path.join(root_folder_path, 'cctconfig')
cct_ini_file_path = os.path.join(cct_config_folder_path, 'cct.config.ini')
dpg_ini_file_path = os.path.join(cct_config_folder_path, 'dpg.config.ini')

gc_ini_file = pathlib.Path(cct_ini_file_path)


def read_config_file():
    global sa_pk_file_path, user_hrsa_data_folder_path, is_sa_pk_file_found, is_user_hrsa_data_folder_found
    if gc_ini_file.exists():
        cct_config.read(cct_ini_file_path)
        # Path to Service Account Key JSON File
        sa_pk_file_path = cct_config['CONFIG']['SK_PK_JSON_FILE_PATH']
        # Path to User HRSA Data Folder
        user_hrsa_data_folder_path = cct_config['CONFIG']['USER_HRSA_DATA_FOLDER_PATH']
    else:
        # Path to Service Account Key JSON File
        sa_pk_file_path = os.path.join(cct_config_folder_path, cct_file_system_constants.DEFAULT_CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE_NAME)

    sa_pk_file = pathlib.Path(sa_pk_file_path)
    if sa_pk_file.exists():
        is_sa_pk_file_found = True

    user_hrsa_data_folder = pathlib.Path(user_hrsa_data_folder_path)
    if user_hrsa_data_folder.exists():
        is_user_hrsa_data_folder_found = True


def save_config_file():
    global gc_ini_file

    if not gc_ini_file.exists():
        cct_config['CONFIG'] = {}
    else:
        cct_config.read(cct_ini_file_path)

    if sa_pk_file_path != '':
        cct_config['CONFIG']['SK_PK_JSON_FILE_PATH'] = sa_pk_file_path
    if user_hrsa_data_folder_path != '':
        cct_config['CONFIG']['USER_HRSA_DATA_FOLDER_PATH'] = user_hrsa_data_folder_path
    with open(cct_ini_file_path, 'w') as configfile:
        cct_config.write(configfile)


read_config_file()
