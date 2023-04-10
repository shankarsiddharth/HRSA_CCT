from app_debug.app_debug import IS_DEBUG_MODE_ENABLED

APP_VERSION_MAJOR = 0
APP_VERSION_MINOR = 0
APP_VERSION_PATCH = 2
APP_RELEASE_TYPE = "internal_test"
APP_VERSION_PREFIX = "v"
if APP_RELEASE_TYPE != "":
    APP_RELEASE_TYPE = f"-{APP_RELEASE_TYPE}"
APP_VERSION_STRING = f"{APP_VERSION_PREFIX}{APP_VERSION_MAJOR}.{APP_VERSION_MINOR}.{APP_VERSION_PATCH}{APP_RELEASE_TYPE}"

if IS_DEBUG_MODE_ENABLED:
    print("AppVersion.__init__()")
