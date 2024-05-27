"""Create TLP config UI."""

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from tlpui import settings
from tlpui.tlp_config.ui_config_objects import gtkentry
from tlpui.tlp_config.ui_config_objects import gtkspinbutton, gtkswitch, gtkcheckbutton, gtkpcilist, gtkdisklistview, \
    gtkusblist, gtkselection, gtkmultiselection, gtkdisklist
from tlpui.config_parser.types import ConfType, TlpConfigItem
from tlpui.uihelper import StateImage


def store_category_num(self, cat, cat_num: int):
    """Store selected config category."""
    settings.user_config.active_category = cat_num
    # settings.userconfig.activeposition = self.get_children()[cat_num].get_vadjustment().get_value()
    settings.active_scroll = self.get_children()[cat_num]


def store_scroll_position(self, event):
    """Store current scrolled position."""
    settings.user_config.active_position = self.get_vadjustment().get_value()


def create_config_widget(configname: str, objecttype: str, objectvalues: str, window: Gtk.Window) -> Gtk.Widget:
    """Create config widget."""
    configwidget = Gtk.Widget

    if objecttype == 'entry':
        configwidget = gtkentry.create_entry(configname)
    elif objecttype == 'usblist':
        configwidget = gtkusblist.create_list(configname, window)
    elif objecttype == 'pcilist':
        configwidget = gtkpcilist.create_list(configname, window)
    elif objecttype == 'disklist':
        configwidget = gtkdisklist.create_list(configname, window)
    elif objecttype == 'disklistview':
        configwidget = gtkdisklistview.create_view(configname)
    elif objecttype == 'bselect':
        configwidget = gtkswitch.create_state_switch(configname, objectvalues)
    elif objecttype == 'select':
        configwidget = gtkselection.create_selection_box(configname, objectvalues)
    elif objecttype == 'multiselect':
        configwidget = gtkmultiselection.create_multi_selection_box(configname, objectvalues)
    elif objecttype == 'check':
        configwidget = gtkcheckbutton.create_checkbutton_box(configname, objectvalues)
    elif objecttype == 'numeric':
        configwidget = gtkspinbutton.create_numeric_spinbutton(configname, objectvalues)

    return configwidget


def init_state_image(configname: str):
    """Create and store state image."""
    image = Gtk.Image()
    defaultvalue = settings.tlp_config_defaults[configname].get_value()
    defaultstate = settings.tlp_config_defaults[configname].is_enabled()
    settings.tlp_config[configname].add_state_image(StateImage(defaultvalue, defaultstate, image))
    return image


def get_type_image(configname: str) -> Gtk.Image:
    """Create config location image."""
    tlpconfig = settings.tlp_config[configname]  # type: TlpConfigItem
    conftype = tlpconfig.get_conf_type()
    conftypeimage = Gtk.Image()

    if conftype == ConfType.DROPIN:
        conftypeimage = Gtk.Image.new_from_file(f'{settings.icon_dir}dropin.svg')
        conftypeimage.set_tooltip_text(tlpconfig.get_conf_path())
    elif conftype == ConfType.USER:
        conftypeimage = Gtk.Image.new_from_file(f'{settings.icon_dir}user.svg')
        conftypeimage.set_tooltip_text(tlpconfig.get_conf_path())

    return conftypeimage


class ConfigObject:
    """Config object helper class."""

    def __init__(self, name: str, datatype: str, values: str):
        """Init config object helper class parameters."""
        self.name = name
        self.datatype = datatype
        self.values = values
