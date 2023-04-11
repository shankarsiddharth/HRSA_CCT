from app_logger.app_logger_file_system_constants import AppLoggerFileSystemConstants
from classes.singleton import Singleton


class AppFileSystemConstants(metaclass=Singleton):

    def __init__(self):
        self.alfsc: AppLoggerFileSystemConstants = AppLoggerFileSystemConstants()

        # region Constants

        # region File Constants
        # Default File Encoding
        self.DEFAULT_FILE_ENCODING = "utf-8"
        # endregion File Constants

        # region Application Constants
        # Application Folder Constants
        self.ASSETS_FOLDER_NAME = "assets"
        self.BINARY_FOLDER_NAME = "bin"
        self.CONFIG_FOLDER_NAME = "config"
        self.DATA_FOLDER_NAME = "data"
        self.SOURCE_FOLDER_NAME = "src"
        self.TESTS_FOLDER_NAME = "tests"

        # Assets Font Folder & File Constants
        self.FONTS_FOLDER_NAME = "fonts"
        # Assets Images Folder & File Constants
        self.ASSETS_IMAGES_FOLDER_NAME = "images"
        self.ASSETS_IMAGES_AVATARS_FOLDER_NAME = "avatars"
        # Assets Images Icons Folder & File Constants
        self.ASSETS_IMAGES_ICONS_FOLDER_NAME = "icons"
        self.ASSETS_IMAGES_ICONS_APP_FOLDER_NAME = "app"
        self.ASSETS_IMAGES_ICONS_APP_DEFAULT_SMALL_ICON_FILE_NAME = "dpg.default.small.ico"
        self.ASSETS_IMAGES_ICONS_APP_DEFAULT_LARGE_ICON_FILE_NAME = "dpg.default.large.ico"

        # region Binary Folder & File Constants
        self.BINARY_INKLECATE_FOLDER_NAME = "inklecate"
        self.BINARY_INKY_FOLDER_NAME = "Inky"

        self.WINDOWS_BINARY_FOLDER_NAME = "Win64"
        self.LINUX_BINARY_FOLDER_NAME = "Linux"
        self.MACOS_BINARY_FOLDER_NAME = "Mac"

        self.DEFAULT_WINDOWS_INKLECATE_EXECUTABLE_FILE_NAME = "inklecate.exe"
        self.DEFAULT_LINUX_INKLECATE_EXECUTABLE_FILE_NAME = "inklecate"
        self.DEFAULT_MACOS_INKLECATE_EXECUTABLE_NAME = "inklecate"

        self.DEFAULT_WINDOWS_INKY_EXECUTABLE_FILE_NAME = "Inky.exe"
        self.DEFAULT_LINUX_INKY_EXECUTABLE_FILE_NAME = "Inky"
        self.DEFAULT_MACOS_INKY_EXECUTABLE_NAME = "Inky"
        # endregion Binary Folder & File Constants

        # Config CCT Folder & File Constants - CCT stands for "Content Creation Tool"
        self.CONFIG_CCT_FOLDER_NAME = "cct"
        # Application Config File Constants
        self.DEFAULT_CONFIG_CCT_APP_CONFIG_JSON_FILE_NAME = "app.config.default.json"

        # Config DPG Folder & File Constants - DPG stands for "Dear PyGui"
        self.CONFIG_DPG_FOLDER_NAME = "dpg"
        # DearPyGUI INI File Constants
        self.DEFAULT_CONFIG_DPG_INI_FILE_NAME = "dpg.default.ini"

        # Config Service Provider Folder & File Constants
        self.CONFIG_SERVICE_PROVIDERS_FOLDER_NAME = "service_providers"
        self.CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_FOLDER_NAME = "google_cloud"
        self.DEFAULT_CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE_NAME = "sapk.default.json"  # Google Cloud Service Account Private Key JSON File

        # Data Folder & File Constants
        self.DATA_IMAGES_FOLDER_NAME = "images"
        self.DATA_SCENARIO_TEMPLATE_FOLDER_NAME = "scenario_template"
        self.DATA_IMAGES_AVATARS_FOLDER_NAME = "avatars"

        # endregion Application Constants

        # region Application User Data Constants
        # AUD stands for Application User Data
        self.AUD_ROOT_FOLDER_NAME = self.alfsc.AUD_ROOT_FOLDER_NAME

        # Application User Config & File Constants
        self.AUD_CONFIG_APP_CONFIG_JSON_FILE_NAME = "app.config.json"
        self.AUD_CONFIG_DPG_INI_FILE_NAME = "dpg.ini"
        self.AUD_CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE_NAME = "sapk.json"  # Google Cloud Service Account Private Key JSON File
        # endregion Application User Data Constants

        # region Application User HRSAData Constants
        # HRSA Data Folder & File Constants
        self.HRSA_DATA_WORKSPACE_FOLDER_NAME = "HRSAData"
        # endregion Application User HRSAData Constants

        # region Application Fonts Constants
        self.DEFAULT_FONT_FOLDER_NAME = "opensans"
        self.DEFAULT_FONT_NAME = "OpenSans-Regular.ttf"
        self.DEFAULT_FONT_SIZE = 18
        self.DEFAULT_BOLD_FONT_NAME = "OpenSans-Bold.ttf"
        self.DEFAULT_BOLD_FONT_SIZE = 16
        # endregion Application Fonts Constants

        # region Application Assets Images File Constants
        self.DEFAULT_ERROR_AVATAR_IMAGE_FILE_NAME = "error.png"
        # endregion Application Assets Images File Constants

        # endregion Constants

        # region Unity Project Data File Constants
        self.CHARACTER_MODEL_DATA_FILE_NAME = "CharacterModelData.json"
        # endregion Unity Project Data File Constants
