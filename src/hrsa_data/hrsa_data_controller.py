from hrsa_data.file_system.hrsa_data_file_system import HRSADataFileSystem


class HRSADataController(object):
    def __init__(self):
        self.hdfs: HRSADataFileSystem = HRSADataFileSystem()
        pass

    def create_new_scenario_data(self, scenario_name: str):
        if not self.hdfs.create_new_scenario_folders_for_default_language(scenario_name):
            return False
        return True
