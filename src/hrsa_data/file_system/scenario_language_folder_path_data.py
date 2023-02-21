from dataclasses import dataclass, field

from hrsa_data.file_system.hrsa_data_file_system_constants import HRSADataFileSystemConstants

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class ScenarioLanguageFolderPathData:
    # Scenario Language Code
    language_code: str = field(default=__hdfsc__.DEFAULT_LANGUAGE_CODE)

    # Scenario Language Folder Path - Root
    scenario_language_folder_root_path: str = field(default='')

    # Break Room Folder
    break_room_folder_path: str = field(default='')
    break_room_audio_folder_path: str = field(default='')
    break_room_dialogue_ink_file_path: str = field(default='')
    break_room_dialogue_ink_json_file_path: str = field(default='')
    # Patient Room Folder
    patient_room_folder_path: str = field(default='')
    patient_room_audio_folder_path: str = field(default='')
    patient_room_dialogue_ink_file_path: str = field(default='')
    patient_room_dialogue_ink_json_file_path: str = field(default='')
    # Feedback Room Folder
    feedback_room_folder_path: str = field(default='')
    # Feedback Break Room Folder
    feedback_break_room_folder_path: str = field(default='')
    feedback_break_room_audio_folder_path: str = field(default='')
    feedback_break_room_dialogue_ink_file_path: str = field(default='')
    feedback_break_room_dialogue_ink_json_file_path: str = field(default='')
    # Feedback Patient Room Folder
    feedback_patient_room_folder_path: str = field(default='')
    feedback_patient_room_audio_folder_path: str = field(default='')
    feedback_patient_room_dialogue_ink_file_path: str = field(default='')
    feedback_patient_room_dialogue_ink_json_file_path: str = field(default='')

    # Scenario Language Folder - Data File Paths
    scenario_information_json_file_path: str = field(default='')
    scenario_config_json_file_path: str = field(default='')
    scenario_voice_config_json_file_path: str = field(default='')
    patient_information_json_file_path: str = field(default='')
    scenario_thumbnail_image_file_path: str = field(default='')
