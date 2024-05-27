from gi.repository import Gtk

from tlpui import language, settings
from tlpui.editor import Editor
from tlpui.views.pages.config_box import ConfigPage
from tlpui.config_parser.file import init_tlp_file_config
from tlpui.views.menu import MenuBar
from tlpui.views.pages.stat_page import StatisticsPage
from tlpui.views.settings_box import create_settings_box


class EditorGUI:
    window: Gtk.Window
    editor: Editor

    def __init__(self, gtk_window: Gtk.Window):
        self.window = gtk_window

    def generate_gtk_box(self) -> Gtk.Box:
        """Create TLP configuration items notebook view."""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        menu = MenuBar(self.window, self.load_tlp_config).create_menu_box()
        notebook = self.create_notebook()

        main_box.pack_start(menu, False, False, 0)
        main_box.pack_start(notebook, True, True, 0)

        return main_box

    def create_notebook(self):
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)

        pages = [
            ConfigPage(self.window),
            StatisticsPage()
        ]
        # config_page = ConfigPage(self.window)
        # contentbox = config_page.create_content_box(self.load_tlp_config)
        # configlabel = Gtk.Label(language.MT_('Configuration'))
        # configlabel.set_hexpand(True)
        # notebook.append_page(contentbox, configlabel)
        #
        # stat_page = StatisticsPage()
        # statbox = stat_page.create_stat_box()
        # statlabel = Gtk.Label(language.MT_('Statistics'))
        # statlabel.set_hexpand(True)
        # notebook.append_page(statbox, statlabel)
        #
        for page in pages:
            page.append_to_notebook(notebook)

        notebook.connect('switch-page', store_option_num)
        notebook.show_all()

        notebook.set_current_page(settings.userconfig.active_page)
        return notebook

    def load_tlp_config(self, reload_tlp_config: bool) -> None:
        """Load TLP configuration to UI."""
        if reload_tlp_config:
            init_tlp_file_config()

        new_main_box = self.generate_gtk_box()  # create_main_box(window)
        children = self.window.get_children()
        for child in children:
            self.window.remove(child)
        self.window.add(new_main_box)
        self.window.show_all()

        while Gtk.events_pending():
            Gtk.main_iteration()

        # reset scroll position
        settings.active_scroll.get_vadjustment().set_value(settings.userconfig.activeposition)


def store_option_num(self, option, option_num: int):
    """Store selected functionality option."""
    settings.userconfig.active_page = option_num
