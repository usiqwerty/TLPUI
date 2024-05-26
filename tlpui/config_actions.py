from gi.repository import Gtk

from tlpui import settings, language
from tlpui.config_parser.file import get_changed_properties, create_tmp_tlp_config_file, write_tlp_config
from tlpui.tlp_runner import exec_command
from tlpui.uihelper import get_graphical_sudo
from tlpui.views.dialogs import changed_items_dialog, show_dialog


def save_tlp_config(self, window) -> None:
    """Persist TLP configuration changes."""
    changedproperties = get_changed_properties()
    if len(changedproperties) == 0:
        return

    tmpfilename = create_tmp_tlp_config_file(changedproperties)

    saveresponse = changed_items_dialog(
        window,
        tmpfilename,
        language.MT_('Review settings'),
        language.MT_('Save these changes?'))

    if saveresponse == Gtk.ResponseType.OK:
        write_tlp_config(tmpfilename)

        #TODO: why?
        ## reload config after file save
        #load_tlp_config(self, window, True)


def quit_tlp_config(_, window) -> None:
    """Quit TLPUI and prompt for unsaved changes."""
    settings.userconfig.write_user_config()

    changedproperties = get_changed_properties()
    if len(changedproperties) == 0:
        Gtk.main_quit()
        return

    tmpfilename = create_tmp_tlp_config_file(changedproperties)

    quitresponse = changed_items_dialog(
        window,
        tmpfilename,
        language.MT_('Unsaved settings'),
        language.MT_('Do you really want to quit? No changes will be saved'))

    if quitresponse == Gtk.ResponseType.OK:
        Gtk.main_quit()


def run_tlp(self, window) -> None:
    """Run TLP service."""
    changedproperties = get_changed_properties()
    if len(changedproperties) != 0:
        save_tlp_config(self, window)
    sudo_cmd=get_graphical_sudo()
    output = exec_command([sudo_cmd, "tlp", "start"])
    if output:
        show_dialog(output)
