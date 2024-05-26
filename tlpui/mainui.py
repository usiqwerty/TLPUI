"""Provide main window parts for TLPUI."""

from gi.repository import Gdk

from .actions import save_tlp_config, quit_tlp_config


def window_key_events(self, event) -> None:
    """Add window key events like crtl+(q|w|s)."""
    if event.state & Gdk.ModifierType.CONTROL_MASK:
        # close window with ctrl+q or ctrl+w
        if event.keyval in (113, 119):
            quit_tlp_config(None, self)
        # save config with ctrl+s
        if event.keyval == 115:
            save_tlp_config(None, self)


def close_main_window(self, _) -> bool:
    """Close main window."""
    quit_tlp_config(None, self)

    # When delete-event is cancelled we have to return True
    # Otherwise application window will disappear
    return True
