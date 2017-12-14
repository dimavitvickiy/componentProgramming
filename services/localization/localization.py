from config import UKRAINIAN_LANGUAGE, RUSSIAN_LANGUAGE, get_language
from services.localization.languages.russian import RUSSIAN
from services.localization.languages.ukrainian import UKRAINIAN


def translate_(s):
    if get_language() == UKRAINIAN_LANGUAGE:
        return UKRAINIAN[s]
    if get_language() == RUSSIAN_LANGUAGE:
        return RUSSIAN[s]
