from tkinter import NSEW, Button, Tk
from typing import Callable, Final

from domain.difficulty import Difficulty


class Difficulty_Select_Screen:
    def __init__(self, get_text_cb: Callable[[str], str]) -> None:
        self._root_widget: Tk | None = None
        self._selected_difficulty: str | None = None
        self._get_text_cb: Final = get_text_cb

    def run(self):
        self._selected_difficulty = None
        self._show()
        return self._selected_difficulty

    def _show(self):
        window = Tk()
        window.resizable(False, False)

        window.title(self._get_text_cb("select_diff.title"))

        easy_btn = Button(text=self._get_text_cb("select_diff.easy"),
                          command=lambda: self._on_select(Difficulty.easy))
        mid_btn = Button(text=self._get_text_cb("select_diff.mid"),
                         command=lambda: self._on_select(Difficulty.mid))
        hard_btn = Button(text=self._get_text_cb("select_diff.hard"),
                          command=lambda: self._on_select(Difficulty.hard))

        easy_btn.grid(row=0, column=0, columnspan=10, ipadx=100,
                      ipady=6, padx=4, pady=4, sticky=NSEW)
        mid_btn.grid(row=1, column=0, columnspan=10, ipadx=100,
                     ipady=6, padx=4, pady=4, sticky=NSEW)
        hard_btn.grid(row=2, column=0, columnspan=10, ipadx=100,
                      ipady=6, padx=4, pady=4, sticky=NSEW)

        self._root_widget = window
        window.mainloop()

    def _on_select(self, difficulty: str):
        self._selected_difficulty = difficulty
        self._destroy_root_widget()

    def _destroy_root_widget(self):
        if self._root_widget is not None:
            self._root_widget.destroy()
