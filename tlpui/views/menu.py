import importlib
from pathlib import Path

from gi.repository import Gtk

from tlpui import language, settings
from tlpui.views.dialogs import show_about_dialog
from tlpui.actions import save_tlp_config, quit_tlp_config

from tlpui.uihelper import get_flag_image
# from tlpui.views.main_box import load_tlp_config


def repack_language_menuitem(menuitem: Gtk.MenuItem):
    """Repack language menu items for better visibility."""
    menuitemname = menuitem.get_name()
    langimage = get_flag_image(menuitemname)
    langlabel = Gtk.Label(menuitemname.split("_")[0])
    langbox = Gtk.Box()
    langbox.pack_start(langimage, False, False, 12)
    langbox.pack_start(langlabel, False, False, 0)
    [menuitem.remove(child) for child in menuitem.get_children()]
    menuitem.add(langbox)


def add_menu_actions(window, actiongroup, load_tlp_config) -> None:
    """Add actions to application menu."""
    actionfilemenu = Gtk.Action("FileMenu", language.MT_("File"), None, None)
    actiongroup.add_action(actionfilemenu)
    actionfilemenusave = Gtk.Action("save", language.MT_('Save'), None, Gtk.STOCK_SAVE)
    actionfilemenusave.connect("activate", save_tlp_config, window)
    actiongroup.add_action(actionfilemenusave)
    actionfilemenuquit = Gtk.Action("quit", language.MT_('Quit'), None, Gtk.STOCK_QUIT)
    actionfilemenuquit.connect("activate", quit_tlp_config, window)
    actiongroup.add_action(actionfilemenuquit)

    actionlanguagemenu = Gtk.Action("LanguageMenu", language.MT_("Language"), None, None)
    actiongroup.add_action(actionlanguagemenu)

    zhlanguagesubmenu = Gtk.Action("zhSubMenu", "zh", None, None)
    actiongroup.add_action(zhlanguagesubmenu)

    actionhelpmenu = Gtk.Action("HelpMenu", language.MT_("Help"), None, None)
    actiongroup.add_action(actionhelpmenu)

    aboutdialogmenu = Gtk.Action("AboutDialog", language.MT_("About"), None, Gtk.STOCK_INFO)
    actiongroup.add_action(aboutdialogmenu)
    aboutdialogmenu.connect('activate', show_about_dialog)

    langdir = Path(settings.langdir)
    for langobject in langdir.iterdir():
        if langobject.is_dir():
            locale = langobject.name

            if locale == settings.userconfig.language:
                actionlang = Gtk.Action(locale, locale, None, Gtk.STOCK_APPLY)
            else:
                actionlang = Gtk.Action(locale, locale, None, None)

            actionlang.connect("activate", lambda x:switch_language(*x, load_tlp_config), locale, window)
            actiongroup.add_action(actionlang)


def create_menu_box(window, load_tlp_config) -> Gtk.Box:
    """Create application menu from XML structure."""
    xmlmenustructure = """
    <ui>
        <menubar name='menubar'>
            <menu action='FileMenu'>
                <menuitem action='save' />
                <menuitem action='quit' />
            </menu>
            <menu name="language_menu" action='LanguageMenu'>
                <menuitem name="en_EN" action='en_EN' />
                <menuitem name="de_DE" action='de_DE' />
                <menuitem name="es_ES" action='es_ES' />
                <menuitem name="fr_FR" action='fr_FR' />
                <menuitem name="pt_BR" action='pt_BR' />
                <menuitem name="ru_RU" action='ru_RU' />
                <menuitem name="tr_TR" action='tr_TR' />
                <menuitem name="id_ID" action='id_ID' />
                <menu name="zh_CN" action='zhSubMenu'>
                    <menuitem name="zh_CN" action='zh_CN' />
                    <menuitem name="zh_TW" action='zh_TW' />
                </menu>
            </menu>
            <menu name="help_menu" action='HelpMenu'>
                <menuitem name="about_dialog" action='AboutDialog' />
            </menu>
        </menubar>
    </ui>
    """

    uimanager = Gtk.UIManager()
    uimanager.add_ui_from_string(xmlmenustructure)

    actiongroup = Gtk.ActionGroup("actions")
    add_menu_actions(window, actiongroup, load_tlp_config)
    uimanager.insert_action_group(actiongroup)

    menubar = uimanager.get_widget("/menubar")

    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/en_EN"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/de_DE"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/es_ES"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/fr_FR"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/pt_BR"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/ru_RU"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/tr_TR"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/id_ID"))
    repack_language_menuitem(uimanager.get_widget("/menubar/language_menu/zh_CN"))

    menubox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    menubox.pack_start(menubar, False, False, 0)

    return menubox


def switch_language(self, lang: str, window: Gtk.Window, load_tlp_config) -> None:
    """Language switcher."""
    settings.userconfig.language = lang

    # reload language values
    importlib.reload(language)

    load_tlp_config(self, window, False)
