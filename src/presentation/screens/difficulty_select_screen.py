from typing import Callable

from domain.ports.difficulty import Difficulty
from presentation.screens.common.select_option_screen import Option, SelectOptionScreen


class DifficultySelectScreen(SelectOptionScreen[str]):
    def __init__(self, get_text_cb: Callable[[str], str]) -> None:
        super().__init__(get_text_cb, "select_diff.title", [
            Option("select_diff.easy", Difficulty.easy),
            Option("select_diff.mid", Difficulty.mid),
            Option("select_diff.hard", Difficulty.hard)
        ])
