import sys

from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_logger.app_logger import AppLogger

log = AppLogger()
# HRSA File System Constants
hfsc: AppFileSystemConstants = AppFileSystemConstants()
# HRSA File System
hfs: AppFileSystem = AppFileSystem()
# # HRSA Data File System Constants
# hdfsc: HRSADataFileSystemConstants = HRSADataFileSystemConstants()
# # HRSA Data File System
# hdfs: HRSADataFileSystem = HRSADataFileSystem()

# Global Variables
default_language_code = "en-US"
none_language_code = '(none)'

language_list = [
    '(none)',
    'en-US',
    'es-US'
]

audio_generation_language_list = [
    '(none)',
    'en-US',
    'es-US',
    'es-ES'
]

option_text_prefixes = [
    'A',
    'B',
    'C',
    'D',
    'E',
    '1',
    '2',
    '3',
    '4',
    '5',
]

dialogue_regular_expression = r"\".*?\""
option_regular_expression = r"[*](.*)\[(.*?(?=`))`(.*?(?=`))`(.*?(?=`))`(.*?(?=`|\]))(?:`(.*)])?"
option_display_text_regular_expression = r"\s*[A-Za-z0-9]+\s*[\.](.*)"

# Scenario Folder Cache
app_data = dict()

connect_to_cloud = False

if sys.flags.dev_mode:
    print("hrsa_cc_globals.__init__()")
