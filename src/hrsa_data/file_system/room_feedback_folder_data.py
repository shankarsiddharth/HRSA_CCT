import os
from dataclasses import dataclass, field

from .hrsa_data_file_system_constants import HRSADataFileSystemConstants
from .audio_folder_data import AudioFolderData

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class RoomFeedbackFolderData:
    # Room Folder Path - Root
    room_feedback_folder_root_path: str = field(default='')
    # Audio Folder Data
    room_feedback_audio_folder_data: AudioFolderData = field(default_factory=AudioFolderData)
    # Feedback ink file path
    feedback_ink_file_path: str = field(default='')
    # Feedback ink JSON file path
    feedback_ink_json_file_path: str = field(default='')

    def initialize_room_feedback_folder_data(self):
        root_path = self.room_feedback_folder_root_path
        dir_list = os.listdir(root_path)
        if len(dir_list) == 0:
            return False
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(root_path, dir_item)
            if os.path.isdir(dir_item_path):
                if dir_item == __hdfsc__.AUDIO_FOLDER_NAME:
                    self.room_feedback_audio_folder_data.audio_folder_root_path = dir_item_path
                    if not self.room_feedback_audio_folder_data.initialize_audio_folder_data():
                        # TODO: Log error / warning - Audio Folder Content Error
                        pass
            if os.path.isfile(dir_item_path):
                if dir_item == __hdfsc__.FEEDBACK_INK_FILE_NAME:
                    self.feedback_ink_file_path = dir_item_path
                if dir_item == __hdfsc__.FEEDBACK_INK_JSON_FILE_NAME:
                    self.feedback_ink_json_file_path = dir_item_path
        return True
