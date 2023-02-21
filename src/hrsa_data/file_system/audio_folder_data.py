import os
from dataclasses import dataclass, field


@dataclass
class AudioFolderData:
    # Audio Folder Path - Root
    audio_folder_root_path: str = field(default='')
    audio_file_path_data_list: list[str] = field(default_factory=list)

    def initialize_audio_folder_data(self):
        root_path = self.audio_folder_root_path
        dir_list = os.listdir(root_path)
        if len(dir_list) == 0:
            return False
        for dir_item in dir_list:
            dir_item_path: str = os.path.join(root_path, dir_item)
            if os.path.isfile(dir_item_path):
                self.audio_file_path_data_list.append(dir_item_path)
        return True
