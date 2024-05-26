from gi.repository import Gtk

from tlpui import language, settings
from tlpui.tlp_config.configui import create_config_box
from tlpui.config_parser.file import init_tlp_file_config
from tlpui.views.menu import create_menu_box
from tlpui.views.statui import create_stat_box
from tlpui.views.settings_box import create_settings_box


def create_main_box(window: Gtk.Window) -> Gtk.Box:
    """Create TLP configuration items notebook view."""
    notebook = Gtk.Notebook()
    notebook.set_tab_pos(Gtk.PositionType.TOP)

    menubox = create_menu_box(window, load_tlp_config)
    settingsbox = create_settings_box(window, load_tlp_config)
    configbox = create_config_box(window)

    contentbox = create_content_box(configbox, settingsbox)
    configlabel = Gtk.Label(language.MT_('Configuration'))
    configlabel.set_hexpand(True)
    notebook.append_page(contentbox, configlabel)


    statlabel = Gtk.Label(language.MT_('Statistics'))
    statlabel.set_hexpand(True)
    statbox = create_stat_box()
    notebook.append_page(statbox, statlabel)

    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
    mainbox.pack_start(menubox, False, False, 0)
    mainbox.pack_start(notebook, True, True, 0)

    notebook.connect('switch-page', store_option_num)

    notebook.show_all()
    notebook.set_current_page(settings.userconfig.activeoption)

    return mainbox


def create_content_box(configbox, settingsbox):
    contentbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
    contentbox.set_margin_top(18)
    contentbox.set_margin_bottom(18)
    contentbox.set_margin_left(18)
    contentbox.set_margin_right(18)
    contentbox.pack_start(settingsbox, False, False, 0)
    contentbox.pack_start(configbox, True, True, 0)
    return contentbox


def store_option_num(self, option, option_num: int):
    """Store selected functionality option."""
    settings.userconfig.activeoption = option_num


def load_tlp_config(_, window: Gtk.Window, reloadtlpconfig: bool) -> None:
    """Load TLP configuration to UI."""
    if reloadtlpconfig:
        init_tlp_file_config()

    new_mainbox = create_main_box(window)
    children = window.get_children()
    for child in children:
        window.remove(child)
    window.add(new_mainbox)
    window.show_all()
    while Gtk.events_pending():
        Gtk.main_iteration()

    #reset scroll position
    settings.active_scroll.get_vadjustment().set_value(settings.userconfig.activeposition)


