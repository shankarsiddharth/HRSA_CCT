from app_globals import log
from app_globals import afsc
from app_globals import afs
from app_primary_viewport import AppPrimaryViewport

log.info("Application Started.")
root_folder = afs.get_root_folder()
log.info(f"Root Folder: {root_folder}")
default_font = afsc.DEFAULT_FONT_NAME
log.info(f"Default Font: {default_font}")
log.info("Application Finished.")

AppPrimaryViewport()
