from app_globals import afsc, afs, log
from app_primary_viewport import AppPrimaryViewport
from app_startup.app_startup import AppStartup

AppStartup()

log.info("Application Started.")
root_folder = afs.get_root_folder_path()
log.info(f"Root Folder: {root_folder}")
default_font = afsc.DEFAULT_FONT_NAME
log.info(f"Default Font: {default_font}")

AppPrimaryViewport()
