import os
import pathlib
import shutil
import sys
import threading

from .app_file_system_constants import AppFileSystemConstants


class AppFileSystem(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppFileSystem, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if sys.flags.dev_mode:
                        print("AppFileSystem.__new__()")
        return cls._instance

    def __initialize__(self):
        self.afsc: AppFileSystemConstants = AppFileSystemConstants()
        self.__EXECUTABLE_PATH__ = None

    def get_root_folder(self):
        application_path = ""
        if getattr(sys, 'frozen', False):
            self.__EXECUTABLE_PATH__ = os.path.realpath(sys.executable)
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            current_file_dir_path = os.path.dirname(__file__)
            application_path = os.path.dirname(current_file_dir_path)
        bin_src_folder = application_path
        root_folder_path = os.path.dirname(bin_src_folder)
        return root_folder_path

    def get_executable_path(self):
        return self.__EXECUTABLE_PATH__

    def get_config_folder_path(self):
        root_folder = self.get_root_folder()
        config_folder_path = os.path.join(root_folder, self.afsc.CONFIG_FOLDER_NAME)
        return config_folder_path

    def get_data_folder_path(self):
        root_folder = self.get_root_folder()
        data_folder_path = os.path.join(root_folder, self.afsc.DATA_FOLDER_NAME)
        return data_folder_path

    # TODO: Replace the following with proper path using the user config settings functionality after it is implemented
    def get_user_hrsa_data_workspace_path(self):
        root_folder = self.get_root_folder()
        user_hrsa_data_workspace_path = os.path.join(root_folder, 'HRSAData')
        return user_hrsa_data_workspace_path

    def reset_user_data(self):
        # Delete DPG ini file
        root_folder = self.get_root_folder()
        config_folder_path = os.path.join(root_folder, self.afsc.CONFIG_FOLDER_NAME)
        dpg_ini_file_path = os.path.join(config_folder_path, self.afsc.DPG_INI_FILE_NAME)
        if dpg_ini_file_path is not None and dpg_ini_file_path != '':
            dpg_ini_file = pathlib.Path(dpg_ini_file_path)
            if dpg_ini_file.exists():
                os.remove(dpg_ini_file_path)

    # ===================== START UI Layout Config methods =====================

    def get_dpg_ini_file_path(self):
        root_folder = self.get_root_folder()
        config_folder_path = os.path.join(root_folder, self.afsc.CONFIG_FOLDER_NAME)
        dpg_ini_file_path = os.path.join(config_folder_path, self.afsc.DPG_INI_FILE_NAME)
        dpg_ini_file = pathlib.Path(dpg_ini_file_path)
        if dpg_ini_file.exists():
            return dpg_ini_file_path
        else:
            default_dpg_ini_file_path = self.get_default_dpg_ini_file_path()
            if default_dpg_ini_file_path is not None and default_dpg_ini_file_path != '':
                shutil.copy(default_dpg_ini_file_path, dpg_ini_file_path)
                return dpg_ini_file_path
        return ''

    def get_default_dpg_ini_file_path(self):
        root_folder = self.get_root_folder()
        config_folder_path = os.path.join(root_folder, self.afsc.CONFIG_FOLDER_NAME)
        default_dpg_ini_file_path = os.path.join(config_folder_path, self.afsc.CONFIG_DEFAULTS_FOLDER_NAME, self.afsc.DEFAULT_DPG_INI_FILE_NAME)
        default_dpg_ini_file = pathlib.Path(default_dpg_ini_file_path)
        if default_dpg_ini_file.exists():
            return default_dpg_ini_file_path
        return ''

    def reset_to_default_layout(self):
        dpg_ini_file_path = self.get_dpg_ini_file_path()
        default_dpg_ini_file_path = self.get_default_dpg_ini_file_path()
        dpg_ini_file = pathlib.Path(dpg_ini_file_path)
        if dpg_ini_file.exists():
            os.remove(dpg_ini_file_path)
        shutil.copy(default_dpg_ini_file_path, dpg_ini_file_path)

    # ===================== END UI Layout Config methods =====================

    # ===================== START Font related methods =====================
    def get_default_font_folder_path(self):
        root_folder = self.get_root_folder()
        asset_folder = os.path.join(root_folder, self.afsc.ASSETS_FOLDER_NAME)
        font_folder = os.path.join(asset_folder, self.afsc.FONTS_FOLDER_NAME)
        opensans_font_folder = os.path.join(font_folder, self.afsc.DEFAULT_FONT_FOLDER_NAME)
        return opensans_font_folder

    def get_default_font_file_path(self):
        default_font_file_path = os.path.join(self.get_default_font_folder_path(), self.afsc.DEFAULT_FONT_NAME)
        return default_font_file_path

    def get_default_font_size(self):
        return self.afsc.DEFAULT_FONT_SIZE

    def get_default_bold_font_file_path(self):
        default_font_file_path = os.path.join(self.get_default_font_folder_path(), self.afsc.DEFAULT_BOLD_FONT_NAME)
        return default_font_file_path

    def get_bold_default_font_size(self):
        return self.afsc.DEFAULT_BOLD_FONT_SIZE

    # ===================== END Font related methods =====================
