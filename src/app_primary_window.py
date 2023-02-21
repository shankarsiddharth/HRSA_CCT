import dearpygui.dearpygui as dpg


class AppPrimaryWindowController(object):
    pass


class AppPrimaryWindowUI(object):
    def __init__(self, controller: AppPrimaryWindowController):
        self.controller = controller

        self.window_title = "App Primary Window"

    def on_render_ui(self):
        with dpg.window(label=self.window_title, tag=self.window_title, no_title_bar=False, no_close=True):
            dpg.add_text("Hello, world!")

        pass


class AppPrimaryWindow(object):
    def __init__(self):
        self.controller = AppPrimaryWindowController()
        self.ui = AppPrimaryWindowUI(self.controller)

    def on_render_ui(self):
        self.ui.on_render_ui()

    def get_window_title(self):
        return self.ui.window_title
