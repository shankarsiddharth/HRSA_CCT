import queue
import sys
import threading


class AppQueue(object):
    _instance = None

    _lock = threading.Lock()

    # Class Constants
    FILE_DIALOG_INSTRUCTION_SHOW = "ShowFileDialog"
    APP_EXIT = "AppExit"
    APP_EXCEPTION = "AppException"

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppQueue, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if sys.flags.dev_mode:
                        print("AppQueue.__new__()")
        return cls._instance

    def __initialize__(self):
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
