"""This module provides helper functions for application settings."""

import configparser
import re
from os import getenv
from pathlib import Path

from tlpui.tlp_runner import exec_command


def get_tlp_config_file(prefix: str) -> str:
    """Select tlp config file by prefix."""
    return f"{prefix}/etc/tlp.conf"


def get_installed_tlp_version() -> str:
    """Fetch tlp version from command."""
    pattern = re.compile(r"TLP ([^\s]+)")
    current_config = exec_command(["tlp-stat", "-c"])
    matcher = pattern.search(current_config)
    return matcher.group(1)


def get_user_config_file() -> Path:
    """Get config path for executing user."""
    user_config_home = getenv("XDG_CONFIG_HOME", "")
    if user_config_home == "":
        user_config_path = Path(str(Path.home()) + "/.config/tlpui")
    else:
        user_config_path = Path(str(user_config_home) + "/tlpui")
    return Path(str(user_config_path) + "/tlpui.cfg")


class UserConfig:
    """Class to handle ui config parameters."""

    def __init__(self):
        """Init user config class parameters."""
        self.language = "en_EN"
        self.active_page = 0
        self.active_category = 0
        self.active_position = 0
        self.window_width = 900
        self.window_height = 600
        self.user_config_file = get_user_config_file()
        self.read_user_config()

    def read_user_config(self):
        """Read ui config parameters from user home."""
        if self.user_config_file.exists():
            config = configparser.ConfigParser()
            with open(str(self.user_config_file), encoding='utf-8') as configfile:
                config.read_file(configfile)
            try:
                self.language = config['default']['language']
                self.active_page = int(config['default']['activeoption'])
                self.active_category = int(config['default']['activecategory'])
                self.active_position = float(config['default']['activeposition'])
                self.window_width = int(config['default']['windowxsize'])
                self.window_height = int(config['default']['windowysize'])
            except KeyError:
                # Config key error, override with default values
                self.write_user_config()
        else:
            self.user_config_file.parent.mkdir(parents=True, exist_ok=True)
            self.write_user_config()

    def write_user_config(self):
        """Persist ui config parameters to user home."""
        config = configparser.ConfigParser()
        config['default'] = {}
        config['default']['language'] = self.language
        config['default']['activeoption'] = str(self.active_page)
        config['default']['activecategory'] = str(self.active_category)
        config['default']['activeposition'] = str(self.active_position)
        config['default']['windowxsize'] = str(self.window_width)
        config['default']['windowysize'] = str(self.window_height)
        with open(str(self.user_config_file), mode='w', encoding='utf-8') as configfile:
            config.write(configfile)
