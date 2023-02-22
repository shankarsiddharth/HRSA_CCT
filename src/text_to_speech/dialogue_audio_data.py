from dataclasses import dataclass, field


@dataclass
class AudioDialogueData:
    # Dialogue Text
    text: str = field(default='')
    # Dialogue Audio File Path
    audio_file_path: str = field(default='')
    # Dialogue Audio File Name
    audio_file_name: str = field(default='')
    # Dialogue Audio File Extension
    audio_file_extension: str = field(default='')
    # Dialogue Audio File Name with Extension
    audio_file_name_with_extension: str = field(default='')
    # Character Type
    character_type: str = field(default='')
