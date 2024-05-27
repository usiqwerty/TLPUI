"""Provide CSS support for UI."""

from gi.repository import Gtk
from . import settings


def get_css_provider() -> Gtk.CssProvider:
    """Create css provider from stylesheet file and return it."""
    css_provider = Gtk.CssProvider()
    css_provider.load_from_path(f'{settings.work_dir}/styles.css')

    return css_provider
