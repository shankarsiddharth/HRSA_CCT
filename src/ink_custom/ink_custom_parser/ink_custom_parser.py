import os
import re

from app_debug.app_debug import IS_DEBUG_MODE_ENABLED
from app_file_system.app_file_system_constants import AppFileSystemConstants
from app_logger.app_logger import AppLogger
from hrsa_data.file_system.hrsa_data_file_system_constants import HRSADataFileSystemConstants
from hrsa_data.file_system.scenario_language_folder_data import ScenarioLanguageFolderData
from hrsa_data.hrsa_data_controller import HRSADataController
from text_to_speech.tts_dialogue_data.audio_dialogue_data import AudioDialogueData
from text_to_speech.tts_dialogue_data.room_dialogue_data import RoomDialogueData
from text_to_speech.tts_dialogue_data.tts_dialogue_data import TTSDialogueData


class InkCustomParser(object):
    _hrsa_data_controller: HRSADataController = HRSADataController()

    def __init__(self):

        self.afsc: AppFileSystemConstants = AppFileSystemConstants()
        self.hdfsc: HRSADataFileSystemConstants = HRSADataFileSystemConstants()
        self.log: AppLogger = AppLogger()

        # Allowed maximum character count for a single line of dialogue text.
        # This will likely to change based on the font settings and size of the text box in the Unity project of the HRSA application.
        # Current Max: 300
        # Current Min: 250
        self.MAX_DIALOGUE_TEXT_CHARACTER_COUNT = 275
        # Default audio file extension is .mp3
        self.DEFAULT_AUDIO_FILE_EXTENSION: str = ".mp3"

        self.option_text_prefixes = [
            'A',
            'B',
            'C',
            'D',
            'E',
            '1',
            '2',
            '3',
            '4',
            '5',
        ]

        self.dialogue_regular_expression = r"\".*?\""
        self.option_regular_expression = r"[*](.*)\[(.*?(?=`))`(.*?(?=`))`(.*?(?=`))`(.*?(?=`|\]))(?:`(.*)])?"
        self.option_display_text_regular_expression = r"\s*[A-Za-z0-9]+\s*[\.](.*)"

        if IS_DEBUG_MODE_ENABLED:
            print("InkCustomParser.__init__()")

    def parse_current_scenario_language_folder(self) -> TTSDialogueData | None:
        # TODO: Error handling
        tts_dialogue_data: TTSDialogueData = TTSDialogueData()

        scenario_language_folder_data: ScenarioLanguageFolderData = self._hrsa_data_controller.get_current_scenario_folder_data_for_current_language_code()
        if scenario_language_folder_data is None:
            return None

        # Parse Break Room Dialogue ink file
        ink_file_path: str = scenario_language_folder_data.break_room_folder_data.dialogue_ink_file_path
        audio_folder_path: str = scenario_language_folder_data.break_room_folder_data.audio_folder_data.audio_folder_root_path
        room_name: str = scenario_language_folder_data.break_room_folder_data.room_name
        room_dialogue_data: RoomDialogueData = self.parse_ink_script(audio_folder_path, ink_file_path, room_name)
        tts_dialogue_data.break_room_dialogue_data = room_dialogue_data

        # Parse Patient Room Dialogue ink file
        ink_file_path: str = scenario_language_folder_data.patient_room_folder_data.dialogue_ink_file_path
        audio_folder_path: str = scenario_language_folder_data.patient_room_folder_data.audio_folder_data.audio_folder_root_path
        room_name: str = scenario_language_folder_data.patient_room_folder_data.room_name
        room_dialogue_data: RoomDialogueData = self.parse_ink_script(audio_folder_path, ink_file_path, room_name)
        tts_dialogue_data.patient_room_dialogue_data = room_dialogue_data

        # Parse Break Feedback Room Feedback ink file
        ink_file_path: str = scenario_language_folder_data.feedback_room_folder_data.break_room_feedback_folder_data.feedback_ink_file_path
        audio_folder_path: str = scenario_language_folder_data.feedback_room_folder_data.break_room_feedback_folder_data.audio_folder_data.audio_folder_root_path
        room_name: str = scenario_language_folder_data.feedback_room_folder_data.break_room_feedback_folder_data.room_name
        room_dialogue_data: RoomDialogueData = self.parse_ink_script(audio_folder_path, ink_file_path, room_name)
        tts_dialogue_data.break_room_feedback_dialogue_data = room_dialogue_data

        # Parse Patient Feedback Room Feedback ink file
        ink_file_path: str = scenario_language_folder_data.feedback_room_folder_data.patient_room_feedback_folder_data.feedback_ink_file_path
        audio_folder_path: str = scenario_language_folder_data.feedback_room_folder_data.patient_room_feedback_folder_data.audio_folder_data.audio_folder_root_path
        room_name: str = scenario_language_folder_data.feedback_room_folder_data.patient_room_feedback_folder_data.room_name
        room_dialogue_data: RoomDialogueData = self.parse_ink_script(audio_folder_path, ink_file_path, room_name)
        tts_dialogue_data.patient_room_feedback_dialogue_data = room_dialogue_data

        return tts_dialogue_data

    def parse_ink_script(self, audio_folder_path: str, ink_file_path: str, room_name: str) -> RoomDialogueData:
        # TODO: Error handling
        room_dialogue_data: RoomDialogueData = RoomDialogueData()
        room_dialogue_data.room_name = room_name

        with open(ink_file_path, 'r', encoding=self.afsc.DEFAULT_FILE_ENCODING) as ink_file:
            lines = ink_file.readlines()
            line_number = 0
            for line in lines:
                audio_dialogue_data: AudioDialogueData = AudioDialogueData()
                line_number = line_number + 1
                # Log line number to Visual Logger - cutelog
                self.log.trace(str(line_number))
                string_to_parse = line.strip()
                if not string_to_parse:
                    continue
                elif string_to_parse.startswith("==="):
                    continue
                elif string_to_parse.startswith("->"):
                    continue
                elif string_to_parse.startswith("*"):
                    # TODO : #Highpriority Check the option string for the option letter/text
                    # TODO : Throw error if it has any option characters
                    # TODO : Check for valid emotion tags
                    match_list = re.findall(self.option_regular_expression, string_to_parse)
                    if len(match_list) >= 1:
                        match_group_tuple = match_list[0]
                        if len(match_group_tuple) >= 3:
                            option_text = match_group_tuple[1]
                            option_text_without_spaces = "".join(option_text.split())
                            if option_text_without_spaces.startswith(tuple(self.option_text_prefixes)):
                                # TODO : Check for other tags
                                pass
                            else:
                                log_text = str(line_number) + ' : ' + 'Not a valid option index. ' \
                                                                      'Option index can be in the range A-E or 1-5 and should have a dot character after the index. ' \
                                                                      'eg. (\'A.\' \'E.\' \'1.\' \'5.\')'
                                self.log.warning(log_text)
                    else:
                        # TODO: Log Error Wrong formatting for Option text
                        # TODO: If it is a feedback room text then ignore
                        log_text = "Line Number : " + str(line_number) + ' : ' + " Wrong formatting for Option text"
                        self.log.warning(log_text)
                    continue
                else:
                    self.log.trace("string_to_parse: " + string_to_parse)
                    text_to_display = string_to_parse.split("#")[0].strip()
                    # TODO: Check the length of the dialogue text and display error to the user
                    if len(text_to_display) > self.MAX_DIALOGUE_TEXT_CHARACTER_COUNT:
                        # TODO: Display error message by collecting this error data in a collection and display in the end
                        log_text = str(line_number) + ' : ' + 'Length exceeds max character count'
                        self.log.warning(log_text)
                        continue
                    string_without_name = string_to_parse.split(":", 1)
                    self.log.trace("string_without_name: " + str(string_without_name))
                    # TODO: Error Check for all the string operations
                    split_1 = string_without_name[1].split("\"")
                    self.log.trace("split_1: " + str(split_1))
                    dialogue_string = split_1[1].strip()
                    self.log.trace("dialogue_string: " + dialogue_string)
                    split_3 = split_1[2].strip()
                    self.log.trace("split_3: " + str(split_3))
                    split_4 = split_3.split("#")
                    self.log.trace("split_4: " + str(split_4))
                    audio_file_name = split_4[1].strip()
                    audio_file_name_with_extension = audio_file_name + self.DEFAULT_AUDIO_FILE_EXTENSION
                    self.log.debug("Dialogue Text: " + str(dialogue_string))
                    self.log.debug("Audio File Name: " + str(audio_file_name))
                    audio_file_path = os.path.join(audio_folder_path, audio_file_name_with_extension)
                    self.log.debug("Audio File Path: " + str(audio_file_path))
                    character_type = split_4[2].strip()
                    # TODO: Create a Dict with audio file names as the key
                    #   and contains a dictionary of text, character_type, audio_file_path
                    if audio_file_name in audio_dialogue_data:
                        # TODO: Error duplicate audio names
                        log_text = str(line_number) + ' : ' + 'Duplicate Audio file names, ' + audio_file_name
                        self.log.warning(log_text)
                        continue
                    else:
                        audio_dialogue_data.text = dialogue_string
                        audio_dialogue_data.audio_file_name = audio_file_name
                        audio_dialogue_data.audio_file_name_with_extension = audio_file_name_with_extension
                        audio_dialogue_data.audio_file_extension = self.DEFAULT_AUDIO_FILE_EXTENSION
                        audio_dialogue_data.audio_file_path = audio_file_path
                        audio_dialogue_data.character_type = character_type
                        room_dialogue_data.audio_dialogue_data_dict[audio_file_name] = audio_dialogue_data
                        # TODO: Error Handling: check the character type validity and log the error
                        #   For example, the BreakRoom only contains conversation between MedicalStudent & Player
                        #   if there is trainer as character in the break room script then it's not valid

        return room_dialogue_data
