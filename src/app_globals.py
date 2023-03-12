from app_debug.app_debug import IS_DEBUG_MODE_ENABLED
from app_file_dialog import AppFileDialog
from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_logger.app_logger import AppLogger

log: AppLogger = AppLogger()
afsc: AppFileSystemConstants = AppFileSystemConstants()
afs: AppFileSystem = AppFileSystem()

file_dialog: AppFileDialog = AppFileDialog()
user_selected_file_path: str = ''
user_selected_folder_path: str = ''

if IS_DEBUG_MODE_ENABLED:
    print("AppGlobals.__init__()")
