import subprocess
import sys
from pathlib import Path
from shutil import which
from subprocess import check_output, CalledProcessError

# TODO: maybe it would be better to
#  import tlpui.views.dialogs (or just show_dialog())
#  but it turns out into circular import
import tlpui.views


def exec_command(commands: [str]):
    """Execute commands locally."""
    try:
        return check_output(commands, stderr=subprocess.STDOUT,).decode(sys.stdout.encoding)
    except CalledProcessError as error:
        tlpui.views.dialogs.show_dialog(error)


def check_binaries_exist(flatpak_folder_prefix: str) -> None:
    """Check if required binaries are installed on system."""
    for expected_command in ["tlp", "tlp-stat", "lspci", "lsusb"]:
        if flatpak_folder_prefix != "":
            command_exists = Path(f"{flatpak_folder_prefix}/usr/bin/{expected_command}").exists()
            if not command_exists:
                command_exists = Path(f"{flatpak_folder_prefix}/usr/sbin/{expected_command}").exists()
        else:
            command_exists = which(expected_command) is not None
            if not command_exists:
                command_exists = Path(f"/usr/sbin/{expected_command}").exists()

        if not command_exists:
            tlpui.views.dialogs.show_dialog(f"{expected_command} not found on system. Please install first.")
            sys.exit(1)
