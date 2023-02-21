from dataclasses import dataclass, field

from hrsa_data.file_system.scenario_folder_path_data import ScenarioFolderPathData


@dataclass
class HRSADataWorkspaceFolderPathData:
    scenario_folder_path_data_list: list[ScenarioFolderPathData] = field(default_factory=list)

    # def __post_init__(self):
    #     if len(self.scenario_folder_path_data_list) == 0:
    #         self.scenario_folder_path_data_list = [ScenarioFolderPathData()]

    def add_new_scenario_folder_path_data(self, scenario_folder_path_data: ScenarioFolderPathData) -> bool:
        for scenario_folder_path_data_item in self.scenario_folder_path_data_list:
            if scenario_folder_path_data_item.scenario_name == scenario_folder_path_data.scenario_name:
                return False
        self.scenario_folder_path_data_list.append(scenario_folder_path_data)
        return True
