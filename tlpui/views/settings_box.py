from gi.repository import Gtk

from tlpui import settings, language
from tlpui.config_actions import save_tlp_config, run_tlp
# from tlpui.views.main_box import load_tlp_config
from tlpui.uihelper import get_theme_image


def create_settings_box(window, load_tlp_config) -> Gtk.Box:
    """Buttons for direct access in UI."""
    # TODO: generate buttons dynamically
    #  instead of hardcoding them

    file_entry_label = Gtk.Label(f"TLP {settings.tlp_version} - {settings.tlp_base_config_file}")
    file_entry_label.set_alignment(0, 0.5)

    reload_button = Gtk.Button(label=' ' + language.MT_('Reload'),
                              image=get_theme_image('view-refresh-symbolic', Gtk.IconSize.BUTTON))
    reload_button.connect('clicked', load_tlp_config, window, True)
    reload_button.set_always_show_image(True)

    save_button = Gtk.Button(label=' ' + language.MT_('Save'),
                            image=get_theme_image('document-save-symbolic', Gtk.IconSize.BUTTON))
    save_button.connect('clicked', save_tlp_config, window)
    save_button.set_always_show_image(True)

    start_button = Gtk.Button(label=' ' + language.MT_('Start'),
                            image=get_theme_image('start-symbolic', Gtk.IconSize.BUTTON))
    start_button.connect('clicked', run_tlp, window)
    start_button.set_always_show_image(True)

    settings_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    settings_box.pack_start(file_entry_label, True, True, 0)
    settings_box.pack_start(reload_button, False, False, 0)
    settings_box.pack_start(save_button, False, False, 0)
    settings_box.pack_start(start_button, False, False, 0)

    return settings_box
