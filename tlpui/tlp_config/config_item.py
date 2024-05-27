"""TLP config."""

from gi.repository import Gtk

from tlpui import settings
from tlpui.tlp_config.configui import ConfigObject, init_state_image, create_config_widget, get_type_image
from tlpui.tlp_config.ui_config_objects import gtktoggle
from tlpui.uihelper import EXPECTED_ITEM_MISSING_TEXT


def create_item_box(configobjects: list, doc: str, grouptitle: str, window) -> Gtk.Box:
    """Create box with config item widgets."""
    configuibox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

    if len(configobjects) > 1:
        grouplabel = Gtk.Label()
        grouplabel.set_markup(f' <b>{grouptitle.replace("_", " ")}</b> ')
        grouplabel.set_use_markup(True)
        grouplabel.set_margin_bottom(12)
        grouplabel.set_halign(Gtk.Align.START)
        grouplabel.set_valign(Gtk.Align.START)

        configuibox.pack_start(grouplabel, False, False, 0)

    for configobject in configobjects:  # type: ConfigObject
        configname = configobject.name
        stateimage = init_state_image(configname)
        tlpuiobject = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=18)
        tlpuiobject.set_margin_start(18)
        tlpuiobject.set_margin_end(18)

        if configname not in settings.tlp_config.keys():
            missingcheckbox = Gtk.CheckButton()
            missingcheckbox.set_child_visible(False)
            missingstatetogglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            missingstatetogglebox.pack_start(missingcheckbox, False, False, 0)
            missingstatetogglebox.set_halign(Gtk.Align.CENTER)
            missingstatetogglebox.set_valign(Gtk.Align.CENTER)

            missingconfiglabel = Gtk.Label(xalign=0)
            missingconfiglabel.set_name('missingConfigLabel')
            missingconfiglabel.set_markup(f' <b>{configname}</b> - <i>{EXPECTED_ITEM_MISSING_TEXT}</i> ')
            missingconfiglabel.set_use_markup(True)

            tlpuiobject.pack_start(missingstatetogglebox, False, False, 0)
            tlpuiobject.pack_start(missingconfiglabel, False, False, 0)
            configuibox.pack_start(tlpuiobject, True, True, 0)
            continue

        statetogglebox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        tlpconfigbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

        # specific config gtk object
        configwidget = create_config_widget(configname, configobject.datatype, configobject.values, window)
        configwidget.set_margin_top(6)
        configwidget.set_margin_bottom(6)
        configwidget.set_margin_left(6)

        # on/off state
        toggle = gtktoggle.create_toggle_button(configname, configwidget, window)
        statetogglebox.pack_start(toggle, False, False, 0)
        statetogglebox.set_halign(Gtk.Align.CENTER)
        statetogglebox.set_valign(Gtk.Align.CENTER)

        # object label
        configlabel = Gtk.Label(xalign=0)
        configlabel.set_markup(f' <b>{configname}</b> ')
        configlabel.set_use_markup(True)
        configlabel.set_size_request(300, 0)

        # combine boxes
        tlpconfigbox.pack_start(configlabel, False, False, 0)
        tlpconfigbox.pack_start(configwidget, True, True, 0)

        if configname.startswith('CPU_SCALING_MIN_FREQ') or configname.startswith('CPU_SCALING_MAX_FREQ'):
            khzlabel = Gtk.Label()
            khzlabel.set_markup('<small>kHz</small>')
            tlpconfigbox.pack_start(khzlabel, False, False, 12)

        if configname.endswith('_BAT'):
            tlpconfigbox.pack_start(Gtk.Image.new_from_file(f'{settings.icon_dir}OnBAT.svg'), False, False, 12)
        elif configname.endswith('_AC'):
            tlpconfigbox.pack_start(Gtk.Image.new_from_file(f'{settings.icon_dir}OnAC.svg'), False, False, 12)

        tlpuiobject.pack_start(statetogglebox, False, False, 0)
        tlpuiobject.pack_start(tlpconfigbox, False, False, 0)
        tlpuiobject.pack_start(stateimage, False, False, 0)
        tlpuiobject.pack_end(get_type_image(configname), False, False, 0)

        configuibox.pack_start(tlpuiobject, True, True, 0)

    # object description
    configdescriptionlabel = Gtk.Label()
    configdescriptionlabel.set_markup(doc)
    configdescriptionlabel.set_line_wrap(True)
    configdescriptionlabel.set_margin_top(6)
    configdescriptionlabel.set_margin_bottom(12)
    configdescriptionlabel.set_margin_start(48)
    configdescriptionlabel.set_halign(Gtk.Align.START)
    configdescriptionlabel.set_valign(Gtk.Align.START)

    # add description and horizontal separator
    configuibox.pack_start(configdescriptionlabel, True, True, 0)
    configuibox.pack_start(Gtk.HSeparator(), True, True, 0)

    return configuibox
