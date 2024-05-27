#!/usr/bin/env python3
"""Entrypoint for UI."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

from . import settings
from .css import get_css_provider
from tlpui.config_parser.file import init_tlp_file_config
from tlpui.window_events import window_key_events_handler, close_main_window
from tlpui.views.application import ApplicationGUI

Gtk.init()
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    get_css_provider(),
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)

# Set window properties
GLib.set_prgname('tlp-ui')
Gdk.set_program_class('Tlp-UI')

# Apply custom scalable icons to icon theme
Gtk.IconTheme().get_default().append_search_path(settings.icon_dir + 'themeable')


def store_window_size(self) -> None:
    """Store current window size in settings."""
    settings.user_config.window_width = self.get_size()[0]
    settings.user_config.window_height = self.get_size()[1]


def main() -> None:
    """Initiate main window with all sub elements."""
    # init configuration settings
    init_tlp_file_config()

    # init application window
    window = Gtk.Window()
    editor_gui = ApplicationGUI(window)
    window.set_title('Tlp-UI')
    window.set_icon_name('tlpui')
    window.set_default_size(settings.user_config.window_width, settings.user_config.window_height)
    window.add(editor_gui.generate_gtk_box()) #create_main_box(window)
    window.connect('check-resize', store_window_size)
    window.connect('delete-event', close_main_window)
    window.connect('key-press-event', window_key_events_handler)
    window.show_all()
    Gtk.main()


if __name__ == '__main__':
    main()

