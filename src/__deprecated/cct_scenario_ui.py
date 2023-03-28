import dearpygui.dearpygui as dpg

from __deprecated import cct_ui_panels


def get_scenario_list():

    pass


def init_ui():
    with dpg.collapsing_header(label="Select Scenario", tag=cct_ui_panels.SELCET_SCENARIO_COLLAPSING_HEADER,
                               default_open=False):
        dpg.add_separator()
