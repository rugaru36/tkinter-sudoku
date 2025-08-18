import sys
from typing import Final

from config.config_manager import Config_Manager
from presentation.screens.difficulty_select_screen import Difficulty_Select_Screen
from presentation.screens.main_screen import Main_Screen
from presentation.screens.value_input_screen import Validation_Types, Value_Input_Screen


class Game_Presentation:
    def __init__(self) -> None:
        self._difficulty_select_screen: Final = Difficulty_Select_Screen()
        self._main_screen: Final = Main_Screen(
            self._on_element_select, self.reload)
        self._config_manager: Final = Config_Manager()

        self._selected_difficulty: str | None = self._config_manager.get_difficulty_level()

        self._num_value_input_screen: Final = Value_Input_Screen(
            self._on_element_value).set_validation_options(Validation_Types.only_digits, 1, 1)
        # self._player_name_input_screen: Final = Value_Input_Screen(
        # self._on_player_name)

    def reload(self):
        self._selected_difficulty = None
        self.run()

    def run(self):
        if self._selected_difficulty is None:
            self._select_difficulty()
        self._run_main_screen()

    def _select_difficulty(self):
        self._selected_difficulty = self._difficulty_select_screen.run()
        if self._selected_difficulty is None:
            sys.exit()
        self._config_manager.set_difficulty_level(self._selected_difficulty)

    def _run_main_screen(self):
        if self._selected_difficulty is None:
            raise ValueError("_difficulty_level is None")
        self._main_screen.run(self._selected_difficulty)

    def _on_element_select(self):
        self._num_value_input_screen.run("Input new value", "Input value")

    def _on_element_value(self, value: str | None):
        if value is None:
            return
        self._main_screen.on_new_value(int(value))
        # if not self._main_screen.get_is_in_progress():
        #     self._player_name_input_screen.run("Input your name", "Name")

    # def _on_player_name(self, value: str | None):
    #     # if value is None:
    #     # return
    #     pass
