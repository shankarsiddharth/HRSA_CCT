# Constants
import sys

HRSA_CCT_TOOL: str = "HRSA_CCT_TOOL"

# Constants
BREAK_ROOM_NAME = "BreakRoom"
PATIENT_ROOM_NAME = "PatientRoom"
FEEDBACK_ROOM_NAME = "FeedbackRoom"
FEEDBACK_TYPE_BREAK_ROOM_NAME = "BreakRoomFeedback"
FEEDBACK_TYPE_PATIENT_ROOM_NAME = "PatientRoomFeedback"
DIALOGUE_INK_FILE_NAME = "dialogue.ink"
FEEDBACK_INK_FILE_NAME = "feedback.ink"
DIALOGUE_INK_JSON_FILE_NAME = "dialogue.json"
FEEDBACK_INK_JSON_FILE_NAME = "feedback.json"
AUDIO_FOLDER_NAME = "Audio"
SCENARIO_INFORMATION_JSON_FILE_NAME = "scenario_information.json"
CHARACTER_VOICE_CONFIG_JSON_FILE_NAME = "scenario_voice_config.json"
PATIENT_INFORMATION_JSON_FILE_NAME = "patient_information.json"
SCENARIO_CONFIG_JSON_FILE_NAME = "scenario_config.json"
MAX_DIALOGUE_TEXT_CHARACTER_COUNT = 275  # 300 / 250

CCT_CONFIG_FOLDER_NAME = "cctconfig"
CCT_CONFIG_FILE_NAME = "cct.config.ini"
DPG_CONFIG_FILE_NAME = "dpg.config.ini"

if sys.flags.dev_mode:
    print("hrsa_cc_constants.__init__()")
