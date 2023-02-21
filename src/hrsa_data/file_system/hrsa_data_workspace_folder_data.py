import os
from dataclasses import dataclass, field

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
                    # TODO - Log Error / Warning - Scenario Folder Path Data is not valid - Empty Folder
                    pass
        return True
