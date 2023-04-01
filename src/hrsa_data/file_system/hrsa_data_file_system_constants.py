from langcodes import Language

from classes.singleton import Singleton


class HRSADataFileSystemConstants(metaclass=Singleton):

    def __init__(self):
        self.HRSA_CCT_WORKSPACE_FOLDER_NAME = "HRSA_CCT_Workspace"

        # region HRSAData Folder Constants
        # region HRSAData Files & Folder Constants
        self.BREAK_ROOM_NAME = "BreakRoom"
        self.PATIENT_ROOM_NAME = "PatientRoom"
        self.FEEDBACK_ROOM_NAME = "FeedbackRoom"
        self.FEEDBACK_TYPE_BREAK_ROOM_NAME = "BreakRoomFeedback"
        self.FEEDBACK_TYPE_PATIENT_ROOM_NAME = "PatientRoomFeedback"
        self.DIALOGUE_INK_FILE_NAME = "dialogue.ink"
        self.FEEDBACK_INK_FILE_NAME = "feedback.ink"
        self.DIALOGUE_INK_JSON_FILE_NAME = "dialogue.json"
        self.FEEDBACK_INK_JSON_FILE_NAME = "feedback.json"
        self.AUDIO_FOLDER_NAME = "Audio"
        self.SCENARIO_INFORMATION_JSON_FILE_NAME = "scenario_information.json"
        self.SCENARIO_VOICE_CONFIG_JSON_FILE_NAME = "scenario_voice_config.json"
        self.PATIENT_INFORMATION_JSON_FILE_NAME = "patient_information.json"
        self.SCENARIO_CONFIG_JSON_FILE_NAME = "scenario_config.json"
        self.SCENARIO_THUMBNAIL_IMAGE_FILE_NAME = "thumbnail.jpg"
        # endregion HRSAData Files & Folder Constants

        # region HRSAData Scenario Constants
        self.NONE_SCENARIO_CODE = "NONE"
        self.NONE_SCENARIO_CODE_NAME = "(none)"
        # endregion HRSAData Scenario Constants

        # region Default Language Constants
        self.NONE_LANGUAGE_CODE = "NONE"
        self.NONE_LANGUAGE_CODE_NAME = "(none)"
        self.DEFAULT_LANGUAGE_CODE = "en-US"
        self.DEFAULT_LANGUAGE_NAME = Language.get(self.DEFAULT_LANGUAGE_CODE).display_name()
        # endregion Default Language Constants

        # endregion HRSAData Folder Constants
