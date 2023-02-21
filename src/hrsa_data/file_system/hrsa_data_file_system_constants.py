import sys
import threading

from langcodes import Language


class HRSADataFileSystemConstants(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(HRSADataFileSystemConstants, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if sys.flags.dev_mode:
                        print("HRSADataFileSystemConstants.__new__()")
        return cls._instance

    def __initialize__(self):

        self.HRSA_CCT_WORKSPACE_FOLDER_NAME = "HRSA_CCT_Workspace"
        
        # ========================== START HRSAData Folder Constants ===================================
        # HRSAData Folder Constants
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

        # Default Language Constants
        self.DEFAULT_LANGUAGE_CODE = "en-US"
        self.DEFAULT_LANGUAGE_NAME = Language.get(self.DEFAULT_LANGUAGE_CODE).display_name()
        # ========================== END HRSAData Folder Constants ===================================

    @staticmethod
    def get_instance():
        return HRSADataFileSystemConstants()
