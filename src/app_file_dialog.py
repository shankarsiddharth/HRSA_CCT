import sys
import threading
from tkinter import *
from tkinter.filedialog import askopenfilename

from app_queue import AppQueue


class AppFileDialog(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    if sys.flags.dev_mode:
                        print("AppFileDialog.__new__()")
                    cls._instance = super(AppFileDialog, cls).__new__(cls)
                    cls._instance.__initialize__()
        return cls._instance

    def __initialize__(self):

        self.__application_queue__: AppQueue = AppQueue()

        # Tinker UI Root
        self.__tk_root__ = Tk()
        self.__tk_root__.attributes("-topmost", True)
        self.__tk_root__.withdraw()  # we don't want a full GUI, so keep the root window from appearing

        self.__is_file_dialog_active__: bool = False
        self.__file_path__: str = ""
        self.__folder_path__: str = ""

    def is_active(self):
        with self._lock:
            return self.__is_file_dialog_active__

    def request_tinker_file_dialog(self):
        with self._lock:
            self.__is_file_dialog_active__ = True
            self.__application_queue__.put_file_dialog_instruction()

    def show_file_dialog(self):
        self.__file_path__ = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        with self._lock:
            self.__is_file_dialog_active__ = False
        if self.__file_path__ != "":
            self.__application_queue__.put_file_path(self.__file_path__)
        else:
            self.__application_queue__.clear_file_path()
            self.__application_queue__.put_file_path("")
