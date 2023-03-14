import os
import pathlib
import shutil
import threading

from app_debug.app_debug import IS_DEBUG_MODE_ENABLED
from app_logger.app_logger_file_system import AppLoggerFileSystem
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
                    if IS_DEBUG_MODE_ENABLED:
                        print("AppFileSystem.__new__()")
        return cls._instance

    def __initialize__(self):
        self.afsc: AppFileSystemConstants = AppFileSystemConstants()
        self.alfs: AppLoggerFileSystem = AppLoggerFileSystem()
        self.__root_folder_path__ = self.alfs.get_root_folder_path()
        self.__user_home_folder_path__ = self.alfs.get_user_home_folder_path()
        self.__app_user_data_root_folder_path__ = self.alfs.get_app_user_data_root_folder_path()
        self.default_app_icon_small_file_path = ''
        self.default_app_icon_large_file_path = ''
        self.__initialize_default_app_icon_file_paths__()

    def get_root_folder_path(self):
        return self.__root_folder_path__

    def get_user_home_folder_path(self):
        return self.__user_home_folder_path__

    def get_default_assets_folder_path(self):
        assets_folder_path = os.path.join(self.__root_folder_path__, self.afsc.ASSETS_FOLDER_NAME)
        return assets_folder_path

    def get_default_binary_folder_path(self):
        bin_folder_path = os.path.join(self.__root_folder_path__, self.afsc.BINARY_FOLDER_NAME)
        return bin_folder_path

    def get_default_config_folder_path(self):
        config_folder_path = os.path.join(self.__root_folder_path__, self.afsc.CONFIG_FOLDER_NAME)
        return config_folder_path

    def get_default_data_folder_path(self):
        data_folder_path = os.path.join(self.__root_folder_path__, self.afsc.DATA_FOLDER_NAME)
        return data_folder_path

    def get_default_source_folder_path(self):
        src_folder_path = os.path.join(self.__root_folder_path__, self.afsc.SOURCE_FOLDER_NAME)
        return src_folder_path

    def get_default_tests_folder_path(self):
        tests_folder_path = os.path.join(self.__root_folder_path__, self.afsc.TESTS_FOLDER_NAME)
        return tests_folder_path

    def get_default_assets_font_folder_path(self):
        asset_folder_path = self.get_default_assets_folder_path()
        default_assets_font_folder_path = os.path.join(asset_folder_path, self.afsc.FONTS_FOLDER_NAME)
        return default_assets_font_folder_path

    def get_default_assets_images_folder_path(self):
        asset_folder_path = self.get_default_assets_folder_path()
        default_assets_image_folder_path = os.path.join(asset_folder_path, self.afsc.ASSETS_IMAGES_FOLDER_NAME)
        return default_assets_image_folder_path

    def get_default_assets_images_avatars_folder_path(self):
        assets_images_folder_path = self.get_default_assets_images_folder_path()
        default_assets_image_avatar_folder_path = os.path.join(assets_images_folder_path, self.afsc.ASSETS_IMAGES_AVATARS_FOLDER_NAME)
        return default_assets_image_avatar_folder_path

    def get_default_assets_images_avatars_file_path(self, image_file_name) -> str:
        assets_images_avatars_folder_path = self.get_default_assets_images_avatars_folder_path()
        image_path = os.path.join(assets_images_avatars_folder_path, image_file_name)
        return image_path

    def get_default_assets_images_icons_folder_path(self):
        assets_images_folder_path = self.get_default_assets_images_folder_path()
        default_assets_image_icon_folder_path = os.path.join(assets_images_folder_path, self.afsc.ASSETS_IMAGES_ICONS_FOLDER_NAME)
        return default_assets_image_icon_folder_path

    def get_default_assets_images_icons_app_folder_path(self):
        assets_images_icons_folder_path = self.get_default_assets_images_icons_folder_path()
        default_assets_image_icon_app_folder_path = os.path.join(assets_images_icons_folder_path, self.afsc.ASSETS_IMAGES_ICONS_APP_FOLDER_NAME)
        return default_assets_image_icon_app_folder_path

    def get_default_app_icon_small_file_path(self):
        assets_images_icons_app_folder_path = self.get_default_assets_images_icons_app_folder_path()
        default_app_icon_small_file_path = os.path.join(assets_images_icons_app_folder_path, self.afsc.ASSETS_IMAGES_ICONS_APP_DEFAULT_SMALL_ICON_FILE_NAME)
        return default_app_icon_small_file_path

    def get_default_app_icon_large_file_path(self):
        assets_images_icons_app_folder_path = self.get_default_assets_images_icons_app_folder_path()
        default_app_icon_large_file_path = os.path.join(assets_images_icons_app_folder_path, self.afsc.ASSETS_IMAGES_ICONS_APP_DEFAULT_LARGE_ICON_FILE_NAME)
        return default_app_icon_large_file_path

    def __initialize_default_app_icon_file_paths__(self):
        self.default_app_icon_small_file_path = self.get_default_app_icon_small_file_path()
        self.default_app_icon_large_file_path = self.get_default_app_icon_large_file_path()

    def get_default_config_cct_folder_path(self):
        config_folder_path = self.get_default_config_folder_path()
        default_config_cct_folder_path = os.path.join(config_folder_path, self.afsc.CONFIG_CCT_FOLDER_NAME)
        return default_config_cct_folder_path

    def get_default_config_cct_app_config_json_file_path(self):
        config_cct_folder_path = self.get_default_config_cct_folder_path()
        default_config_cct_app_config_json_file_path = os.path.join(config_cct_folder_path, self.afsc.DEFAULT_CONFIG_CCT_APP_CONFIG_JSON_FILE_NAME)
        return default_config_cct_app_config_json_file_path

    def get_default_config_dpg_folder_path(self):
        config_folder_path = self.get_default_config_folder_path()
        default_config_dpg_folder_path = os.path.join(config_folder_path, self.afsc.CONFIG_DPG_FOLDER_NAME)
        return default_config_dpg_folder_path

    def get_default_config_dpg_ini_file_path(self):
        config_dpg_folder_path = self.get_default_config_dpg_folder_path()
        default_config_dpg_ini_file_path = os.path.join(config_dpg_folder_path, self.afsc.DEFAULT_CONFIG_DPG_INI_FILE_NAME)
        return default_config_dpg_ini_file_path

    def get_default_config_service_providers_folder_path(self):
        config_folder_path = self.get_default_config_folder_path()
        service_providers_folder_path = os.path.join(config_folder_path, self.afsc.CONFIG_SERVICE_PROVIDERS_FOLDER_NAME)
        return service_providers_folder_path

    def get_default_service_providers_google_cloud_folder_path(self):
        service_providers_folder_path = self.get_default_config_service_providers_folder_path()
        google_cloud_folder_path = os.path.join(service_providers_folder_path, self.afsc.CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_FOLDER_NAME)
        return google_cloud_folder_path

    def get_default_service_providers_google_cloud_credentials_file_path(self):
        google_cloud_folder_path = self.get_default_service_providers_google_cloud_folder_path()
        credentials_file_path = os.path.join(google_cloud_folder_path, self.afsc.DEFAULT_CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE_NAME)
        return credentials_file_path

    def get_default_data_images_folder_path(self):
        data_folder_path = self.get_default_data_folder_path()
        default_data_images_folder_path = os.path.join(data_folder_path, self.afsc.DATA_IMAGES_FOLDER_NAME)
        return default_data_images_folder_path

    def get_default_data_images_avatars_folder_path(self):
        data_images_folder_path = self.get_default_data_images_folder_path()
        default_data_images_avatars_folder_path = os.path.join(data_images_folder_path, self.afsc.DATA_IMAGES_AVATARS_FOLDER_NAME)
        return default_data_images_avatars_folder_path

    # region App User Data methods
    def get_app_user_data_config_folder_path(self):
        app_user_data_config_folder_path = os.path.join(self.__app_user_data_root_folder_path__, self.afsc.CONFIG_FOLDER_NAME)
        return app_user_data_config_folder_path

    def get_app_user_data_config_cct_folder_path(self):
        app_user_data_config_folder_path = self.get_app_user_data_config_folder_path()
        app_user_data_config_cct_folder_path = os.path.join(app_user_data_config_folder_path, self.afsc.CONFIG_CCT_FOLDER_NAME)
        return app_user_data_config_cct_folder_path

    def get_app_user_data_config_cct_app_config_json_file_path(self):
        app_user_data_config_cct_folder_path = self.get_app_user_data_config_cct_folder_path()
        app_user_data_config_cct_app_config_json_file_path = os.path.join(app_user_data_config_cct_folder_path, self.afsc.AUD_CONFIG_APP_CONFIG_JSON_FILE_NAME)
        return app_user_data_config_cct_app_config_json_file_path

    def get_app_user_data_config_dpg_folder_path(self):
        app_user_data_config_folder_path = self.get_app_user_data_config_folder_path()
        app_user_data_config_dpg_folder_path = os.path.join(app_user_data_config_folder_path, self.afsc.CONFIG_DPG_FOLDER_NAME)
        return app_user_data_config_dpg_folder_path

    def get_app_user_data_config_dpg_ini_file_path(self):
        app_user_data_config_dpg_folder_path = self.get_app_user_data_config_dpg_folder_path()
        app_user_data_config_dpg_ini_file_path = os.path.join(app_user_data_config_dpg_folder_path, self.afsc.AUD_CONFIG_DPG_INI_FILE_NAME)
        return app_user_data_config_dpg_ini_file_path

    def get_app_user_data_config_service_providers_folder_path(self):
        app_user_data_config_folder_path = self.get_app_user_data_config_folder_path()
        app_user_data_config_service_providers_folder_path = os.path.join(app_user_data_config_folder_path, self.afsc.CONFIG_SERVICE_PROVIDERS_FOLDER_NAME)
        return app_user_data_config_service_providers_folder_path

    def get_app_user_data_config_service_providers_google_cloud_folder_path(self):
        app_user_data_config_service_providers_folder_path = self.get_app_user_data_config_service_providers_folder_path()
        app_user_data_config_service_providers_google_cloud_folder_path = os.path.join(app_user_data_config_service_providers_folder_path,
                                                                                       self.afsc.CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_FOLDER_NAME)
        return app_user_data_config_service_providers_google_cloud_folder_path

    def get_app_user_data_config_service_providers_google_cloud_credentials_file_path(self):
        app_user_data_config_service_providers_google_cloud_folder_path = self.get_app_user_data_config_service_providers_google_cloud_folder_path()
        app_user_data_config_service_providers_google_cloud_credentials_file_path = os.path.join(
            app_user_data_config_service_providers_google_cloud_folder_path, self.afsc.AUD_CONFIG_SERVICE_PROVIDERS_GOOGLE_CLOUD_SERVICE_ACCOUNT_FILE_NAME)
        return app_user_data_config_service_providers_google_cloud_credentials_file_path

    # endregion App User Data methods

    # region HRSA Data Workspace methods

    def __get_default_hrsa_data_workspace_folder_path__(self):
        user_hrsa_data_workspace_path = os.path.join(self.__root_folder_path__, self.afsc.HRSA_DATA_WORKSPACE_FOLDER_NAME)
        return user_hrsa_data_workspace_path

    def __get_user_hrsa_data_workspace_path__(self):
        user_home_folder_path = self.__user_home_folder_path__
        user_hrsa_data_workspace_path = os.path.join(user_home_folder_path, self.afsc.HRSA_DATA_WORKSPACE_FOLDER_NAME)
        return user_hrsa_data_workspace_path

    # TODO: Replace the following with proper path using the user config settings functionality after it is implemented
    def get_hrsa_data_workspace_folder_path(self):
        if IS_DEBUG_MODE_ENABLED:
            return self.__get_default_hrsa_data_workspace_folder_path__()
        return self.__get_user_hrsa_data_workspace_path__()

    # endregion HRSA Data Workspace methods

    def reset_user_data(self):
        # TODO: Implement this method
        pass

    def get_google_cloud_credentials_file_path(self) -> str | None:
        # TODO: Replace the following with proper path using the user config settings functionality after it is implemented
        #   Use the default path if the user has not specified a path
        #   If the user has specified a path, use that path
        #   This config setting should be stored in the user config file => app.config.ini
        google_cloud_service_account_file_path: str = ''

        if IS_DEBUG_MODE_ENABLED:
            google_cloud_service_account_file_path = self.get_default_service_providers_google_cloud_credentials_file_path()
        else:
            google_cloud_service_account_file_path = self.get_app_user_data_config_service_providers_google_cloud_credentials_file_path()

        if google_cloud_service_account_file_path != '':
            google_cloud_service_account_file = pathlib.Path(google_cloud_service_account_file_path)
            if google_cloud_service_account_file.exists():
                return google_cloud_service_account_file_path

        return None

    # region UI Layout Config methods

    def reset_to_default_layout(self):
        # TODO: Implement the following method
        # dpg_ini_file_path = self.get_dpg_ini_file_path()
        # default_dpg_ini_file_path = self.get_default_dpg_ini_file_path()
        # dpg_ini_file = pathlib.Path(dpg_ini_file_path)
        # if dpg_ini_file.exists():
        #     os.remove(dpg_ini_file_path)
        # shutil.copy(default_dpg_ini_file_path, dpg_ini_file_path)
        pass

    # endregion UI Layout Config methods

    # region Font related methods
    def get_default_font_folder_path(self):
        default_assets_font_folder_path = self.get_default_assets_font_folder_path()
        default_font_folder_path = os.path.join(default_assets_font_folder_path, self.afsc.DEFAULT_FONT_FOLDER_NAME)
        return default_font_folder_path

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

    # endregion Font related methods

    def create_user_dir(self):
        user_dir = pathlib.Path(self.__app_user_data_root_folder_path__)
        if not user_dir.exists():
            user_dir.mkdir(parents=True, exist_ok=True)

    def create_user_dir_config_cct(self):
        user_dir_config_cct_path = self.get_app_user_data_config_cct_folder_path()
        user_dir_config_cct = pathlib.Path(user_dir_config_cct_path)
        if not user_dir_config_cct.exists():
            user_dir_config_cct.mkdir(parents=True, exist_ok=True)

    def create_user_dir_config_dpg(self):
        user_dir_config_dpg_path = self.get_app_user_data_config_dpg_folder_path()
        user_dir_config_dpg = pathlib.Path(user_dir_config_dpg_path)
        if not user_dir_config_dpg.exists():
            user_dir_config_dpg.mkdir(parents=True, exist_ok=True)

    def create_user_dir_config_service_providers_google_cloud(self):
        user_dir_config_service_providers_google_cloud_path = self.get_app_user_data_config_service_providers_google_cloud_folder_path()
        user_dir_config_service_providers_google_cloud = pathlib.Path(user_dir_config_service_providers_google_cloud_path)
        if not user_dir_config_service_providers_google_cloud.exists():
            user_dir_config_service_providers_google_cloud.mkdir(parents=True, exist_ok=True)

    def initialize_user_dir(self):
        # Check for the user directory
        self.create_user_dir()
        self.create_user_dir_config_cct()
        self.create_user_dir_config_dpg()
        self.create_user_dir_config_service_providers_google_cloud()

    def create_app_user_data_config_json_file(self):
        app_user_data_config_json_file_path = self.get_app_user_data_config_cct_app_config_json_file_path()
        app_user_data_config_json_file = pathlib.Path(app_user_data_config_json_file_path)
        if not app_user_data_config_json_file.exists():
            # Copy default app config json file to user data folder
            default_app_config_json_file_path = self.get_default_config_cct_app_config_json_file_path()
            default_app_config_json_file = pathlib.Path(default_app_config_json_file_path)
            if default_app_config_json_file.exists():
                shutil.copyfile(default_app_config_json_file_path, app_user_data_config_json_file_path)
            else:
                raise FileNotFoundError(f'Default app config json file not found: {default_app_config_json_file_path}')

    def create_app_user_data_dpg_ini_file(self):
        app_user_data_dpg_ini_file_path = self.get_app_user_data_config_dpg_ini_file_path()
        app_user_data_dpg_ini_file = pathlib.Path(app_user_data_dpg_ini_file_path)
        if not app_user_data_dpg_ini_file.exists():
            # Copy default dpg ini file to user data folder
            default_dpg_ini_file_path = self.get_default_config_dpg_ini_file_path()
            default_dpg_ini_file = pathlib.Path(default_dpg_ini_file_path)
            if default_dpg_ini_file.exists():
                shutil.copyfile(default_dpg_ini_file_path, app_user_data_dpg_ini_file_path)
            else:
                raise FileNotFoundError(f'Default dpg ini file not found: {default_dpg_ini_file_path}')

    def create_app_user_data_google_cloud_credentials_json_file(self):
        app_user_data_google_cloud_credentials_json_file_path = self.get_app_user_data_config_service_providers_google_cloud_credentials_file_path()
        app_user_data_google_cloud_credentials_json_file = pathlib.Path(app_user_data_google_cloud_credentials_json_file_path)
        if not app_user_data_google_cloud_credentials_json_file.exists():
            # Copy default google cloud credentials json file to user data folder
            default_google_cloud_credentials_json_file_path = self.get_default_service_providers_google_cloud_credentials_file_path()
            default_google_cloud_credentials_json_file = pathlib.Path(default_google_cloud_credentials_json_file_path)
            if default_google_cloud_credentials_json_file.exists():
                shutil.copyfile(default_google_cloud_credentials_json_file_path, app_user_data_google_cloud_credentials_json_file_path)
            else:
                raise FileNotFoundError(f'Default Google Cloud Credentials file not found: {default_google_cloud_credentials_json_file_path}')

    def initialize_user_config_files(self):
        self.create_app_user_data_config_json_file()
        self.create_app_user_data_dpg_ini_file()
        self.create_app_user_data_google_cloud_credentials_json_file()

    def create_hrsa_data_workspace_folder(self):
        hrsa_data_workspace_folder_path = self.get_hrsa_data_workspace_folder_path()
        hrsa_data_workspace_folder = pathlib.Path(hrsa_data_workspace_folder_path)
        if not hrsa_data_workspace_folder.exists():
            hrsa_data_workspace_folder.mkdir(parents=True, exist_ok=True)
