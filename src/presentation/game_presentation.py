import sys
from typing import Final

from presentation.screens.difficulty_select_screen import Difficulty_Select_Screen
from presentation.screens.main_screen import Main_Screen
from presentation.screens.value_input_screen import Value_Input_Screen


class Game_Presentation:
    def __init__(self) -> None:
        self._difficulty_select_screen: Final = Difficulty_Select_Screen()
        self._main_screen: Final = Main_Screen(
            self._on_element_select, self.run)
        self._input_screen: Final = Value_Input_Screen()

        self._selected_difficulty_level: str | None = None
        pass

    def run(self):
        self._select_difficulty()
        self._run_main_screen()

    def _select_difficulty(self):
        self._selected_difficulty_level = self._difficulty_select_screen.run()
        if self._selected_difficulty_level is None:
            sys.exit()

    def _run_main_screen(self):
        if self._selected_difficulty_level is None:
            raise ValueError("_difficulty_level is None")
        self._main_screen.run(self._selected_difficulty_level)

    def _on_element_select(self):
        self._input_screen.run(self._on_new_value)

    def _on_new_value(self, value: int | None):
        if value is None:
            return
        self._main_screen.on_new_value(value)
