from dataclasses import dataclass, field

from .audio_dialogue_data import AudioDialogueData


@dataclass
class RoomDialogueData:
    # Room Name
    room_name: str = field(default='')
    # Audio Dialogue Data List
    audio_dialogue_data_dict: dict[str, AudioDialogueData] = field(default_factory=dict)
