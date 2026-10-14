import sys
from typing import Final

from config.config_manager import ConfigManager
from domain.ports.game_rules import DifficultyNameEnum
from lib.string import safe_str_to_enum
from presentation.locales.locale_manager import LocaleManager
from presentation.screens.difficulty_select_screen import DifficultySelectScreen
from presentation.screens.locale_select_screen import LocaleSelectScreen
from presentation.screens.main_screen import MainScreen
from presentation.screens.value_input_screen import ValidationTypes, ValueInputScreen


class GamePresentation:
    def __init__(self) -> None:
        self._config_manager: Final = ConfigManager()

        self._locale_manager: Final = LocaleManager(self._config_manager)
        locale_info_list = self._locale_manager.get_locale_info_list()

        self._select_locale_screen: Final = LocaleSelectScreen(
            self._locale_manager.get_value,
            self._on_locale_selected,
            locale_info_list
        )
        self._select_difficulty_screen: Final = DifficultySelectScreen(
            self._locale_manager.get_value, self._on_difficulty_selected)
        self._main_screen: Final = MainScreen(
            self._config_manager,
            locale_info_list,
            self._on_element_select,
            # self._on_reload,
            self._locale_manager.get_value,
            self._on_change_locale_from_menu_bar,
            self._on_change_difficulty_from_menu_bar
        )
        self._selected_locale_code: str | None = None
        self._selected_difficulty_level: DifficultyNameEnum | None = None

        locale_from_config = self._config_manager.get_locale()
        difficulty_from_config = self._config_manager.get_difficulty_level()

        if locale_from_config is not None:
            self._set_locale_value(locale_from_config)

        if difficulty_from_config is not None:
            self._set_difficulty_value(difficulty_from_config)

        self._num_value_input_screen: Final = ValueInputScreen(
            self._on_element_value, self._locale_manager.get_value, "input_num_value")
        self._num_value_input_screen.set_validation_options(
            ValidationTypes.only_digits, 1, 1)

    def run(self):
        if self._selected_locale_code is None:
            self._select_locale_screen.run()
        elif self._selected_difficulty_level is None:
            self._select_difficulty_screen.run()
        else:
            self._main_screen.run(self._selected_difficulty_level)

    def _on_locale_selected(self, locale_code: str):
        self._set_locale_value(locale_code)
        self._locale_manager.sync_with_config()
        if self._selected_difficulty_level is None:
            self._show_startup_difficulty_selector()
        else:
            self._main_screen.run(self._selected_difficulty_level)

    def _on_difficulty_selected(self, difficulty: str):
        casted_diff_lvl = safe_str_to_enum(difficulty, DifficultyNameEnum)
        if not casted_diff_lvl:
            return
        self._set_difficulty_value(casted_diff_lvl)
        self._main_screen.run(casted_diff_lvl)

    def _set_locale_value(self, locale_code: str):
        self._selected_locale_code = locale_code
        self._config_manager.set_locale(self._selected_locale_code)
        self._locale_manager.sync_with_config()

    def _set_difficulty_value(self, difficulty: DifficultyNameEnum):
        self._selected_difficulty_level = difficulty
        self._config_manager.set_difficulty_level(diff_level=difficulty)

    # handle UI events

    def _on_change_locale_from_menu_bar(self, locale_code: str):
        if locale_code == self._selected_locale_code:
            return
        self._set_locale_value(locale_code)

    def _on_change_difficulty_from_menu_bar(self, difficulty: str):
        if difficulty == self._selected_difficulty_level:
            return
        casted_diff_name = safe_str_to_enum(difficulty, DifficultyNameEnum)
        if casted_diff_name:
            self._set_difficulty_value(casted_diff_name)

    def _show_startup_locale_selector(self):
        locale_code = self._select_locale_screen.run()
        if locale_code is None:
            sys.exit()
        self._set_locale_value(locale_code)

    def _show_startup_difficulty_selector(self):
        self._selected_difficulty_level = self._select_difficulty_screen.run()
        if self._selected_difficulty_level is None:
            sys.exit()
        self._config_manager.set_difficulty_level(
            self._selected_difficulty_level)

    def _on_element_select(self):
        self._num_value_input_screen.run()

    def _on_element_value(self, value: str | None):
        if value is None:
            return
        self._main_screen.on_new_value(int(value))
