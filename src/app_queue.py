import queue

from classes.singleton import Singleton


class AppQueue(metaclass=Singleton):
    # Class Constants
    FILE_DIALOG_INSTRUCTION_SHOW = "ShowFileDialog"
    APP_EXIT = "AppExit"
    APP_EXCEPTION = "AppException"

    def __init__(self):
        self.__file_dialog_instruction_queue__ = queue.LifoQueue(maxsize=1)
        self.__file_path_queue__ = queue.LifoQueue(maxsize=1)
        self.__app_instruction_queue__ = queue.LifoQueue(maxsize=1)

    def put_file_dialog_instruction(self, item=FILE_DIALOG_INSTRUCTION_SHOW, block=True, timeout=None):
        self.__file_dialog_instruction_queue__.put(item, block, timeout)

    def get_file_dialog_instruction(self, block=True, timeout=None):
        return self.__file_dialog_instruction_queue__.get(block, timeout)

    def put_file_path(self, item, block=True, timeout=None):
        self.__file_path_queue__.put(item, block, timeout)

    def get_file_path(self, block=True, timeout=None):
        return self.__file_path_queue__.get(block, timeout)

    def put_app_instruction(self, item, block=True, timeout=None):
        self.__app_instruction_queue__.put(item, block, timeout)

    def get_app_instruction(self, block=True, timeout=None):
        return self.__app_instruction_queue__.get(block, timeout)

    def clear_file_path(self):
        while not self.__file_path_queue__.empty():
            self.__file_path_queue__.get(block=True, timeout=None)
