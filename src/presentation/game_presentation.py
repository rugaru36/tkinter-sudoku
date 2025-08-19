import sys
from typing import Final

from config.config_manager import Config_Manager
from presentation.locales.locale_manager import Locale_Manager
from presentation.screens.difficulty_select_screen import Difficulty_Select_Screen
from presentation.screens.locale_select_screen import Locale_Select_Screen
from presentation.screens.main_screen import Main_Screen
from presentation.screens.value_input_screen import Validation_Types, Value_Input_Screen


class Game_Presentation:
    def __init__(self) -> None:
        self._locale_manager: Final = Locale_Manager()
        locale_info_list = self._locale_manager.get_locale_info_list()

        self._select_locale_screen: Final = Locale_Select_Screen(
            locale_info_list)
        self._difficulty_select_screen: Final = Difficulty_Select_Screen(
            self._locale_manager.get_value)
        self._main_screen: Final = Main_Screen(
            locale_info_list,
            self._on_element_select,
            self._on_reload,
            self._locale_manager.get_value,
            self._on_change_locale,
            self._on_change_difficulty
        )
        self._config_manager: Final = Config_Manager()

        self._selected_difficulty_level: str | None = self._config_manager.get_difficulty_level()
        self._selected_locale_code: str | None = self._config_manager.get_locale()

        self._num_value_input_screen: Final = Value_Input_Screen(
            self._on_element_value, self._locale_manager.get_value, "input_num_value")
        self._num_value_input_screen.set_validation_options(
            Validation_Types.only_digits, 1, 1)

    def run(self):
        if self._selected_locale_code is None:
            self._select_locale()
        else:
            self._locale_manager.set_locale(self._selected_locale_code)
        if self._selected_difficulty_level is None:
            self._select_difficulty()
        self._run_main_screen()

    def _on_reload(self):
        self.run()

    def _on_change_locale(self, locale_code: str):
        pass

    def _on_change_difficulty(self, difficulty: str):
        self._selected_difficulty_level = difficulty
        self.run()

    def _select_locale(self):
        self._selected_locale_code = self._select_locale_screen.run()
        if self._selected_locale_code is None:
            sys.exit()
        self._locale_manager.set_locale(self._selected_locale_code)
        self._config_manager.set_locale(self._selected_locale_code)

    def _select_difficulty(self):
        self._selected_difficulty_level = self._difficulty_select_screen.run()
        if self._selected_difficulty_level is None:
            sys.exit()
        self._config_manager.set_difficulty_level(
            self._selected_difficulty_level)

    def _run_main_screen(self):
        if self._selected_difficulty_level is None:
            raise ValueError("_difficulty_level is None")
        self._main_screen.run(self._selected_difficulty_level)

    def _on_element_select(self):
        self._num_value_input_screen.run()

    def _on_element_value(self, value: str | None):
        if value is None:
            return
        self._main_screen.on_new_value(int(value))
