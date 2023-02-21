from dataclasses import dataclass, field

from hrsa_data.file_system.hrsa_data_file_system_constants import HRSADataFileSystemConstants
from hrsa_data.file_system.scenario_language_folder_path_data import ScenarioLanguageFolderPathData

# Module Level Constants
__hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()


@dataclass
class ScenarioFolderPathData:
    # Scenario Name
    scenario_name: str = field(default='')
    # Scenario Folder Path - Root
    scenario_folder_root_path: str = field(default='')
    language_folder_path_data_list: list[ScenarioLanguageFolderPathData] = field(default_factory=list)

    def __post_init__(self):
        if len(self.language_folder_path_data_list) == 0:
            self.language_folder_path_data_list = [ScenarioLanguageFolderPathData()]

    def is_scenario_language_folder_path_data_valid(self, language_code: str) -> bool:
        for language_folder_path_data in self.language_folder_path_data_list:
            if language_folder_path_data.language_code == language_code:
                return True
        return False

    def get_scenario_language_folder_path_data(self, language_code: str) -> ScenarioLanguageFolderPathData | None:
        """
        Get the scenario language folder path data for the given language code.\n
        Use **is_scenario_language_folder_path_data_valid()** first to check if the language code is valid.
        :param language_code:
        :return:
        """
        for language_folder_path_data in self.language_folder_path_data_list:
            if language_folder_path_data.language_code == language_code:
                return language_folder_path_data
        return None

    def get_default_scenario_language_folder_path_data(self) -> ScenarioLanguageFolderPathData:
        return self.get_scenario_language_folder_path_data(__hdfsc__.DEFAULT_LANGUAGE_CODE)
