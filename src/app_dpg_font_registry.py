import dearpygui.dearpygui as dpg
from app_globals import afs


class AppFontRegistry(object):

    def __init__(self):
        self.default_font_registry = None
        self.default_font = None
        self.default_font_size = None
        self.default_font_bold = None
        self.default_font_bold_size = None
        self.default_font_italic = None
        self.default_font_mono = None
        self.default_font_mono_size = None

    def on_render(self):
        with dpg.font_registry():
            # first argument is the path to the .ttf or .otf file
            self.default_font = dpg.add_font(afs.get_default_font_file_path(), afs.get_default_font_size())
            self.default_font_bold = dpg.add_font(afs.get_default_bold_font_file_path(), afs.get_default_font_size())
