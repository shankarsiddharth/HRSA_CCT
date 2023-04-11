import logging

from app_debug.app_debug import IS_DEBUG_MODE_ENABLED

# region Log Constants
LOG_LEVEL_SUCCESS = logging.INFO + 5
LOG_LEVEL_EXCEPTION = logging.CRITICAL + 10
logging.addLevelName(LOG_LEVEL_SUCCESS, "SUCCESS")
logging.addLevelName(LOG_LEVEL_EXCEPTION, "EXCEPTION")
if IS_DEBUG_MODE_ENABLED:
    print("AppLoggingCustom.__init__()")
# endregion Log Constants
