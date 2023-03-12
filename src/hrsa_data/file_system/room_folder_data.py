import os
import pathlib
from dataclasses import dataclass, field

from .audio_folder_data import AudioFolderData
from .file_system_result_data import FileSystemResultData
from .hrsa_data_file_system_constants import HRSADataFileSystemConstants

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class RoomFolderData:
    # Room Name
    room_name: str = field(default='')
    # Room Folder Path - Root
    folder_root_path: str = field(default='')
    # Audio Folder Data
    audio_folder_data: AudioFolderData = field(default_factory=AudioFolderData)
    # Dialogue ink file path
    dialogue_ink_file_path: str = field(default='')
    # Dialogue ink JSON file path
    dialogue_ink_json_file_path: str = field(default='')

    def initialize_room_folder_data(self):
        root_path = self.folder_root_path
        dir_list = os.listdir(root_path)
        if len(dir_list) == 0:
            return False
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(root_path, dir_item)
            if os.path.isdir(dir_item_path):
                if dir_item == __hdfsc__.AUDIO_FOLDER_NAME:
                    self.audio_folder_data.audio_folder_root_path = dir_item_path
                    if not self.audio_folder_data.initialize_audio_folder_data():
                        # TODO: Log error / warning - Audio Folder Empty
                        pass
            if os.path.isfile(dir_item_path):
                if dir_item == __hdfsc__.DIALOGUE_INK_FILE_NAME:
                    self.dialogue_ink_file_path = dir_item_path
                if dir_item == __hdfsc__.DIALOGUE_INK_JSON_FILE_NAME:
                    self.dialogue_ink_json_file_path = dir_item_path
        return True

    def create_new_room_folder(self) -> FileSystemResultData:
        # Create Room Folder
        new_room_folder_path = pathlib.Path(self.folder_root_path)
        if new_room_folder_path.exists():
            return FileSystemResultData(is_success=False, error_message='Room Folder Already Exists')
        new_room_folder_path.mkdir()
        # Create Audio Folder
        self.audio_folder_data.audio_folder_root_path = os.path.join(self.folder_root_path, __hdfsc__.AUDIO_FOLDER_NAME)
        file_system_result_data: FileSystemResultData = self.audio_folder_data.create_new_audio_folder()
        if not file_system_result_data.is_success:
            return file_system_result_data
        # Create Dialogue Ink File
        self.dialogue_ink_file_path = os.path.join(self.folder_root_path, __hdfsc__.DIALOGUE_INK_FILE_NAME)
        new_dialogue_ink_file_path = pathlib.Path(self.dialogue_ink_file_path)
        if new_dialogue_ink_file_path.exists():
            return FileSystemResultData(is_success=False, error_message='Dialogue Ink File Already Exists')
        open(self.dialogue_ink_file_path, 'a').close()
        # Dialogue Ink JSON File Path
        self.dialogue_ink_json_file_path = os.path.join(self.folder_root_path, __hdfsc__.DIALOGUE_INK_JSON_FILE_NAME)
        return FileSystemResultData(is_success=True)
