import json
import os
from typing import Final, cast
from lib.file_system import ensure_file, read_file, write_file


class ConfigData:
    def __init__(self) -> None:
        self.difficulty_level: str | None = None
        self.locale: str | None = None

    def update_from_dict(self, data: dict[str, str]):
        self.__dict__.update(data)


class ConfigManager:
    def __init__(self) -> None:
        config_file_name = "config.json"
        self._config_file_path: Final = f"{os.getcwd()}/{config_file_name}"

        ensure_file(self._config_file_path, "{}")

        self._config: Final = ConfigData()
        self._load_config_file()

    def get_difficulty_level(self) -> str | None:
        return self._config.difficulty_level

    def get_locale(self):
        return self._config.locale

    def set_difficulty_level(self, diff_level: str):
        self._config.difficulty_level = diff_level
        self._write_config_file()

    def set_locale(self, locale_code: str):
        self._config.locale = locale_code
        self._write_config_file()

    def _load_config_file(self):
        content = read_file(self._config_file_path)
        data = cast(dict[str, str], json.loads(content))
        self._config.update_from_dict(data)

    def _write_config_file(self):
        json_str_content = json.dumps(self._config.__dict__)
        write_file(self._config_file_path, json_str_content)
