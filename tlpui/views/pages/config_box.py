from gi.repository import Gtk

from tlpui import settings
from tlpui.tlp_config.configui import store_scroll_position, store_category_num
from tlpui.tlp_config.config_category import get_tlp_categories
from tlpui.uihelper import get_theme_image
from tlpui.views.pages.page import AppPage
from tlpui.views.settings_box import create_settings_box


class ConfigPage(AppPage):
    window: Gtk.Window
    name = "Configuration"
    def __init__(self, window: Gtk.Window):
        self.window = window

    def create_box(self) -> Gtk.Box:
        """Create TLP config box."""
        notebook = Gtk.Notebook()
        notebook.set_name('configNotebook')
        notebook.set_tab_pos(Gtk.PositionType.LEFT)

        tlp_categories = get_tlp_categories(self.window)
        for name, category_data in tlp_categories.items():
            viewport = Gtk.Viewport()
            viewport.set_name(f'categoryViewport_{name}')
            viewport.add(category_data[1])

            scroll = Gtk.ScrolledWindow()
            scroll.add(viewport)
            scroll.connect("scroll-event", store_scroll_position)

            category_image = get_theme_image(f'tlpui-{name.replace(" ", "-")}-symbolic', Gtk.IconSize.MENU)

            label_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            label_box.pack_start(category_image, False, False, 0)
            label_box.pack_start(category_data[0], True, True, 0)
            label_box.show_all()

            notebook.append_page(scroll, label_box)

        notebook.connect('switch-page', store_category_num)

        config_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        config_box.pack_start(notebook, True, True, 0)

        active_category = settings.user_config.active_category
        notebook.show_all()
        notebook.set_current_page(active_category)

        return config_box

    def create_content_box(self, load_tlp_config):
        settingsbox = create_settings_box(self.window, load_tlp_config)
        configbox = self.create_config_box()
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(18)
        content_box.set_margin_bottom(18)
        content_box.set_margin_left(18)
        content_box.set_margin_right(18)
        content_box.pack_start(settingsbox, False, False, 0)
        content_box.pack_start(configbox, True, True, 0)
        return content_box