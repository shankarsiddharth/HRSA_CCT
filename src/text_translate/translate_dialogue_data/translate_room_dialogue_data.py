from dataclasses import dataclass, field


@dataclass
class TranslateRoomDialogueData:
    # Room Name
    room_name: str = field(default='')
    # Translate Dialogue Data List
    translate_dialogue_data_list: list[str] = field(default_factory=list)
