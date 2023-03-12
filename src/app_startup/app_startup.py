from app_debug.app_debug import IS_DEBUG_MODE_ENABLED
from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants


class AppStartup:
    def __init__(self):
        self.afsc: AppFileSystemConstants = AppFileSystemConstants()
        self.afs: AppFileSystem = AppFileSystem()

        try:
            self.afs.initialize_user_dir()
            self.afs.initialize_user_config_files()
            self.afs.create_hrsa_data_workspace_folder()
        except Exception as e:
            print("Error initializing user directory and config files.")
            raise e

        if IS_DEBUG_MODE_ENABLED:
            print("AppStartup.__init__()")
