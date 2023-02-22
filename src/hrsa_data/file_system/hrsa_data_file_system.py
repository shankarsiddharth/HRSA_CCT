import sys
import threading

from app_file_system.app_file_system import AppFileSystem
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_logger.app_logger import AppLogger
from .file_system_result_data import FileSystemResultData
from .hrsa_data_file_system_constants import HRSADataFileSystemConstants
from .hrsa_data_workspace_folder_data import HRSADataWorkspaceFolderData


class HRSADataFileSystem(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(HRSADataFileSystem, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if sys.flags.dev_mode:
                        print("HRSADataFileSystem.__new__()")
        return cls._instance

    def __initialize__(self):
        self.hdfsc: HRSADataFileSystemConstants = HRSADataFileSystemConstants()
        self.afsc: AppFileSystemConstants = AppFileSystemConstants()
        self.afs: AppFileSystem = AppFileSystem()
        self.log: AppLogger = AppLogger()
        # TODO: Get the Workspace folder path data while starting the application
        #   Read the workspace folder path data from the settings config file
        #   then, populate the self.hrsa_data_workspace_folder_path_data object with the workspace folder data
        #   this will useful while creating new scenarios to check if the scenario name already exists
        #   Currently, this is not implemented and will be empty
        self.hrsa_data_workspace_root_folder_path = self.afs.get_user_hrsa_data_workspace_path()
        self.hrsa_data_workspace_folder_data: HRSADataWorkspaceFolderData = HRSADataWorkspaceFolderData(
            hrsa_data_workspace_folder_root_path=self.hrsa_data_workspace_root_folder_path
        )

        # Initialize the workspace folder data from the workspace directory
        self.hrsa_data_workspace_folder_data.initialize_workspace_folder_data()
        # print("\n" + json.dumps(asdict(self.hrsa_data_workspace_folder_data), indent=4) + "\n")

    def validate_scenario_name(self, scenario_name: str) -> bool:
        # TODO: Check if scenario_name is valid (no special characters, etc.)
        # TODO: Check if scenario_name already exists
        # TODO: Check if the workspace folder has write permissions for the user
        return True

    def create_new_scenario_folder_for_language(self, scenario_name, language_code) -> bool:
        file_system_result_data: FileSystemResultData = self.hrsa_data_workspace_folder_data.create_new_scenario_folder_for_language(scenario_name, language_code)
        return file_system_result_data.is_success

    def delete_scenario_folder(self, scenario_name) -> bool:
        if not self.hrsa_data_workspace_folder_data.delete_scenario_folder(scenario_name):
            return False
        return True

    def set_current_scenario(self, scenario_name: str, language_code: str = '') -> bool:
        """
        Set the current scenario and language
        If the language_code is not provided, then the default language code will be used
        :param scenario_name:
        :param language_code:
        :return:
        """
        if language_code == '':
            language_code = self.hdfsc.DEFAULT_LANGUAGE_CODE

        if not self.set_current_scenario(scenario_name, language_code):
            return False
        return True

    def set_current_scenario_and_language(self, scenario_name, language_code) -> bool:
        if not self.hrsa_data_workspace_folder_data.set_current_scenario_name(scenario_name):
            if not self.hrsa_data_workspace_folder_data.set_current_scenario_current_language_code(language_code):
                return False
            return False
        return True

    def refresh_scenario_data(self, scenario_name) -> None:
        self.hrsa_data_workspace_folder_data.refresh_scenario_data(scenario_name)
        pass

    def get_current_scenario_languages(self) -> list[str] | None:
        return self.hrsa_data_workspace_folder_data.get_current_scenario_languages()

    # def create_new_scenario_folder_for_default_language(self, scenario_name: str):
    #     if not self.validate_scenario_name(scenario_name):
    #         return False
    #
    #     # Scenario Folder
    #     scenario_folder_path_root = os.path.join(self.hrsa_data_workspace_root_folder_path, scenario_name)
    #     self.log.info("scenario_path_root: " + scenario_folder_path_root)
    #     os.mkdir(scenario_folder_path_root)
    #
    #     # Create a new Scenario Folder Path Data object
    #     new_scenario_folder_path_data = ScenarioFolderData(scenario_name=scenario_name, scenario_folder_root_path=scenario_folder_path_root)
    #     # New Scenario Default Language Folder Path Data called as 'nsdlfd' for brevity
    #     nsdlfd: ScenarioLanguageFolderData = new_scenario_folder_path_data.get_default_scenario_language_folder_data()
    #
    #     if nsdlfd is None:
    #         self.log.error("nsdlfd is None")
    #         return False
    #
    #     # Default Language Folder
    #     scenario_default_language_folder = os.path.join(scenario_folder_path_root, self.hdfsc.DEFAULT_LANGUAGE_CODE)
    #     self.log.info("default_language_folder: " + scenario_default_language_folder)
    #     os.mkdir(scenario_default_language_folder)
    #     nsdlfd.scenario_language_folder_root_path = scenario_default_language_folder
    #
    #     # Break Room Folder
    #     break_room_folder_path = os.path.join(scenario_default_language_folder, self.hdfsc.BREAK_ROOM_NAME)
    #     os.mkdir(break_room_folder_path)
    #     nsdlfd.break_room_folder_path = break_room_folder_path
    #     # Break Room Audio Folder
    #     audio_folder = os.path.join(break_room_folder_path, self.hdfsc.AUDIO_FOLDER_NAME)
    #     os.mkdir(audio_folder)
    #     nsdlfd.break_room_audio_folder_path = audio_folder
    #     # Break Room Dialogue Ink File
    #     file_path = os.path.join(break_room_folder_path, self.hdfsc.DIALOGUE_INK_FILE_NAME)
    #     open(file_path, 'a').close()
    #     nsdlfd.break_room_dialogue_ink_file_path = file_path
    #     # Break Room Dialogue JSON File
    #     file_path = os.path.join(break_room_folder_path, self.hdfsc.DIALOGUE_INK_JSON_FILE_NAME)
    #     nsdlfd.break_room_dialogue_ink_json_file_path = file_path
    #
    #     # Patient Room Folder
    #     patient_room_folder_path = os.path.join(scenario_default_language_folder, self.hdfsc.PATIENT_ROOM_NAME)
    #     os.mkdir(patient_room_folder_path)
    #     nsdlfd.patient_room_folder_path = patient_room_folder_path
    #     # Patient Room Audio Folder
    #     audio_folder = os.path.join(patient_room_folder_path, self.hdfsc.AUDIO_FOLDER_NAME)
    #     os.mkdir(audio_folder)
    #     nsdlfd.patient_room_audio_folder_path = audio_folder
    #     # Patient Room Dialogue Ink File
    #     file_path = os.path.join(patient_room_folder_path, self.hdfsc.DIALOGUE_INK_FILE_NAME)
    #     open(file_path, 'a').close()
    #     nsdlfd.patient_room_dialogue_ink_file_path = file_path
    #     # Patient Room Dialogue JSON File
    #     file_path = os.path.join(patient_room_folder_path, self.hdfsc.DIALOGUE_INK_JSON_FILE_NAME)
    #     nsdlfd.patient_room_dialogue_ink_json_file_path = file_path
    #
    #     # Feedback Room Folder
    #     feedback_room_folder_path = os.path.join(scenario_default_language_folder, self.hdfsc.FEEDBACK_ROOM_NAME)
    #     os.mkdir(feedback_room_folder_path)
    #     nsdlfd.feedback_room_folder_path = feedback_room_folder_path
    #
    #     # Break Room Feedback Folder
    #     break_room_feedback_folder_path = os.path.join(feedback_room_folder_path, self.hdfsc.FEEDBACK_TYPE_BREAK_ROOM_NAME)
    #     os.mkdir(break_room_feedback_folder_path)
    #     nsdlfd.feedback_break_room_folder_path = break_room_feedback_folder_path
    #     # Break Room Feedback Audio Folder
    #     audio_folder = os.path.join(break_room_feedback_folder_path, self.hdfsc.AUDIO_FOLDER_NAME)
    #     os.mkdir(audio_folder)
    #     nsdlfd.feedback_break_room_audio_folder_path = audio_folder
    #     # Break Room Feedback Ink File
    #     file_path = os.path.join(break_room_feedback_folder_path, self.hdfsc.FEEDBACK_INK_FILE_NAME)
    #     open(file_path, 'a').close()
    #     nsdlfd.feedback_break_room_dialogue_ink_file_path = file_path
    #     # Break Room Feedback JSON File
    #     file_path = os.path.join(break_room_feedback_folder_path, self.hdfsc.FEEDBACK_INK_JSON_FILE_NAME)
    #     nsdlfd.feedback_break_room_dialogue_ink_json_file_path = file_path
    #
    #     # Patient Room Feedback Folder
    #     patient_room_feedback_folder_path = os.path.join(feedback_room_folder_path, self.hdfsc.FEEDBACK_TYPE_PATIENT_ROOM_NAME)
    #     os.mkdir(patient_room_feedback_folder_path)
    #     nsdlfd.feedback_patient_room_folder_path = patient_room_feedback_folder_path
    #     # Patient Room Feedback Audio Folder
    #     audio_folder = os.path.join(patient_room_feedback_folder_path, self.hdfsc.AUDIO_FOLDER_NAME)
    #     os.mkdir(audio_folder)
    #     nsdlfd.feedback_patient_room_audio_folder_path = audio_folder
    #     # Patient Room Feedback Ink File
    #     file_path = os.path.join(patient_room_feedback_folder_path, self.hdfsc.FEEDBACK_INK_FILE_NAME)
    #     open(file_path, 'a').close()
    #     nsdlfd.feedback_patient_room_dialogue_ink_file_path = file_path
    #     # Patient Room Feedback JSON File
    #     file_path = os.path.join(patient_room_feedback_folder_path, self.hdfsc.FEEDBACK_INK_JSON_FILE_NAME)
    #     nsdlfd.feedback_patient_room_dialogue_ink_json_file_path = file_path
    #
    #     # Scenario Data Files
    #
    #     # Scenario Information File
    #     file_path = os.path.join(scenario_default_language_folder, self.hdfsc.SCENARIO_INFORMATION_JSON_FILE_NAME)
    #     scenario_information = ScenarioInformation()
    #     scenario_information.scenario_name = scenario_name
    #     with open(file_path, 'w', encoding=self.afsc.DEFAULT_FILE_ENCODING) as json_file:
    #         json.dump(asdict(scenario_information), json_file, indent=4)
    #     nsdlfd.scenario_information_json_file_path = file_path
    #
    #     # Scenario Config File
    #     file_path = os.path.join(scenario_default_language_folder, self.hdfsc.SCENARIO_CONFIG_JSON_FILE_NAME)
    #     scenario_config = ScenarioConfig()
    #     with open(file_path, 'w', encoding=self.afsc.DEFAULT_FILE_ENCODING) as json_file:
    #         json.dump(asdict(scenario_config), json_file, indent=4)
    #     nsdlfd.scenario_config_json_file_path = file_path
    #
    #     # Scenario Voice Config File
    #     file_path = os.path.join(scenario_default_language_folder, self.hdfsc.SCENARIO_VOICE_CONFIG_JSON_FILE_NAME)
    #     scenario_voice_config = ScenarioVoiceConfig()
    #     with open(file_path, 'w', encoding=self.afsc.DEFAULT_FILE_ENCODING) as json_file:
    #         json.dump(asdict(scenario_voice_config), json_file, indent=4)
    #     nsdlfd.scenario_voice_config_json_file_path = file_path
    #
    #     # Patient Information File
    #     file_path = os.path.join(scenario_default_language_folder, self.hdfsc.PATIENT_INFORMATION_JSON_FILE_NAME)
    #     patient_information = PatientInformation()
    #     with open(file_path, 'w', encoding=self.afsc.DEFAULT_FILE_ENCODING) as json_file:
    #         json.dump(asdict(patient_information), json_file, indent=4)
    #     nsdlfd.patient_information_json_file_path = file_path
    #
    #     # Scenario Thumbnail File
    #     file_path = os.path.join(scenario_default_language_folder, self.hdfsc.SCENARIO_THUMBNAIL_IMAGE_FILE_NAME)
    #     # TODO: Create a default thumbnail image, from the default data folder of the application
    #     nsdlfd.scenario_thumbnail_image_file_path = file_path
    #
    #     # Add new scenario folder path data to the workspace folder path data
    #     self.hrsa_data_workspace_folder_data.add_new_scenario_folder_path_data(new_scenario_folder_path_data)
    #     # print(json.dumps(asdict(self.hrsa_data_workspace_folder_path_data), indent=4))
    #
    #     return True
