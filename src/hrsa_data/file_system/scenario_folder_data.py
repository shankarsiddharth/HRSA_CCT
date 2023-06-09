import os
import pathlib
from dataclasses import dataclass, field

from .file_system_result_data import FileSystemResultData
from .hrsa_data_file_system_constants import HRSADataFileSystemConstants
from .scenario_language_folder_data import ScenarioLanguageFolderData

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class ScenarioFolderData:
    # Scenario Name
    scenario_name: str = field(default='')
    # Scenario Folder Path - Root
    folder_root_path: str = field(default='')
    scenario_language_folder_data_list: list[ScenarioLanguageFolderData] = field(default_factory=list)

    # def __post_init__(self):
    #     if len(self.scenario_language_folder_data_list) == 0:
    #         self.scenario_language_folder_data_list = [ScenarioLanguageFolderData()]

    def is_scenario_language_folder_data_present(self, language_code: str) -> bool:
        for scenario_language_folder_data_item in self.scenario_language_folder_data_list:
            if scenario_language_folder_data_item.language_code == language_code:
                return True
        return False

    def get_scenario_language_folder_data(self, language_code: str) -> ScenarioLanguageFolderData | None:
        """
        Get the scenario language folder path data for the given language code.\n
        Use **is_scenario_language_folder_data_present()** first to check if the language code is valid.
        :param language_code:
        :return:
        """
        for scenario_language_folder_data_item in self.scenario_language_folder_data_list:
            if scenario_language_folder_data_item.language_code == language_code:
                return scenario_language_folder_data_item
        return None

    def get_default_scenario_language_folder_data(self) -> ScenarioLanguageFolderData:
        return self.get_scenario_language_folder_data(__hdfsc__.DEFAULT_LANGUAGE_CODE)

    def initialize_scenario_folder_data(self):
        scenario_root_path: str = self.folder_root_path
        dir_list = os.listdir(scenario_root_path)
        if len(dir_list) == 0:
            os.rmdir(scenario_root_path)
            return False
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(scenario_root_path, dir_item)
            if os.path.isdir(dir_item_path):
                scenario_language_folder_data: ScenarioLanguageFolderData = ScenarioLanguageFolderData()
                scenario_language_folder_data.language_code = dir_item
                scenario_language_folder_data.folder_root_path = dir_item_path
                if scenario_language_folder_data.initialize_scenario_language_folder_data():
                    self.scenario_language_folder_data_list.append(scenario_language_folder_data)
                else:
                    # TODO - Log Error / Warning - Scenario Folder Path Data is not valid - Empty Folder
                    pass
        return True

    def create_new_scenario_folder_for_language(self, language_code) -> FileSystemResultData:
        new_scenario_path = pathlib.Path(self.folder_root_path)

        if new_scenario_path.exists():
            # TODO: Folder already exists, handle this
            return FileSystemResultData(is_success=False, error_message='Scenario Folder Already Exists')

        if self.is_scenario_language_folder_data_present(language_code):
            file_system_result_data: FileSystemResultData = FileSystemResultData(is_success=False, error_message='Language Code already exists')
            return file_system_result_data
        new_scenario_path.mkdir()
        scenario_language_folder_data: ScenarioLanguageFolderData = ScenarioLanguageFolderData()
        scenario_language_folder_data.language_code = language_code
        scenario_language_folder_data.folder_root_path = os.path.join(self.folder_root_path, language_code)
        file_system_result_data: FileSystemResultData = scenario_language_folder_data.create_new_scenario_language_folder()
        if not file_system_result_data.is_success:
            return file_system_result_data
        self.scenario_language_folder_data_list.append(scenario_language_folder_data)
        return FileSystemResultData(is_success=True)

    def refresh_scenario_data(self):
        self.scenario_language_folder_data_list.clear()
        self.initialize_scenario_folder_data()
        pass

    def get_scenario_languages(self) -> list[str] | None:
        # TODO: Return the language codes as user-friendly names
        language_folder_data_item: ScenarioLanguageFolderData
        language_list: list[str] = [__hdfsc__.NONE_LANGUAGE_CODE]
        for language_folder_data_item in self.scenario_language_folder_data_list:
            language_list.append(language_folder_data_item.language_code)
        if len(language_list) == 1:  # Only the None Language Code
            return None
        else:
            return language_list
