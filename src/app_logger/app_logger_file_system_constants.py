from classes.singleton import Singleton


class AppLoggerFileSystemConstants(metaclass=Singleton):

    def __init__(self):
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
