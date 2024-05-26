import difflib

from gi.repository import Gtk, GdkPixbuf

from tlpui import settings, __version__, language


def changed_items_dialog(window, tmpfilename: str, dialogtitle: str, message: str) -> Gtk.ResponseType:
    """Dialog to show changed TLP configuration items."""
    dialog = Gtk.Dialog(dialogtitle, window, 0, (
        Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OK, Gtk.ResponseType.OK
    ))
    dialog.set_default_size(400, 300)

    scrolledwindow = Gtk.ScrolledWindow()
    scrolledwindow.set_hexpand(True)
    scrolledwindow.set_vexpand(True)

    with open(settings.tlpconfigfile, encoding='utf-8') as fromfile:
        fromfilecontent = fromfile.readlines()
    with open(tmpfilename, encoding='utf-8') as tofile:
        tofilecontent = tofile.readlines()
    diff = settings.tlpbaseconfigfile + '\n\n'
    for line in difflib.unified_diff(fromfilecontent, tofilecontent, n=0, lineterm=''):
        if line.startswith('---') or line.startswith('+++'):
            continue
        postfix = '' if line.startswith('-') else '\n'
        diff += line + postfix

    textbuffer = Gtk.TextBuffer()
    textbuffer.set_text(diff)

    textview = Gtk.TextView()
    textview.set_buffer(textbuffer)
    textview.set_editable(False)

    scrolledwindow.add(textview)
    scrolledwindow.set_border_width(12)

    box = dialog.get_content_area()
    box.pack_start(scrolledwindow, True, True, 0)
    box.pack_start(Gtk.Label(f'\n{message}\n'), False, False, 0)

    dialog.show_all()
    response = dialog.run()
    dialog.destroy()

    return response


def show_about_dialog(self):
    """Applications about dialog."""
    aboutdialog = Gtk.AboutDialog()
    aboutdialog.set_title("TLP-UI")
    aboutdialog.set_name("name")
    aboutdialog.set_version(__version__)
    aboutdialog.set_comments(language.MT_("UI for TLP written in Python/Gtk"))
    aboutdialog.set_website("https://github.com/d4nj1/TLPUI")
    aboutdialog.set_website_label("TLP-UI @ GitHub")
    aboutdialog.set_authors(["Daniel Christophis"])
    aboutdialog.set_translator_credits("Muhammet Emin AKALAN (05akalan57@gmail.com)")
    aboutdialog.set_license_type(Gtk.License.GPL_2_0)
    aboutdialog.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(
        f"{settings.icondir}themeable/hicolor/scalable/apps/tlpui.svg", width=128, height=128)
    )
    aboutdialog.connect('response', lambda dialog, fata: dialog.destroy())
    aboutdialog.show_all()
