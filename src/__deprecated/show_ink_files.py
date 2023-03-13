import dearpygui.dearpygui as dpg

from __deprecated import hrsa_cct_constants


def init_ui():
    with dpg.collapsing_header(label="Ink Files", default_open=False, parent=hrsa_cct_constants.HRSA_CCT_TOOL):

        dpg.add_separator()
