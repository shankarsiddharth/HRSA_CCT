import logging
import os
import pathlib
import sys
import threading
import traceback
from logging.handlers import SocketHandler

import app_logging_custom as alc
from app_file_system_constants import AppFileSystemConstants
from app_file_system import AppFileSystem
from app_logger_ui import AppUILogger


class AppLogger(object):
    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppLogger, cls).__new__(cls)
                    cls._instance.__initialize__()
                    if sys.flags.dev_mode:
                        print("AppLogger.__new__()")
        return cls._instance

    def __initialize__(self):
        self.afsc = AppFileSystemConstants()
        self.afs = AppFileSystem()
        self.should_log_to_ui = True

        print("Creating Logger Instance...")

        print("Getting root folder...")
        root_folder_path = self.afs.get_root_folder()

        print("Checking log folder...")
        self.log_folder_path = os.path.join(root_folder_path, self.afsc.LOG_FOLDER_NAME)
        self.log_folder = pathlib.Path(self.log_folder_path)
        if not self.log_folder.exists():
            print("Log folder does not exist. Creating it.")
            print("Creating log folder: " + self.log_folder_path)
            try:
                os.makedirs(self.log_folder_path)
            except OSError as e:
                traceback_string = traceback.format_exc()
                exception_message = ("Creation of the log folder %s failed" % self.log_folder_path) + str(e) + "\n" + traceback_string
                print(exception_message)

        print("Log Folder exists.")
        self.log_file_path = os.path.join(self.log_folder_path, self.afsc.LOG_FILE_NAME)

        self.backup_log_file_path = os.path.join(self.log_folder_path, self.afsc.BACKUP_LOG_FILE_NAME)

        self.log_file = pathlib.Path(self.log_file_path)
        self.backup_log_file = pathlib.Path(self.backup_log_file_path)
        maximum_log_file_size_in_megabytes = 10  # 10 MB
        maximum_log_file_size_in_bytes = maximum_log_file_size_in_megabytes * 1024 * 1024  # MBs to bytes

        self.logger_instance = logging.getLogger('HRSA CCT Log')
        self.logger_instance.setLevel(1)  # to send all records to log

        # Attach a console handler to the logger
        console_handler = logging.StreamHandler(stream=sys.stdout)
        # create formatter
        console_formatter = logging.Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        console_handler.setFormatter(console_formatter)
        self.logger_instance.addHandler(console_handler)

        # Attach SocketHandler - Visual Log Viewer - cutelog
        socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
        self.logger_instance.addHandler(socket_handler)

        # Handle Log files
        log_file_write_mode = 'a'
        if self.log_file.is_file():
            # Log File Exists
            current_log_file_size = os.path.getsize(self.log_file)
            if current_log_file_size >= maximum_log_file_size_in_bytes:
                if self.backup_log_file.is_file():
                    # Backup Log file Exists
                    os.remove(self.backup_log_file_path)
                os.rename(self.log_file_path, self.backup_log_file_path)
        else:
            # Log File Does Not Exist
            log_file_write_mode = 'w'
            with open(self.log_file_path, log_file_write_mode) as log_file:
                log_file.write('')

        # Attach File Logger
        file_handler = logging.FileHandler(self.log_file_path, mode=log_file_write_mode, encoding="UTF-8")
        file_formatter = logging.Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        file_handler.setFormatter(file_formatter)
        self.logger_instance.addHandler(file_handler)

        # Test Logs
        # self.logger_instance.log(1, '======================================== HRSA CCT LOGGER STARTED ========================================')
        self.logger_instance.debug('======================================== HRSA CCT LOGGER STARTED ========================================')
        # self.logger_instance.debug('Test Debug')
        # self.logger_instance.info('Test Info')
        # self.logger_instance.log(c_logging.log_level_success, 'Test Success')
        # self.logger_instance.warning('Test Warning')
        # self.logger_instance.error('Test Error')
        # self.logger_instance.critical('Test Critical')

        self.ui_logger = None
        self.log_level = 0
        self.count = 0
        # self.flush_count = 10000

    def on_init_and_render_ui(self, parent=None):
        self.ui_logger: AppUILogger = AppUILogger(parent=parent)
        self.ui_logger.trace("HRSA CCT UI Logger Started")
        if sys.flags.dev_mode:
            self.ui_logger.debug('Test UI Debug')
            self.ui_logger.info('Test UI Info')
            self.ui_logger.success('Test UI Success')
            self.ui_logger.warning('Test UI Warning')
            self.ui_logger.error('Test UI Error')
            self.ui_logger.critical('Test UI Critical')

            self.debug('Test Debug')
            self.info('Test Info')
            self.success('Test Success')
            self.warning('Test Warning')
            self.error('Test Error')
            self.critical('Test Critical')

    def close_ui(self):
        if self.ui_logger is not None:
            self.ui_logger = None

    def _log(self, level, message, *args):

        if level < self.log_level:
            return

        self.count += 1

        # if self.count > self.flush_count:
        #     self.clear_log()

        self.log_message = message
        if args:
            self.log_message = message % args

        if logging.NOTSET <= level < logging.DEBUG:
            self.logger_instance.log(1, message, *args)
            if self.ui_logger is not None and self.should_log_to_ui:
                self.ui_logger.trace(message, *args)

        elif level == logging.DEBUG:
            self.logger_instance.debug(message, *args)
            if self.ui_logger is not None and self.should_log_to_ui:
                self.ui_logger.debug(message, *args)

        elif level == logging.INFO:
            self.logger_instance.info(message, *args)
            if self.ui_logger is not None and self.should_log_to_ui:
                self.ui_logger.info(message, *args)

        elif level == alc.log_level_success:
            self.logger_instance.log(alc.log_level_success, message, *args)
            if self.ui_logger is not None and self.should_log_to_ui:
                self.ui_logger.success(message, *args)

        elif level == logging.WARNING:
            self.logger_instance.warning(message, *args)
            if self.ui_logger is not None and self.should_log_to_ui:
                self.ui_logger.warning(message, *args)

        elif level == logging.ERROR:
            self.logger_instance.error(message, *args)
            if self.ui_logger is not None and self.should_log_to_ui:
                self.ui_logger.error(message, *args)

        elif level == logging.CRITICAL:
            self.logger_instance.critical(message, *args)
            if self.ui_logger is not None:
                self.ui_logger.critical(message, *args)

        # print(message)

    def trace(self, message, *args: object):
        self._log(logging.NOTSET, message, *args)

    def debug(self, message, *args: object):
        self._log(logging.DEBUG, message, *args)

    def info(self, message, *args: object):
        self._log(logging.INFO, message, *args)

    def success(self, message, *args: object):
        self._log(alc.log_level_success, message, *args)

    def warning(self, message, *args: object):
        self._log(logging.WARNING, message, *args)

    def error(self, message, *args: object):
        self._log(logging.ERROR, message, *args)

    def critical(self, message, *args: object):
        self._log(logging.CRITICAL, message, *args)

    def exception(self, message, *args: object):
        self.logger_instance.exception(message, *args)
        if self.ui_logger is not None:
            self.ui_logger.exception(message, *args)

    def clear_log(self):
        pass
