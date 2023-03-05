from dataclasses import dataclass, field

from text_to_speech.room_dialogue_data import RoomDialogueData


@dataclass
class DialogueData:
    # Break Room Dialogue Data
    break_room_dialogue_data: RoomDialogueData = field(default_factory=RoomDialogueData)
    # Patient Room Dialogue Data
    patient_room_dialogue_data: RoomDialogueData = field(default_factory=RoomDialogueData)
    # Break Room Feedback Dialogue Data
    break_room_feedback_dialogue_data: RoomDialogueData = field(default_factory=RoomDialogueData)
    # Patient Room Feedback Dialogue Data
    patient_room_feedback_dialogue_data: RoomDialogueData = field(default_factory=RoomDialogueData)
