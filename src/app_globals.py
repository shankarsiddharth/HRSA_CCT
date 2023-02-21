import sys

from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_logger.app_logger import AppLogger
from app_file_dialog import AppFileDialog

afsc: AppFileSystemConstants = AppFileSystemConstants()
afs: AppFileSystem = AppFileSystem()
log: AppLogger = AppLogger()

file_dialog: AppFileDialog = AppFileDialog()
user_selected_file_path: str = ''
user_selected_folder_path: str = ''

if sys.flags.dev_mode:
    print("AppGlobals.__init__()")
