from collections import OrderedDict
from typing import Any

from gi.repository import Gtk

from tlpui import language
from tlpui.config_parser.file import get_yaml_schema_object
from tlpui.tlp_config.configui import ConfigObject
from tlpui.tlp_config.config_item import create_item_box


def get_tlp_categories(window: Gtk.Window) ->  OrderedDict[Any, list[Gtk.Label | Gtk.Box]] :
    """Get categories from TLP schema."""
    property_objects = OrderedDict()

    categories = get_yaml_schema_object('categories')
    for category in categories:
        category_name = category['name']

        # Create category label
        category_label = Gtk.Label(language.CDT_(f"{category_name}__CATEGORY_TITLE"))
        category_label.set_alignment(1, 0.5)
        category_label.set_margin_top(6)
        category_label.set_margin_bottom(6)
        category_label.set_margin_left(6)
        category_label.set_margin_right(6)

        # Create category box
        category_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        configs = category['configs']
        for config in configs:
            group_title = ""
            config_objects = []

            if 'group' in config:
                group_title = config['group']
                trans_description = f"{group_title}__GROUP_DESCRIPTION"
                group_items = config['ids']
                for group_item in group_items:
                    config_objects.append(ConfigObject(group_item['id'], group_item['type'], group_item['values']))
            else:
                item_id = config['id']
                trans_description = f"{item_id}__ID_DESCRIPTION"
                config_objects.append(ConfigObject(item_id, config['type'], config['values']))

            config_box = create_item_box(config_objects, language.CDT_(trans_description), group_title, window)
            config_box.set_margin_start(12)
            config_box.set_margin_end(12)
            config_box.set_margin_top(12)
            category_box.pack_start(config_box, False, False, 0)

        property_objects[category_name] = [category_label, category_box]

    return property_objects
