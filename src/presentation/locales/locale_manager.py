import json
import os
from typing import Final, TypedDict, cast

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
        self._default_locale: str | None = None
        self._selected_locale_info: LocaleInfo | None = None
        self._selected_locale: dict[str, str] = {}
        self._load_locale_info_list()

    def get_locale_info_list(self):
        return self._locale_info_list

    def set_locale(self, code: str):
        is_locale_found = False
        for locale_info in self._locale_info_list:
            locale_info["is_selected"] = locale_info["code"] == code
            if locale_info["is_selected"]:
                self._selected_locale_info = locale_info
                self._load_locale_file()
                is_locale_found = True
        if not is_locale_found:
            self._selected_locale_info = None

    def get_value(self, key: str):
        if key in self._selected_locale:
            return self._selected_locale[key]
        if self._selected_locale_info is not None:
            print(f"locale text value is not found by key {key}")
        return key

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
                self.set_locale(data_as_dict["code"])

    def _load_locale_file(self):
        if self._selected_locale_info is None:
            self._selected_locale = {}
            return
        locale_file_name = f"locale.{self._selected_locale_info["code"]}.json"
        locale_file_path = f"{self._locales_dir_path}/{locale_file_name}"
        file_content = read_file(locale_file_path)
        self._selected_locale = cast(dict[str, str], json.loads(file_content))
