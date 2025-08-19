import json
import os
from typing import Final

from lib.file_system import read_file


class Locale_Info:
    def __init__(self, dict: dict[str, str] | None = None):
        self.name: str = "[locale_name]"
        self.code: str = "[locale_code]"
        if dict is not None:
            self.update_from_dict(dict)

    def update_from_dict(self, dict: dict[str, str]):
        self.__dict__.update(dict)


class Locale_Manager:
    def __init__(self) -> None:
        self._locales_dir_path: Final = f"{os.getcwd()}/resources/locales"
        self._locale_info_list: list[Locale_Info] = []
        self._load_locale_info_list()

        self._selected_locale_info: Locale_Info | None = None
        self._selected_locale: dict[str, str] = {}

    def get_locale_info_list(self):
        return self._locale_info_list

    def set_locale(self, code: str):
        for locale_info in self._locale_info_list:
            if locale_info.code == code:
                self._selected_locale_info = locale_info
                self._load_locale_file()
                return
        self._selected_locale_info = None

    def get_value(self, key: str):
        if key in self._selected_locale:
            return self._selected_locale[key]
        print(f"locale text value is not found by key {key}")
        return key

    def _load_locale_info_list(self):
        locales_list_file_name = "locales.list.json"
        locales_list_file_path = f"{self._locales_dir_path}/{locales_list_file_name}"
        file_content = read_file(locales_list_file_path)
        if len(file_content) == 0:
            return
        parsed_json: dict[str, list[dict[str, str]]] = json.loads(file_content)  # pyright: ignore[reportAny]
        data_as_dict_list: list[dict[str, str]] = parsed_json["locales"]
        for data_as_dict in data_as_dict_list:
            self._locale_info_list.append(Locale_Info(data_as_dict))
    
    def _load_locale_file(self):
        if self._selected_locale_info is None:
            self._selected_locale = {}
            return
        locale_file_name = f"locale.{self._selected_locale_info.code}.json"
        locale_file_path = f"{self._locales_dir_path}/{locale_file_name}"
        file_content = read_file(locale_file_path)
        self._selected_locale = json.loads(file_content)

