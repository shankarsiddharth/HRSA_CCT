import logging
from logging.handlers import SocketHandler

import os
from pathlib import Path
import hrsa_ui_logger
import hrsa_cct_constants

log_file_path = Path('hrsa_cct.log')
log_file = log_file_path
backup_log_file_path = Path('hrsa_cct.backup.log')
backup_log_file = backup_log_file_path
maximum_log_file_size_in_MBs = 10  # 10 MB
maximum_log_file_size_in_bytes = maximum_log_file_size_in_MBs * 1024 * 1024  # MBs to bytes

hrsa_cct_logger = logging.getLogger('HRSA CCT Log')
hrsa_cct_logger.setLevel(1)  # to send all records to log

# Attach SocketHandler - Visual Log Viewer - cutelog
socket_handler = SocketHandler('127.0.0.1', 19996)  # default listening address
hrsa_cct_logger.addHandler(socket_handler)

# Handle Log files
log_file_write_mode = 'a'
if log_file.is_file():
    # Log File Exists
    current_log_file_size = os.path.getsize(log_file)
    if current_log_file_size >= maximum_log_file_size_in_bytes:
        if backup_log_file.is_file():
            # Backup Log file Exists
            os.remove(backup_log_file_path)
            pass
        os.rename(log_file_path, backup_log_file_path)

# Attach File Logger
file_handler = logging.FileHandler(log_file_path, mode=log_file_write_mode)
file_formatter = logging.Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
file_handler.setFormatter(file_formatter)
hrsa_cct_logger.addHandler(file_handler)

# Test Logs
hrsa_cct_logger.log(1, '======================================== HRSA LOGGER STARTED ========================================')
hrsa_cct_logger.debug('======================================== HRSA LOGGER STARTED ========================================')
hrsa_cct_logger.debug('Test Debug')
hrsa_cct_logger.info('Test Info')
hrsa_cct_logger.warning('Test Warning')
hrsa_cct_logger.error('Test Error')
hrsa_cct_logger.critical('Test Critical')


class HRSALogger:

    def __init__(self):
        global hrsa_cct_logger
        self.ui_logger = None
        self.hrsa_cct_logger = hrsa_cct_logger
        self.log_level = 0
        self.count = 0
        # self.flush_count = 10000

    def init_ui_logger(self, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        self.ui_logger = hrsa_ui_logger.HRSAUILogger(parent=parent)
        self.ui_logger.trace("HRSA CCT UI Logger Started")
        self.ui_logger.log_debug('Test Debug')
        self.ui_logger.log_info('Test Info')
        self.ui_logger.log_warning('Test Warning')
        self.ui_logger.log_error('Test Error')
        self.ui_logger.log_critical('Test Critical')

    def _log(self, message, level, should_log_to_ui):

        if level < self.log_level:
            return

        self.count += 1

        # if self.count > self.flush_count:
        #     self.clear_log()

        if logging.NOTSET <= level < logging.DEBUG:
            self.hrsa_cct_logger.log(level=1, msg=message)
            if self.ui_logger is not None and should_log_to_ui:
                self.ui_logger.trace(message)

        elif level == logging.DEBUG:
            self.hrsa_cct_logger.debug(msg=message)
            if self.ui_logger is not None and should_log_to_ui:
                self.ui_logger.log_debug(message)

        elif level == logging.INFO:
            self.hrsa_cct_logger.info(msg=message)
            if self.ui_logger is not None and should_log_to_ui:
                self.ui_logger.log_info(message)

        elif level == logging.WARNING:
            self.hrsa_cct_logger.warning(msg=message)
            if self.ui_logger is not None and should_log_to_ui:
                self.ui_logger.log_warning(message)

        elif level == logging.ERROR:
            self.hrsa_cct_logger.error(msg=message)
            if self.ui_logger is not None and should_log_to_ui:
                self.ui_logger.log_error(message)

        elif level == logging.CRITICAL:
            self.hrsa_cct_logger.critical(msg=message)
            if self.ui_logger is not None:
                self.ui_logger.log_critical(message)

        print(message)

    def trace(self, message, should_log_to_ui=True):
        self._log(message, logging.NOTSET, should_log_to_ui)

    def debug(self, message, should_log_to_ui=True):
        self._log(message, logging.DEBUG, should_log_to_ui)

    def info(self, message, should_log_to_ui=True):
        self._log(message, logging.INFO, should_log_to_ui)

    def warning(self, message, should_log_to_ui=True):
        self._log(message, logging.WARNING, should_log_to_ui)

    def error(self, message, should_log_to_ui=True):
        self._log(message, logging.ERROR, should_log_to_ui)

    def critical(self, message, should_log_to_ui=True):
        self._log(message, logging.CRITICAL, should_log_to_ui)

    def clear_log(self):
        pass
