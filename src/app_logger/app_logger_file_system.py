import os
import pathlib
import sys
import threading
import traceback

from app_debug.app_debug import IS_DEBUG_MODE_ENABLED
from .app_logger_file_system_constants import AppLoggerFileSystemConstants


class AppLoggerFileSystem(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppLoggerFileSystem, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if IS_DEBUG_MODE_ENABLED:
                        print("AppLoggerFileSystem.__new__()")
        return cls._instance

    def __initialize__(self):
        self.alfsc: AppLoggerFileSystemConstants = AppLoggerFileSystemConstants()
        self.__EXECUTABLE_FILE_PATH__ = None
        self.__root_folder_path__ = None
        self.__initialize_root_folder_path__()
        self.__user_home_folder_path__ = None
        self.__initialize_user_home_folder_path__()
        self.__log_folder_path__ = None

    def __initialize_root_folder_path__(self):
        application_path = ""
        if getattr(sys, 'frozen', False):
            self.__EXECUTABLE_FILE_PATH__ = os.path.realpath(sys.executable)
            application_path = os.path.dirname(sys.executable)
        elif __file__:
            current_file_dir_path = os.path.dirname(__file__)
            application_path = os.path.dirname(current_file_dir_path)
        bin_src_folder = application_path  # binaries folder or source folder
        self.__root_folder_path__ = os.path.dirname(bin_src_folder)

    def get_root_folder_path(self):
        if self.__root_folder_path__ is None:
            self.__initialize_root_folder_path__()
        return self.__root_folder_path__

    def __initialize_user_home_folder_path__(self):
        self.__user_home_folder_path__ = pathlib.Path.home()

    def get_user_home_folder_path(self):
        if self.__user_home_folder_path__ is None:
            self.__initialize_user_home_folder_path__()
        return self.__user_home_folder_path__

    def get_default_log_folder_path(self):
        log_folder_path = os.path.join(self.__root_folder_path__, self.alfsc.LOG_FOLDER_NAME)
        return log_folder_path

    def get_default_log_file_path(self):
        log_folder_path = self.get_default_log_folder_path()
        default_log_file_path = os.path.join(log_folder_path, self.alfsc.LOG_FILE_NAME)
        return default_log_file_path

    def get_default_backup_log_file_path(self):
        log_folder_path = self.get_default_log_folder_path()
        default_backup_log_file_path = os.path.join(log_folder_path, self.alfsc.BACKUP_LOG_FILE_NAME)
        return default_backup_log_file_path

    def get_app_user_data_root_folder_path(self):
        user_home_folder_path = self.__user_home_folder_path__
        app_user_data_root_folder_path = os.path.join(user_home_folder_path, self.alfsc.AUD_ROOT_FOLDER_NAME)
        return app_user_data_root_folder_path

    # region App User Data methods

    def get_app_user_data_log_folder_path(self):
        app_user_data_root_folder_path = self.get_app_user_data_root_folder_path()
        app_user_data_log_folder_path = os.path.join(app_user_data_root_folder_path, self.alfsc.LOG_FOLDER_NAME)
        return app_user_data_log_folder_path

    def get_app_user_data_log_file_path(self):
        app_user_data_log_folder_path = self.get_app_user_data_log_folder_path()
        app_user_data_log_file_path = os.path.join(app_user_data_log_folder_path, self.alfsc.LOG_FILE_NAME)
        return app_user_data_log_file_path

    def get_app_user_data_backup_log_file_path(self):
        app_user_data_log_folder_path = self.get_app_user_data_log_folder_path()
        app_user_data_backup_log_file_path = os.path.join(app_user_data_log_folder_path, self.alfsc.BACKUP_LOG_FILE_NAME)
        return app_user_data_backup_log_file_path

    # endregion App User Data methods
    def initialize_log_folder(self) -> str:
        print("Checking log folder...")
        self.__log_folder_path__ = ''
        # Get the log folder path based on the debug mode.
        if IS_DEBUG_MODE_ENABLED:
            self.__log_folder_path__ = self.get_default_log_folder_path()
        else:
            self.__log_folder_path__ = self.get_app_user_data_log_folder_path()

        if self.__log_folder_path__ == '':
            raise Exception("Log folder path is empty.")

        log_folder = pathlib.Path(self.__log_folder_path__)
        if not log_folder.exists():
            print("Log folder does not exist. Creating it.")
            print("Creating log folder: " + self.__log_folder_path__)
            try:
                os.makedirs(self.__log_folder_path__, exist_ok=True)
            except OSError as e:
                traceback_string = traceback.format_exc()
                exception_message = ("Creation of the log folder %s failed" % self.__log_folder_path__) + "\n" + str(e) + "\n" + traceback_string
                print(exception_message)
                raise Exception(exception_message)
            except Exception as e:
                traceback_string = traceback.format_exc()
                exception_message = ("Creation of the log folder %s failed" % self.__log_folder_path__) + "\n" + str(e) + "\n" + traceback_string
                print(exception_message)
                raise Exception(exception_message)

        return self.__log_folder_path__
