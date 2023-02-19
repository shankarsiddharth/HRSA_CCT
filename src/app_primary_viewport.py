import sys
import threading
import time

import dearpygui.dearpygui as dpg

import app_version as av
from app_dpg_font_registry import AppFontRegistry
from app_dpg_theme import AppTheme
from app_globals import afs, log, file_dialog
from app_queue import AppQueue
from app_primary_window import AppPrimaryWindow


class AppPrimaryViewportController(object):
    def __init__(self):
        self.exception_message = ''

        # Constants
        self.is_load_default_layout_clicked = False
        self.is_window_close_button_clicked = False


class AppPrimaryViewportUI(threading.Thread):
    __minimum_width__ = 1200
    __minimum_height__ = 900

    def __init__(self, controller=None, viewport_width=__minimum_width__, viewport_height=__minimum_height__):
        super().__init__()

        self.controller: AppPrimaryViewportController = controller
        self.application_queue: AppQueue = AppQueue()
        self.primary_window: AppPrimaryWindow = AppPrimaryWindow()

        self.exception = None
        self.exception_message = ''

        # DearPyGUI's Viewport Constants
        if viewport_width is None or viewport_width <= self.__minimum_width__:
            viewport_width = self.__minimum_width__
        if viewport_height is None or viewport_height <= self.__minimum_height__:
            viewport_height = self.__minimum_height__
        self.VIEWPORT_WIDTH = viewport_width
        self.VIEWPORT_HEIGHT = viewport_height
        self.viewport_title = "HRSA CCT " + " - " + av.APP_VERSION_STRING
        self.user_close_ui = False

        # TODO: Replace the below call to with a call to afs.get_dpg_ini_file_path()
        # self.dpg_ini_file_path = afs.get_dpg_ini_file_path()
        self.dpg_ini_file_path = "dpg.ini"

        # Initialize the DearPyGUI Related Objects
        self.app_theme = AppTheme()
        self.font_registry = AppFontRegistry()

    def run(self):
        try:
            if self.controller is None:
                exception_message = "Invalid arguments passed to the AppPrimaryViewportUI constructor."
                # TODO: Change this exception to application handled exception / application exception class => AppError
                raise Exception(exception_message)
            self.__render_ui__()
        except BaseException as e:
            self.exception = e
            application_queue: AppQueue = AppQueue()
            application_queue.put_app_instruction(application_queue.APP_EXCEPTION)

    def join(self, **kwargs):
        threading.Thread.join(self, **kwargs)
        # since join() returns in caller thread we re-raise the caught exception if any was caught
        if self.exception:
            raise self.exception

    def __exit_callback__(self):
        log.info("User clicked on the Close Window button.")
        application_queue: AppQueue = AppQueue()
        application_queue.put_app_instruction(application_queue.APP_EXIT)
        self.controller.is_window_close_button_clicked = True

    def button_callback(self):
        if dpg.get_item_configuration("Window 2")['show']:
            dpg.hide_item("Window 2")
        else:
            dpg.show_item("Window 2")
        log.info("User clicked on the Button.")
        if not file_dialog.is_active():
            file_dialog.request_tinker_file_dialog()

    def __render_ui__(self):

        dpg.create_context()

        # Bind a theme to the dpg application context
        self.app_theme.on_render()
        dpg.bind_theme(self.app_theme.dark_theme)

        self.font_registry.on_render()
        dpg.bind_font(self.font_registry.default_font)

        # TODO: Change this to use load_init_file instead of init_file and replace the path with self.dpg_ini_file_path
        dpg.configure_app(manual_callback_management=sys.flags.dev_mode, docking=True, docking_space=True,
                          load_init_file=self.dpg_ini_file_path, auto_device=True)

        # dpg.configure_app(manual_callback_management=sys.flags.dev_mode, docking=True, docking_space=True,
        #                   init_file=self.dpg_ini_file_path, auto_device=True)

        dpg.create_viewport(title=self.viewport_title, width=self.VIEWPORT_WIDTH, height=self.VIEWPORT_HEIGHT)

        dpg.set_exit_callback(callback=self.__exit_callback__)

        # TODO: Remove the code below and Add Proper Menu Bar
        # Menu Bar
        with dpg.viewport_menu_bar():
            with dpg.menu(label="UI", tag="UI"):
                dpg.add_menu_item(label="Save ini", tag="Save ini",
                                  callback=lambda: dpg.save_init_file(self.dpg_ini_file_path))

        # TODO: Add Windows
        self.primary_window.on_render_ui()

        # with dpg.window(label="Window 1", tag="Window 1", width=300, height=300, no_resize=False, no_move=False, no_close=True, no_collapse=True):
        #     dpg.add_button(label="Button 1", tag="Button 1", callback=self.button_callback)
        #
        #     with dpg.child_window(tag="Window 2", label="Window 2", width=150, height=150, show=False):
        #         dpg.add_button(tag="Button 2", label="Button 2", callback=self.button_callback)

        dpg.setup_dearpygui()
        # dpg.maximize_viewport()
        dpg.show_viewport()

        # below replaces, start_dearpygui()
        while dpg.is_dearpygui_running():

            if sys.flags.dev_mode:
                jobs = dpg.get_callback_queue()  # retrieves and clears queue
                dpg.run_callbacks(jobs)

            if file_dialog.is_active():
                file_path = self.application_queue.get_file_path()
                print("Received File Path: ", file_path)
                dpg.focus_item("Window 1")

            # global is_load_default_layout_clicked
            if self.controller.is_load_default_layout_clicked or self.controller.is_window_close_button_clicked:
                dpg.stop_dearpygui()

            dpg.render_dearpygui_frame()

        log.close_ui()
        dpg.destroy_context()

        if self.controller.is_load_default_layout_clicked:
            # TODO: Add functionality to reset to default layout
            # self.reset_to_default_layout()
            pass


class AppPrimaryViewport(object):

    def init_and_render_ui(self):
        while not self.controller.is_window_close_button_clicked:
            self.ui = AppPrimaryViewportUI(self.controller)
            self.ui.start()

            self.__process_queue__()

            try:
                self.ui.join()
            except BaseException as e:
                raise e
            finally:
                if self.controller.is_load_default_layout_clicked:
                    self.controller.is_window_close_button_clicked = False
                    self.controller.is_load_default_layout_clicked = False
                    continue

    def __process_queue__(self):
        while True:
            try:
                file_dialog_instruction = self.application_queue.get_file_dialog_instruction(block=False)
                if file_dialog_instruction is not None:
                    if file_dialog_instruction == self.application_queue.FILE_DIALOG_INSTRUCTION_SHOW:
                        file_dialog.show_file_dialog()
            except BaseException as e:
                time.sleep(0.0001)
            try:
                app_instruction = self.application_queue.get_app_instruction(block=False)
                if app_instruction is not None:
                    if app_instruction == self.application_queue.APP_EXCEPTION \
                            or app_instruction == self.application_queue.APP_EXIT:
                        break
            except BaseException as e:
                time.sleep(0.0001)
                continue

    def __init__(self):
        self.controller = AppPrimaryViewportController()
        self.ui = None  # Initialized in init_and_render_ui()

        self.application_queue: AppQueue = AppQueue()

        self.init_and_render_ui()

        if self.ui is not None:
            if self.ui.user_close_ui:
                # TODO: Change this exception to application handled exception / application exception class => AppExit
                raise Exception()
