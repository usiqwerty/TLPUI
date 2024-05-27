"""Toggle config state."""

from gi.repository import Gtk

import tlpui.config_actions
import tlpui.views.application
from tlpui import settings


def create_toggle_button(configname: str, configwidget: Gtk.Widget, window: Gtk.Window) -> Gtk.CheckButton:
    """Create state toggle."""
    togglebutton = Gtk.CheckButton()

    if settings.tlp_config[configname].is_enabled():
        togglebutton.set_active(True)
    else:
        configwidget.set_sensitive(False)

    togglebutton.connect('toggled', on_button_toggled, configname, configwidget, window)
    return togglebutton


def on_button_toggled(self: Gtk.CheckButton, configname: str, configwidget: Gtk.Widget, window: Gtk.Window):
    """Process and store config state."""
    tlpobject = settings.tlp_config[configname]

    if self.get_active():
        tlpobject.set_enabled(True)
        configwidget.set_sensitive(True)

        # Reset to default when intrinsic default gets reactivated
        if tlpobject.get_value() == "" and settings.tlp_config_defaults[configname].is_enabled():
            tlpobject.set_value(settings.tlp_config_defaults[configname].get_value())
            tlpui.views.main_box.load_tlp_config(self, window, False)
    else:
        tlpobject.set_enabled(False)
        configwidget.set_sensitive(False)

        # If intrinsic default gets deactivated we have to remove value
        if settings.tlp_config_defaults[configname].is_enabled():
            tlpobject.set_value("")
