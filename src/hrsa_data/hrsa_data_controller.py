from classes.singleton import Singleton
from .file_system.hrsa_data_file_system import HRSADataFileSystem
from .file_system.hrsa_data_file_system_constants import HRSADataFileSystemConstants
from .file_system.scenario_language_folder_data import ScenarioLanguageFolderData


class HRSADataController(metaclass=Singleton):
    __hdfs__: HRSADataFileSystem = HRSADataFileSystem()
    __hdfsc__: HRSADataFileSystemConstants = HRSADataFileSystemConstants()

    def __init__(self):
        pass

    def create_new_scenario_data(self, scenario_name: str, language_code: str = '') -> bool:
        """
        Create a new scenario folder and all the required sub-folders.
        By default, the scenario will be created with the default language code.
        The default language code **DEFAULT_LANGUAGE_CODE** is defined in the **HRSADataFileSystemConstants** class.
        :param scenario_name:
        :param language_code:
        :return:
        """
        if language_code == '':
            language_code = self.__hdfsc__.DEFAULT_LANGUAGE_CODE

        if not self.__hdfs__.create_new_scenario_folder_for_language(scenario_name, language_code):
            return False
        return True

    def delete_scenario_data(self, scenario_name: str) -> bool:
        if not self.__hdfs__.delete_scenario_folder(scenario_name):
            return False
        return True

    def get_current_scenario_folder_data_for_current_language_code(self) -> ScenarioLanguageFolderData | None:
        return self.__hdfs__.get_current_scenario_folder_data_for_current_language_code()
