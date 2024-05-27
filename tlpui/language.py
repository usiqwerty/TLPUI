"""Provide translation."""

from . import settings
import gettext


def load_lang(lang_file):
    """Load language from file."""
    translation = gettext.translation(lang_file, settings.lang_dir, [settings.user_config.language])

    version_lang_file = f"{lang_file}{settings.tlp_base_version}"
    if gettext.find(version_lang_file, settings.lang_dir, [settings.user_config.language]) is None:
        return translation.gettext

    version_translation = gettext.translation(version_lang_file, settings.lang_dir, [settings.user_config.language])
    version_translation.add_fallback(translation)
    return version_translation.gettext


CDT_ = load_lang('configdescriptions')
MT_ = load_lang('mainui')
ST_ = load_lang('statui')
UH_ = load_lang('uihelper')
