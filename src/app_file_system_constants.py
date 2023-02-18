import threading


class AppFileSystemConstants(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    print('Creating the Logger object')
                    cls._instance = super(AppFileSystemConstants, cls).__new__(cls)
                    cls._instance.__initialize__()
        return cls._instance

    def __initialize__(self):

        # Constants

        # ========================== START Application Constants ===================================
        # Application Folder Constants
        self.ASSETS_FOLDER_NAME = "assets"
        self.BINARY_FOLDER_NAME = "bin"
        self.CONFIG_FOLDER_NAME = "config"
        self.CONFIG_DEFAULTS_FOLDER_NAME = "defaults"
        self.DATA_FOLDER_NAME = "data"
        self.DATA_DEFAULTS_FOLDER_NAME = "defaults"
        self.LOG_FOLDER_NAME = "logs"
        self.SOURCE_FOLDER_NAME = "src"
        self.FONTS_FOLDER_NAME = "fonts"

        # Log File Constants
        self.LOG_FILE_NAME = "cct.log"
        self.BACKUP_LOG_FILE_NAME = "cct.backup.log"

        # DearPyGUI INI File Constants
        self.DEFAULT_DPG_INI_FILE_NAME = "dpg.default.ini"
        self.DPG_INI_FILE_NAME = "dpg.ini"

        # Application Config File Constants
        self.DEFAULT_APP_CONFIG_INI_FILE_NAME = "app.config.default.ini"
        self.APP_CONFIG_INI_FILE_NAME = "app.config.ini"
        # Application Config File Version Key
        self.KEY_APP_CONFIG_VERSION: str = "APP_CONFIG_VERSION"

        # ========================== END Application Constants ===================================

        # ========================== START Application Fonts Constants ===================================

        self.DEFAULT_FONT_FOLDER_NAME = "opensans"
        self.DEFAULT_FONT_NAME = "OpenSans-Regular.ttf"
        self.DEFAULT_FONT_SIZE = 18
        self.DEFAULT_BOLD_FONT_NAME = "OpenSans-Bold.ttf"
        self.DEFAULT_BOLD_FONT_SIZE = 16

        # ========================== END Application Fonts Constants ===================================