import os
from dataclasses import dataclass, field

from .hrsa_data_file_system_constants import HRSADataFileSystemConstants
from .scenario_language_folder_data import ScenarioLanguageFolderData

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class ScenarioFolderData:
    # Scenario Name
    scenario_name: str = field(default='')
    # Scenario Folder Path - Root
    scenario_folder_root_path: str = field(default='')
    scenario_language_folder_data_list: list[ScenarioLanguageFolderData] = field(default_factory=list)

    # def __post_init__(self):
    #     if len(self.scenario_language_folder_data_list) == 0:
    #         self.scenario_language_folder_data_list = [ScenarioLanguageFolderData()]

    def is_scenario_language_folder_data_valid(self, language_code: str) -> bool:
        for scenario_language_folder_data_item in self.scenario_language_folder_data_list:
            if scenario_language_folder_data_item.language_code == language_code:
                return True
        return False

    def get_scenario_language_folder_data(self, language_code: str) -> ScenarioLanguageFolderData | None:
        """
        Get the scenario language folder path data for the given language code.\n
        Use **is_scenario_language_folder_path_data_valid()** first to check if the language code is valid.
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
        scenario_root_path: str = self.scenario_folder_root_path
        dir_list = os.listdir(scenario_root_path)
        if len(dir_list) == 0:
            os.rmdir(scenario_root_path)
            return False
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(scenario_root_path, dir_item)
            if os.path.isdir(dir_item_path):
                scenario_language_folder_data: ScenarioLanguageFolderData = ScenarioLanguageFolderData()
                scenario_language_folder_data.language_code = dir_item
                scenario_language_folder_data.scenario_language_folder_root_path = dir_item_path
                if scenario_language_folder_data.initialize_scenario_language_folder_data():
                    self.scenario_language_folder_data_list.append(scenario_language_folder_data)
                else:
                    # TODO - Log Error / Warning - Scenario Folder Path Data is not valid - Empty Folder
                    pass
        return True
