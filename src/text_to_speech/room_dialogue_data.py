from dataclasses import dataclass, field

from .dialogue_audio_data import AudioDialogueData


@dataclass
class RoomDialogueData:
    # Room Name
    room_name: str = field(default='')
    # Audio Dialogue Data List
    audio_dialogue_data_list: list[AudioDialogueData] = field(default_factory=list)
