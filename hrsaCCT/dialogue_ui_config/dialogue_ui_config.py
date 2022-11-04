import json
import os.path

import dearpygui.dearpygui as dpg

import hrsa_cct_constants


# GUI Element Tags


# Module Variables


def init_ui():
    with dpg.collapsing_header(label="Dialogue UI Config", default_open=True, parent=hrsa_cct_constants.HRSA_CCT_TOOL):
        # TODO: UI Creation

        dpg.add_text(tag="DIALOGUE")
