import sys

CREATE_SCENARIO_COLLAPSING_HEADER: str = 'CREATE_SCENARIO_COLLAPSING_HEADER'
COPY_SCENARIO_COLLAPSING_HEADER: str = 'COPY_SCENARIO_COLLAPSING_HEADER'
SELECT_SCENARIO_COLLAPSING_HEADER: str = 'SELECT_SCENARIO_COLLAPSING_HEADER'
CCT_PATIENT_INFO_COLLAPSING_HEADER: str = 'CCT_PATIENT_INFO_COLLAPSING_HEADER'
CCT_SCENARIO_CONFIG_COLLAPSING_HEADER: str = 'CCT_SCENARIO_CONFIG_COLLAPSING_HEADER'
SHOW_INK_FILES_COLLAPSING_HEADER: str = 'SHOW_INK_FILES_COLLAPSING_HEADER'
AUDIO_GENERATION_COLLAPSING_HEADER: str = "AUDIO_GENERATION_COLLAPSING_HEADER"
TRANSLATE_COLLAPSING_HEADER: str = "TRANSLATE_COLLAPSING_HEADER"
TRANSFER_TO_DEVICE_COLLAPSING_HEADER: str = "TRANSFER_TO_DEVICE_COLLAPSING_HEADER"

if sys.flags.dev_mode:
    print("cct_ui_panels.__init__()")
