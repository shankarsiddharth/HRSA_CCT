import os
import pathlib
from dataclasses import dataclass, field

from .file_system_result_data import FileSystemResultData
from .hrsa_data_file_system_constants import HRSADataFileSystemConstants
from .room_feedback_folder_data import RoomFeedbackFolderData

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class FeedbackRoomFolderData:
    # Room Folder Path - Root
    feedback_room_folder_root_path: str = field(default='')
    # Break Room Feedback Folder Data
    break_room_feedback_folder_data: RoomFeedbackFolderData = field(default_factory=RoomFeedbackFolderData)
    # Patient Room Feedback Folder Data
    patient_room_feedback_folder_data: RoomFeedbackFolderData = field(default_factory=RoomFeedbackFolderData)

    def initialize_feedback_room_folder_data(self):
        root_path = self.feedback_room_folder_root_path
        dir_list = os.listdir(root_path)
        if len(dir_list) == 0:
            return False
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(root_path, dir_item)
            if os.path.isdir(dir_item_path):
                if dir_item == __hdfsc__.FEEDBACK_TYPE_BREAK_ROOM_NAME:
                    self.break_room_feedback_folder_data.room_feedback_folder_root_path = dir_item_path
                    if not self.break_room_feedback_folder_data.initialize_room_feedback_folder_data():
                        # TODO: Log error / warning - Break Room Feedback Folder Content Error
                        pass
                if dir_item == __hdfsc__.FEEDBACK_TYPE_PATIENT_ROOM_NAME:
                    self.patient_room_feedback_folder_data.room_feedback_folder_root_path = dir_item_path
                    if not self.patient_room_feedback_folder_data.initialize_room_feedback_folder_data():
                        # TODO: Log error / warning - Patient Room Feedback Folder Content Error
                        pass
        return True

    def create_new_feedback_room_folder(self) -> FileSystemResultData:
        feedback_room_folder_root_path = pathlib.Path(self.feedback_room_folder_root_path)
        if feedback_room_folder_root_path.exists():
            return FileSystemResultData(is_success=False, error_message='Feedback Room Folder Already Exists')
        feedback_room_folder_root_path.mkdir()

        self.break_room_feedback_folder_data.room_feedback_folder_root_path = os.path.join(self.feedback_room_folder_root_path, __hdfsc__.FEEDBACK_TYPE_BREAK_ROOM_NAME)
        file_system_result_data: FileSystemResultData = self.break_room_feedback_folder_data.create_new_room_feedback_folder()
        if not file_system_result_data.is_success:
            return file_system_result_data
        self.patient_room_feedback_folder_data.room_feedback_folder_root_path = os.path.join(self.feedback_room_folder_root_path, __hdfsc__.FEEDBACK_TYPE_PATIENT_ROOM_NAME)
        file_system_result_data: FileSystemResultData = self.patient_room_feedback_folder_data.create_new_room_feedback_folder()
        if not file_system_result_data.is_success:
            return file_system_result_data
        return FileSystemResultData(is_success=True)
