from typing import Callable

from domain.ports.difficulty import Difficulty
from presentation.screens.common.select_option_screen import Option, SelectOptionScreen


class DifficultySelectScreen(SelectOptionScreen[str]):
    def __init__(self, get_text_cb: Callable[[str], str]) -> None:
        options: list[Option[str]] = []

        for diff_info in Difficulty.get_all():
            name = str(diff_info["name"])
            options.append(
                Option[str](f"select_diff.{name}", name))

        super().__init__(get_text_cb, "select_diff.title", options)
