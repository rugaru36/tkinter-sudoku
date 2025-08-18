import json
import os
from types import SimpleNamespace
from typing import Final
from lib.file_system import ensure_file, read_file, write_file


class Config_Data:
    def __init__(self) -> None:
        self.difficulty_level: str | None = None


class Config_Manager:
    def __init__(self) -> None:
        config_file_name = "config.json"
        self._config_file_path: Final = f"{os.getcwd()}/{config_file_name}"

        ensure_file(self._config_file_path, "{}")

        self._config_data: Config_Data | None = None
        self._load_config_file()

    def get_difficulty_level(self) -> str | None:
        if self._config_data is None:
            return None
        return self._config_data.difficulty_level

    def set_difficulty_level(self, diff_level: str):
        if self._config_data is None:
            self._config_data = Config_Data()
        self._config_data.difficulty_level = diff_level

    def _load_config_file(self):
        file_content = read_file(self._config_file_path)
        self._config_data = json.loads(
            file_content, object_hook=lambda d: SimpleNamespace(**d))

    def _write_config_file(self):
        json_str_content = json.dumps(self._config_data.__dict__)
        write_file(self._config_file_path, json_str_content)
