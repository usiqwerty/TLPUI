from gi.repository import Gtk

from tlpui import settings, language
from tlpui.actions import save_tlp_config, run_tlp
# from tlpui.views.main_box import load_tlp_config
from tlpui.uihelper import get_theme_image


def create_settings_box(window, load_tlp_config) -> Gtk.Box:
    """Buttons for direct access in UI."""
    fileentrylabel = Gtk.Label(f"TLP {settings.tlpversion} - {settings.tlpbaseconfigfile}")
    fileentrylabel.set_alignment(0, 0.5)

    reloadbutton = Gtk.Button(label=' ' + language.MT_('Reload'),
                              image=get_theme_image('view-refresh-symbolic', Gtk.IconSize.BUTTON))
    reloadbutton.connect('clicked', load_tlp_config, window, True)
    reloadbutton.set_always_show_image(True)

    savebutton = Gtk.Button(label=' ' + language.MT_('Save'),
                            image=get_theme_image('document-save-symbolic', Gtk.IconSize.BUTTON))
    savebutton.connect('clicked', save_tlp_config, window)
    savebutton.set_always_show_image(True)

    startbutton = Gtk.Button(label=' ' + language.MT_('Start'),
                            image=get_theme_image('start-symbolic', Gtk.IconSize.BUTTON))
    startbutton.connect('clicked', run_tlp, window)
    startbutton.set_always_show_image(True)

    settingsbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
    settingsbox.pack_start(fileentrylabel, True, True, 0)
    settingsbox.pack_start(reloadbutton, False, False, 0)
    settingsbox.pack_start(savebutton, False, False, 0)
    settingsbox.pack_start(startbutton, False, False, 0)

    return settingsbox
