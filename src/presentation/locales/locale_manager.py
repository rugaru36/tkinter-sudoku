import json
import os
from typing import Final, Literal, TypedDict, cast

from config.config_manager import ConfigManager
from lib.file_system import read_file


class LocaleInfo(TypedDict):
    name: str
    code: str
    is_default: bool


class LocaleManager:
    def __init__(self, config_manager: ConfigManager) -> None:
        self._locales_dir_path: Final = f"{os.getcwd()}/resources/locales"
        self._locale_info_list: list[LocaleInfo] = []

        self._selected_locale_info: LocaleInfo | None = None
        self._selected_locale: dict[str, str] = {}

        self._fallback_locale_info: LocaleInfo | None = None
        self._fallback_locale: dict[str, str] = {}

        self._load_locale_info_list()
        self._config: Final = config_manager

    def get_locale_info_list(self):
        return self._locale_info_list

    def get_is_locale_selected(self):
        return self._selected_locale_info is not None

    def sync_with_config(self):
        code_from_config = self._config.get_locale()
        if code_from_config:
            self._set_locale(code_from_config)
        else:
            self._selected_locale = {}
            self._selected_locale_info = None
    
    def get_value(self, key: str):
        if key in self._selected_locale:
            return self._selected_locale[key]
        if self._selected_locale_info:
            print(f"text is not found by key {key} in selected locale")
        return self._fallback_locale[key] if key in self._fallback_locale else key

    def _get_locale_info_by_code(self, code: str):
        for locale_info in self._locale_info_list:
            if locale_info["code"] == code:
                return locale_info
        return None

    def _set_locale(self, code: str, selected_or_fallback: Literal["fallback", "selected"] = "selected"):
        loaded_locale = self._load_locale_from_file(code)
        if selected_or_fallback == "selected":
            self._selected_locale_info = self._get_locale_info_by_code(code)
            self._selected_locale = loaded_locale
        elif selected_or_fallback == "fallback":
            self._fallback_locale_info = self._get_locale_info_by_code(code)
            self._fallback_locale = loaded_locale

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
                self._set_locale(data_as_dict["code"], "fallback")

    def _load_locale_from_file(self, code: str):
        locale_file_name = f"locale.{code}.json"
        locale_file_path = f"{self._locales_dir_path}/{locale_file_name}"
        file_content = read_file(locale_file_path)
        return cast(dict[str, str], json.loads(file_content))
