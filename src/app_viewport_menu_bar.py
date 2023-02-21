import dearpygui.dearpygui as dpg

import app_version as av

# TODO: Implement the AppViewportMenuBar class & functionality

class AppViewportMenuBarController(object):
    pass


class AppViewportMenuBarUI(object):
    def __init__(self, controller: AppViewportMenuBarController):
        self.controller = controller

        # Menu Bar
        self.viewport_menu_bar_tag = "Viewport Menu Bar"
        # UI Menu
        self.ui_menu_tag = "UI"
        self.save_current_layout_to_dpg_ini_tag = "Save current layout to dpg.ini"
        self.reset_to_default_layout_tag = "Reset to default layout"
        # About Menu
        self.about_menu_tag = "About"
        self.about_menu_version_tag = "App Version"

    # def on_render_ui(self):
    #     # Menu Bar
    #     with dpg.viewport_menu_bar(tag=):
    #         # UI Menu
    #         with dpg.menu(label=self.ui_menu_tag, tag=self.ui_menu_tag):
    #             dpg.add_menu_item(label=self.save_current_layout_to_dpg_ini_tag, tag=self.save_current_layout_to_dpg_ini_tag,
    #                               callback=lambda: dpg.save_init_file(self.dpg_ini_file_path))
    #             # dpg.add_menu_item(label=self.reset_to_default_layout_tag, tag=self.reset_to_default_layout_tag, callback=self.load_default_layout)
    #         # # About Menu
    #         # with dpg.menu(label=self.about_menu_tag, tag=self.about_menu_tag):
    #         #     dpg.add_menu_item(label=av.APP_VERSION_STRING, tag=self.about_menu_version_tag, callback=self.about_callback)


class AppViewportMenuBar(object):
    def __init__(self):
        self.controller = AppViewportMenuBarController()
        self.ui = AppViewportMenuBarUI(self.controller)

    # def on_render_ui(self):
    #     self.ui.on_render_ui()
