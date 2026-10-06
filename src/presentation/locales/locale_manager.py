import json
import os
from typing import Final, Literal, TypedDict, cast

from lib.file_system import read_file


class LocaleInfo(TypedDict):
    name: str
    code: str
    is_selected: bool
    is_default: bool


class LocaleManager:
    def __init__(self) -> None:
        self._locales_dir_path: Final = f"{os.getcwd()}/resources/locales"
        self._locale_info_list: list[LocaleInfo] = []

        self._selected_locale_info: LocaleInfo | None = None
        self._selected_locale: dict[str, str] = {}

        self._fallback_locale_info: LocaleInfo | None = None
        self._fallback_locale: dict[str, str] = {}

        self._load_locale_info_list()

    def get_locale_info_list(self):
        return self._locale_info_list

    def set_locale(self, code: str, selected_or_fallback: Literal["fallback", "selected"] = "selected"):
        is_locale_found = False
        for locale_info in self._locale_info_list:
            locale_info["is_selected"] = locale_info["code"] == code
            if locale_info["is_selected"]:
                loaded_locale = self._load_locale_from_file(code)
                if selected_or_fallback == "selected":
                    self._selected_locale_info = locale_info
                    self._selected_locale = loaded_locale
                elif selected_or_fallback == "fallback":
                    self._fallback_locale_info = locale_info
                    self._fallback_locale = loaded_locale
                is_locale_found = True
        if not is_locale_found and selected_or_fallback == "selected":
            self._selected_locale_info = None

    def get_value(self, key: str):
        if key in self._selected_locale:
            return self._selected_locale[key]
        if self._selected_locale_info is not None:
            print(f"text is not found by key {key} in selected locale")
        return self._fallback_locale[key] if key in self._fallback_locale else key

    def _load_locale_info_list(self):
        locales_list_file_name = "locales.list.json"
        locales_list_file_path = f"{self._locales_dir_path}/{locales_list_file_name}"
        file_content = read_file(locales_list_file_path)
        if len(file_content) == 0:
            return
        self._locale_info_list = cast(
            list[LocaleInfo], json.loads(file_content)["locales"])
        for data_as_dict in self._locale_info_list:
            if "is_default" in data_as_dict:
                self.set_locale(data_as_dict["code"], "fallback")

    def _load_locale_from_file(self, code: str):
        locale_file_name = f"locale.{code}.json"
        locale_file_path = f"{self._locales_dir_path}/{locale_file_name}"
        file_content = read_file(locale_file_path)
        return cast(dict[str, str], json.loads(file_content))
