import sys
from typing import Final

from presentation.screens.difficulty_selector import Difficulty_Selector
from presentation.screens.main_screen import Main_Screen
from presentation.screens.value_input import Value_Input


class Game_Presentation:
    def __init__(self) -> None:
        self._difficulty_selector: Final = Difficulty_Selector()
        self._main_screen: Final = Main_Screen(
            self._on_element_select, self.run)
        self._input_screen: Final = Value_Input()

        self._selected_difficulty_level: str | None = None
        pass

    def reload(self):
        self._select_difficulty()

    def run(self):
        self._select_difficulty()
        self._run_main_screen()

    def _select_difficulty(self):
        self._selected_difficulty_level = self._difficulty_selector.select()
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
