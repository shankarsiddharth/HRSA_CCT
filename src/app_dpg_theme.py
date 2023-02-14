import dearpygui.dearpygui as dpg

from dearpygui_ext import themes


class AppTheme(object):

    def __init__(self):
        self.dark_theme = None
        self.light_theme = None

    def on_render(self):
        self.dark_theme = themes.create_theme_imgui_dark()
        self.light_theme = themes.create_theme_imgui_light()
