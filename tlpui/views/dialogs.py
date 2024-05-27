import difflib

from gi.repository import Gtk, GdkPixbuf

from tlpui import settings, __version__, language
import gi
gi.require_version('Gtk', '3.0')


def changed_items_dialog(window, tmp_filename: str, dialog_title: str, message: str) -> Gtk.ResponseType:
    """Dialog to show changed TLP configuration items."""
    dialog = Gtk.Dialog(dialog_title, window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))
    dialog.set_default_size(400, 300)

    scrolled_window = Gtk.ScrolledWindow()
    scrolled_window.set_hexpand(True)
    scrolled_window.set_vexpand(True)

    with open(settings.tlp_config_file, encoding='utf-8') as fromfile:
        from_file_content = fromfile.readlines()
    with open(tmp_filename, encoding='utf-8') as tofile:
        to_file_content = tofile.readlines()
    diff = settings.tlp_base_config_file + '\n\n'
    for line in difflib.unified_diff(from_file_content, to_file_content, n=0, lineterm=''):
        if line.startswith('---') or line.startswith('+++'):
            continue
        postfix = '' if line.startswith('-') else '\n'
        diff += line + postfix

    text_buffer = Gtk.TextBuffer()
    text_buffer.set_text(diff)

    textview = Gtk.TextView()
    textview.set_buffer(text_buffer)
    textview.set_editable(False)

    scrolled_window.add(textview)
    scrolled_window.set_border_width(12)

    box = dialog.get_content_area()
    box.pack_start(scrolled_window, True, True, 0)
    box.pack_start(Gtk.Label(f'\n{message}\n'), False, False, 0)

    dialog.show_all()
    response = dialog.run()
    dialog.destroy()

    return response


def show_about_dialog(self):
    """Applications about dialog."""
    dialog = Gtk.AboutDialog()
    dialog.set_title("TLP-UI")
    dialog.set_name("name")
    dialog.set_version(__version__)
    dialog.set_comments(language.MT_("UI for TLP written in Python/Gtk"))
    dialog.set_website("https://github.com/d4nj1/TLPUI")
    dialog.set_website_label("TLP-UI @ GitHub")
    dialog.set_authors(["Daniel Christophis"])
    dialog.set_translator_credits("Muhammet Emin AKALAN (05akalan57@gmail.com)")
    dialog.set_license_type(Gtk.License.GPL_2_0)
    dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(
        f"{settings.icon_dir}themeable/hicolor/scalable/apps/tlpui.svg", width=128, height=128)
    )
    dialog.connect('response', lambda dialog, fata: dialog.destroy())
    dialog.show_all()


def show_dialog(error_message) -> None:
    """Show error dialog."""
    dialog = Gtk.MessageDialog()
    dialog.set_default_size(150, 100)
    dialog.add_button(Gtk.STOCK_OK, Gtk.ResponseType.OK)
    dialog.format_secondary_markup(error_message)
    dialog.run()
    dialog.destroy()
