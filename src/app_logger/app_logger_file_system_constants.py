import threading

from app_debug.app_debug import IS_DEBUG_MODE_ENABLED


class AppLoggerFileSystemConstants(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppLoggerFileSystemConstants, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if IS_DEBUG_MODE_ENABLED:
                        print("AppLoggerFileSystemConstants.__new__()")
        return cls._instance

    def __initialize__(self):

        # region Logger Constants
        self.LOG_FOLDER_NAME = "log"

        # Log Folder & File Constants
        self.LOG_FILE_NAME = "cct.log"
        self.BACKUP_LOG_FILE_NAME = "cct.backup.log"

        # endregion Logger Constants

        # region Application User Data Constants
        # AUD stands for Application User Data
        self.AUD_ROOT_FOLDER_NAME = ".hrsacct"
        # endregion Application User Data Constants
