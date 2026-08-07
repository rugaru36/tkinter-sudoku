from tkinter import Tk
from typing import Callable

from presentation.locales.locale_manager import LocaleInfo
from presentation.screens.common.select_option_screen import Option, SelectOptionScreen


class LocaleSelectScreen(SelectOptionScreen[str]):
    def __init__(self, get_text_cb: Callable[[str], str], locale_info_list: list[LocaleInfo]) -> None:
        self._root_widget: Tk | None = None
        self._selected_locale: str | None = None
        self._locale_info_list: list[LocaleInfo] = locale_info_list
        options = [Option(locale["name"], locale["code"])
                   for locale in locale_info_list]
        super().__init__(get_text_cb, "select_locale.title", options)
