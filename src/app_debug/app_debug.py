import os
import sys
import threading


class AppDebug(object):
    __is_debug_mode_enabled__: bool = None

    __HRSA_CCT_DEBUG_MODE__: str = 'HRSA_CCT_DEBUG_MODE'

    _instance = None

    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppDebug, cls).__new__(cls)
                    cls.__initialize__()
                    if cls.__is_debug_mode_enabled__:
                        print("AppDebug.__new__()")
        return cls._instance

    @classmethod
    def __initialize__(cls):
        # Check if the app is running in debug mode or not.
        # Check the '-X dev' flag in the python interpreter command line options.
        if sys.flags.dev_mode:
            cls.__is_debug_mode_enabled__ = True
        # Check the command line arguments.
        if len(sys.argv) > 1:
            if '--debug' in sys.argv or '-d' in sys.argv:
                cls.__is_debug_mode_enabled__ = True
        # Check the HRSA_CCT_DEBUG_MODE environment variable and the value of 1.
        os_env_value = os.environ.get(cls.__HRSA_CCT_DEBUG_MODE__)
        if os_env_value is not None:
            if os_env_value == '1':
                cls.__is_debug_mode_enabled__ = True
        # If the debug mode is not enabled, set the default value to False.
        if cls.__is_debug_mode_enabled__ is None:
            cls.__is_debug_mode_enabled__ = False

    def is_debug_mode_enabled(self) -> bool:
        if self.__is_debug_mode_enabled__ is None:
            if self._instance is None:
                self._instance = AppDebug()
        if self.__is_debug_mode_enabled__ is None:
            self.__is_debug_mode_enabled__ = False
        return self.__is_debug_mode_enabled__


__app_debug_instance__: AppDebug = AppDebug()

IS_DEBUG_MODE_ENABLED: bool = __app_debug_instance__.is_debug_mode_enabled()
