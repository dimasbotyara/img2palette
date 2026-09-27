"""
img2palette - Locale Manager
Author: dimasbotyara
"""

from locales import STRINGS
from config import load_config, save_config


class LocaleManager:
    """Менеджер локализации."""

    def __init__(self):
        self._config = load_config()
        self._lang = self._config.get("language", None)

    @property
    def language(self) -> str | None:
        return self._lang

    @language.setter
    def language(self, lang: str):
        self._lang = lang
        self._config["language"] = lang
        self._config["first_run"] = False
        save_config(self._config)

    @property
    def is_first_run(self) -> bool:
        return self._config.get("first_run", True)

    def get(self, key: str, *args) -> str:
        """
        Получить локализованную строку.
        Поддерживает форматирование: locale.get("key", value1, value2)
        """
        if key not in STRINGS:
            return f"[MISSING: {key}]"

        lang = self._lang or "en"
        text = STRINGS[key].get(lang, STRINGS[key].get("en", f"[NO LANG: {key}]"))

        if args:
            try:
                text = text.format(*args)
            except (IndexError, KeyError):
                pass

        return text


# Глобальный экземпляр
locale = LocaleManager()