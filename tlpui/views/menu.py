import importlib

from pathlib import Path
from typing import Callable
from gi.repository import Gtk
from tlpui import language, settings
from tlpui.views.dialogs import show_about_dialog
from tlpui.config_actions import save_tlp_config, quit_tlp_config
from tlpui.uihelper import get_flag_image

# TODO: generate these two things dynamically,
#  using just list of available translations,
#  so we don't have to hard-code them in source code

xml_menu_structure = """
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
lang_menu_items = [
    "/menubar/language_menu/en_EN",
    "/menubar/language_menu/de_DE",
    "/menubar/language_menu/es_ES",
    "/menubar/language_menu/fr_FR",
    "/menubar/language_menu/pt_BR",
    "/menubar/language_menu/ru_RU",
    "/menubar/language_menu/tr_TR",
    "/menubar/language_menu/id_ID",
    "/menubar/language_menu/zh_CN",
]


def switch_language(lang: str, load_tlp_config) -> None:
    """Language switcher."""
    settings.user_config.language = lang

    # reload language values
    importlib.reload(language)

    load_tlp_config(False)


def repack_language_menuitem(menuitem: Gtk.MenuItem):
    """Repack language menu items for better visibility."""
    menu_item_name = menuitem.get_name()
    lang_image = get_flag_image(menu_item_name)
    lang_label = Gtk.Label(menu_item_name.split("_")[0])
    lang_box = Gtk.Box()
    lang_box.pack_start(lang_image, False, False, 12)
    lang_box.pack_start(lang_label, False, False, 0)
    for child in menuitem.get_children(): menuitem.remove(child)
    menuitem.add(lang_box)


class MenuBar:
    window: Gtk.Window
    load_tlp_config: Callable

    def __init__(self, window: Gtk.Window, load_tlp_callback):
        self.window = window
        self.load_tlp_config = load_tlp_callback

    def create_menu_box(self) -> Gtk.Box:
        """Create application menu from XML structure."""

        ui_manager = Gtk.UIManager()
        ui_manager.add_ui_from_string(xml_menu_structure)

        action_group = Gtk.ActionGroup("actions")
        self.add_menu_actions(action_group, self.load_tlp_config)
        ui_manager.insert_action_group(action_group)

        menubar = ui_manager.get_widget("/menubar")

        for lang_item in lang_menu_items:
            repack_language_menuitem(ui_manager.get_widget(lang_item))

        menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        menu_box.pack_start(menubar, False, False, 0)

        return menu_box

    def add_menu_actions(self, action_group, load_tlp_config) -> None:
        """Add actions to application menu."""
        action_file_menu = Gtk.Action("FileMenu", language.MT_("File"), None, None)
        action_group.add_action(action_file_menu)

        action_file_menu_save = Gtk.Action("save", language.MT_('Save'), None, Gtk.STOCK_SAVE)
        action_file_menu_save.connect("activate", save_tlp_config, self.window)
        action_group.add_action(action_file_menu_save)

        action_file_menu_quit = Gtk.Action("quit", language.MT_('Quit'), None, Gtk.STOCK_QUIT)
        action_file_menu_quit.connect("activate", quit_tlp_config, self.window)
        action_group.add_action(action_file_menu_quit)

        action_language_menu = Gtk.Action("LanguageMenu", language.MT_("Language"), None, None)
        action_group.add_action(action_language_menu)

        zh_language_submenu = Gtk.Action("zhSubMenu", "zh", None, None)
        action_group.add_action(zh_language_submenu)

        action_help_menu = Gtk.Action("HelpMenu", language.MT_("Help"), None, None)
        action_group.add_action(action_help_menu)

        about_dialog_menu = Gtk.Action("AboutDialog", language.MT_("About"), None, Gtk.STOCK_INFO)
        action_group.add_action(about_dialog_menu)
        about_dialog_menu.connect('activate', show_about_dialog)

        lang_dir = Path(settings.lang_dir)
        for lang_object in lang_dir.iterdir():
            if lang_object.is_dir():
                locale = lang_object.name

                if locale == settings.user_config.language:
                    action_lang = Gtk.Action(locale, locale, None, Gtk.STOCK_APPLY)
                else:
                    action_lang = Gtk.Action(locale, locale, None, None)

                action_lang.connect("activate", lambda _, lang, wind: switch_language(lang, load_tlp_config), locale,
                                    self.window)
                action_group.add_action(action_lang)
