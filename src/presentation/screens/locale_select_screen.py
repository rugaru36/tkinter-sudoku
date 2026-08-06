from tkinter import Tk
from typing import Callable

from presentation.locales.locale_manager import Locale_Info
from presentation.screens.common.select_option_screen import Option, Select_Option_Screen


class Locale_Select_Screen(Select_Option_Screen[str]):
    def __init__(self, get_text_cb: Callable[[str], str], locale_info_list: list[Locale_Info]) -> None:
        self._root_widget: Tk | None = None
        self._selected_locale: str | None = None
        self._locale_info_list: list[Locale_Info] = locale_info_list
        options = [Option(locale["name"], locale["code"])
                   for locale in locale_info_list]
        super().__init__(get_text_cb, "select_locale.title", options)
