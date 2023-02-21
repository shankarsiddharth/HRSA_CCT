from .file_system.hrsa_data_file_system import HRSADataFileSystem
from .file_system.hrsa_data_file_system_constants import HRSADataFileSystemConstants


class HRSADataController(object):
    hdfs: HRSADataFileSystem = HRSADataFileSystem()
    hdfsc: HRSADataFileSystemConstants = HRSADataFileSystemConstants()

    def __init__(self):
        pass

    def create_new_scenario_data(self, scenario_name: str):
        """
        Create a new scenario folder and all the required sub-folders.
        By default, the scenario will be created with the default language code.
        The default language code **DEFAULT_LANGUAGE_CODE** is defined in the **HRSADataFileSystemConstants** class.
        :param scenario_name:
        :return:
        """
        if not self.create_new_scenario_data_for_language(scenario_name):
            return False
        return True

    def create_new_scenario_data_for_language(self, scenario_name: str, language_code: str = hdfsc.DEFAULT_LANGUAGE_CODE):
        if not self.hdfs.create_new_scenario_folder_for_language(scenario_name, language_code):
            return False
        return True

    def delete_scenario_data(self, scenario_name: str):
        if not self.hdfs.delete_scenario_folder(scenario_name):
            return False
        return True
