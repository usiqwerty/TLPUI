"""Provide runtime application settings."""

from os import path, getenv
from pathlib import Path

import tlpui.tlp_runner
from . import settings_loader

# application folder settings
work_dir = path.dirname(path.abspath(__file__))
lang_dir = f'{work_dir}/lang/'
icon_dir = f'{work_dir}/icons/'

# flatpak related params
IS_FLATPAK = Path("/.flatpak-info").exists()
FOLDER_PREFIX = "/var/run/host" if IS_FLATPAK else ""
TMP_FOLDER = f"{getenv('XDG_RUNTIME_DIR')}/app/{getenv('FLATPAK_ID')}" if IS_FLATPAK else None

# check for required commands to exist
tlpui.tlp_runner.check_binaries_exist(FOLDER_PREFIX)

user_config = settings_loader.UserConfig()

# runtime params
tlp_version = settings_loader.get_installed_tlp_version()
tlp_base_version = tlp_version.replace(".", "_")[0:3]
tlp_base_config_file = settings_loader.get_tlp_config_file("")
tlp_config_file = settings_loader.get_tlp_config_file(FOLDER_PREFIX)
tlp_config = {}
tlp_config_original = {}
tlp_config_defaults = {}
active_scroll = None
