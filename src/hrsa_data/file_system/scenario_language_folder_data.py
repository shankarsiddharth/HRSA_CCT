import os
from dataclasses import dataclass, field

from hrsa_data.scenario_data.ehr.patient_information import PatientInformation
from hrsa_data.scenario_data.scenario_config.scenario_config import ScenarioConfig
from hrsa_data.scenario_data.scenario_information.scenario_information import ScenarioInformation
from hrsa_data.scenario_data.scenario_voice_config.scenario_voice_config import ScenarioVoiceConfig
from .feedback_room_folder_data import FeedbackRoomFolderData
from .hrsa_data_file_system_constants import HRSADataFileSystemConstants
from .room_folder_data import RoomFolderData

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class ScenarioLanguageFolderData:
    # Scenario Language Code
    language_code: str = field(default=__hdfsc__.DEFAULT_LANGUAGE_CODE)

    # Scenario Language Folder Path - Root
    scenario_language_folder_root_path: str = field(default='')

    # Break Room Folder Data
    scenario_break_room_folder_data: RoomFolderData = field(default_factory=RoomFolderData)
    # Patient Room Folder Data
    scenario_patient_room_folder_data: RoomFolderData = field(default_factory=RoomFolderData)
    # Feedback Room Folder Data
    scenario_feedback_room_folder_data: FeedbackRoomFolderData = field(default_factory=FeedbackRoomFolderData)

    # Scenario Language Folder - Data File Paths
    scenario_information_json_file_path: str = field(default='')
    scenario_config_json_file_path: str = field(default='')
    scenario_voice_config_json_file_path: str = field(default='')
    patient_information_json_file_path: str = field(default='')
    scenario_thumbnail_image_file_path: str = field(default='')

    # Scenario Language Folder - Data
    scenario_information: ScenarioInformation = field(default_factory=ScenarioInformation)
    scenario_config: ScenarioConfig = field(default_factory=ScenarioConfig)
    scenario_voice_config: ScenarioVoiceConfig = field(default_factory=ScenarioVoiceConfig)
    patient_information: PatientInformation = field(default_factory=PatientInformation)

    def initialize_scenario_language_folder_data(self):
        language_folder_root: str = self.scenario_language_folder_root_path
        dir_list = os.listdir(language_folder_root)
        if len(dir_list) == 0:
            os.rmdir(language_folder_root)
            return False
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(language_folder_root, dir_item)
            if os.path.isdir(dir_item_path):
                if dir_item == __hdfsc__.BREAK_ROOM_NAME:
                    self.scenario_break_room_folder_data.room_folder_root_path = dir_item_path
                    if not self.scenario_break_room_folder_data.initialize_room_folder_data():
                        # TODO: Log error / warning - Break Room Folder Content Error
                        pass
                elif dir_item == __hdfsc__.PATIENT_ROOM_NAME:
                    self.scenario_patient_room_folder_data.room_folder_root_path = dir_item_path
                    if not self.scenario_patient_room_folder_data.initialize_room_folder_data():
                        # TODO: Log error / warning - Patient Room Folder Content Error
                        pass
                elif dir_item == __hdfsc__.FEEDBACK_ROOM_NAME:
                    self.scenario_feedback_room_folder_data.feedback_room_folder_root_path = dir_item_path
                    if not self.scenario_feedback_room_folder_data.initialize_feedback_room_folder_data():
                        # TODO: Log error / warning - Feedback Room Folder Content Error
                        pass

            if os.path.isfile(dir_item_path):
                if dir_item == __hdfsc__.SCENARIO_INFORMATION_JSON_FILE_NAME:
                    self.scenario_information_json_file_path = dir_item_path
                    # TODO - Handle error if the load fails
                    self.scenario_information = ScenarioInformation.load_from_json_file(self.scenario_information_json_file_path)

                elif dir_item == __hdfsc__.SCENARIO_CONFIG_JSON_FILE_NAME:
                    self.scenario_config_json_file_path = dir_item_path
                    # TODO - Handle error if the load fails
                    self.scenario_config = ScenarioConfig.load_from_json_file(self.scenario_config_json_file_path)
                elif dir_item == __hdfsc__.SCENARIO_VOICE_CONFIG_JSON_FILE_NAME:
                    self.scenario_voice_config_json_file_path = dir_item_path
                    # TODO - Handle error if the load fails
                    self.scenario_voice_config = ScenarioVoiceConfig.load_from_json_file(self.scenario_voice_config_json_file_path)
                elif dir_item == __hdfsc__.PATIENT_INFORMATION_JSON_FILE_NAME:
                    self.patient_information_json_file_path = dir_item_path
                    # TODO - Handle error if the load fails
                    self.patient_information = PatientInformation.load_from_json_file(self.patient_information_json_file_path)
                elif dir_item == __hdfsc__.SCENARIO_THUMBNAIL_IMAGE_FILE_NAME:
                    self.scenario_thumbnail_image_file_path = dir_item_path
        return True
