from dataclasses import dataclass, field

from .translate_room_dialogue_data import TranslateRoomDialogueData


@dataclass
class TranslateDialogueData:
    # Break Room Dialogue Data
    break_room_dialogue_data: TranslateRoomDialogueData = field(default_factory=TranslateRoomDialogueData)
    # Patient Room Dialogue Data
    patient_room_dialogue_data: TranslateRoomDialogueData = field(default_factory=TranslateRoomDialogueData)
    # Break Room Feedback Dialogue Data
    break_room_feedback_dialogue_data: TranslateRoomDialogueData = field(default_factory=TranslateRoomDialogueData)
    # Patient Room Feedback Dialogue Data
    patient_room_feedback_dialogue_data: TranslateRoomDialogueData = field(default_factory=TranslateRoomDialogueData)
