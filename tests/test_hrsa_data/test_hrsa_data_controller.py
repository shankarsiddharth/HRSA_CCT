import os.path
import shutil
import unittest

from app_file_system.app_file_system import AppFileSystem
from hrsa_data.hrsa_data_controller import HRSADataController


class TestHRSADataController(unittest.TestCase):

    def setUp(self):
        self.hdc: HRSADataController = HRSADataController()
        self.afs: AppFileSystem = AppFileSystem()

    def delete_scenario_if_exist(self, test_scenario, ws_root):
        test_scenario_path = os.path.join(ws_root, test_scenario)
        if os.path.exists(test_scenario_path):
            shutil.rmtree(test_scenario_path)
            print("Deleted scenario path: " + test_scenario_path)
        return test_scenario_path

    def test_create_new_scenario_data(self):
        # Workspace Root Path
        ws_root = self.afs.get_hrsa_data_workspace_folder_path()
        # Scenario Path
        test_scenario_1 = 'test_scenario_1'
        test_scenario_1_path = self.delete_scenario_if_exist(test_scenario_1, ws_root)
        print("Trying to create scenario path: " + test_scenario_1_path)
        self.assertEqual(self.hdc.create_new_scenario_data(test_scenario_1), True)

        test_scenario_2 = 'test_scenario_2'
        test_scenario_2_path = self.delete_scenario_if_exist(test_scenario_2, ws_root)
        print("Trying to create scenario path: " + test_scenario_2_path)
        self.assertEqual(self.hdc.create_new_scenario_data(test_scenario_2), True)

    def test_create_new_scenario_data_for_language(self):
        # Workspace Root Path
        ws_root = self.afs.get_hrsa_data_workspace_folder_path()
        # Scenario Path
        test_scenario_1 = 'test_scenario_1'
        self.hdc.delete_scenario_data(test_scenario_1)
        print("Trying to create scenario path: " + test_scenario_1)
        self.assertEqual(self.hdc.create_new_scenario_data(test_scenario_1, self.hdc.__hdfsc__.DEFAULT_LANGUAGE_CODE), True)

        test_scenario_2 = 'test_scenario_2'
        self.hdc.delete_scenario_data(test_scenario_2)
        print("Trying to create scenario path: " + test_scenario_2)
        self.assertEqual(self.hdc.create_new_scenario_data(test_scenario_2, self.hdc.__hdfsc__.DEFAULT_LANGUAGE_CODE), True)


if __name__ == '__main__':
    unittest.main()
