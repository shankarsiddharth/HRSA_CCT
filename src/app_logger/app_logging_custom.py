# ****************************************************************************************************************************************************************

# ========================== START Log Constants ===================================
import logging

from app_debug.app_debug import IS_DEBUG_MODE_ENABLED

log_level_success = logging.INFO + 5
log_level_exception = logging.CRITICAL + 10
logging.addLevelName(log_level_success, "SUCCESS")
logging.addLevelName(log_level_exception, "EXCEPTION")
if IS_DEBUG_MODE_ENABLED:
    print("AppLoggingCustom.__init__()")
# ========================== END Log Constants ===================================

# ****************************************************************************************************************************************************************
