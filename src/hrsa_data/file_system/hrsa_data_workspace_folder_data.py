import os
import pathlib
import shutil
from dataclasses import dataclass, field

from .file_system_result_data import FileSystemResultData
from .scenario_folder_data import ScenarioFolderData


@dataclass
class HRSADataWorkspaceFolderData:
    # Workspace Folder Path
    hrsa_data_workspace_folder_root_path: str = field(default='')
    # Scenario Folder Path Data List
    scenario_folder_data_list: list[ScenarioFolderData] = field(default_factory=list)

    # def __post_init__(self):
    #     if len(self.scenario_folder_path_data_list) == 0:
    #         self.scenario_folder_path_data_list = [ScenarioFolderPathData()]

    def add_new_scenario_folder_path_data(self, scenario_folder_path_data: ScenarioFolderData) -> bool:
        for scenario_folder_data_item in self.scenario_folder_data_list:
            if scenario_folder_data_item.scenario_name == scenario_folder_path_data.scenario_name:
                return False
        self.scenario_folder_data_list.append(scenario_folder_path_data)
        return True

    # TODO: Return FileSystemResultData instead of simple bool
    def initialize_workspace_folder_data(self) -> bool:
        ws_root_path: str = self.hrsa_data_workspace_folder_root_path
        dir_list = os.listdir(ws_root_path)
        if len(dir_list) == 0:
            return True
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(ws_root_path, dir_item)
            if os.path.isdir(dir_item_path):
                scenario_folder_data: ScenarioFolderData = ScenarioFolderData()
                scenario_folder_data.scenario_name = dir_item
                scenario_folder_data.scenario_folder_root_path = dir_item_path
                if scenario_folder_data.initialize_scenario_folder_data():
                    self.scenario_folder_data_list.append(scenario_folder_data)
                else:
                    # TODO: - Log Error / Warning - Scenario Folder Path Data is not valid - Empty Folder
                    pass
        return True

    def create_new_scenario_folder_for_language(self, scenario_name: str, language_code: str) -> FileSystemResultData:
        scenario_folder_data: ScenarioFolderData = ScenarioFolderData()
        scenario_folder_data.scenario_name = scenario_name
        scenario_folder_data.scenario_folder_root_path = os.path.join(self.hrsa_data_workspace_folder_root_path, scenario_name)
        file_system_result_data: FileSystemResultData = scenario_folder_data.create_new_scenario_folder_for_language(language_code)
        if not file_system_result_data.is_success:
            scenario_path = pathlib.Path(scenario_folder_data.scenario_folder_root_path)
            if scenario_path.exists():
                # TODO: Handle shutil rmtree error
                shutil.rmtree(scenario_folder_data.scenario_folder_root_path)
            return file_system_result_data
        else:
            self.scenario_folder_data_list.append(scenario_folder_data)
            return file_system_result_data

    def delete_scenario_folder(self, scenario_name: str) -> bool:
        # TODO: Implement delete for scenario folder data by going through the folder classes instead of deleting the folder
        for scenario_folder_data_item in self.scenario_folder_data_list:
            if scenario_folder_data_item.scenario_name == scenario_name:
                scenario_path = pathlib.Path(scenario_folder_data_item.scenario_folder_root_path)
                if scenario_path.exists():
                    # TODO: Handle shutil rmtree error while deleting scenario folder
                    shutil.rmtree(scenario_folder_data_item.scenario_folder_root_path)
                self.scenario_folder_data_list.remove(scenario_folder_data_item)
                return True
        return True
