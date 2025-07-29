from tkinter import NSEW, Button, PhotoImage, Tk

from domain.difficulty import Difficulty


class Difficulty_Selector:
    def __init__(self) -> None:
        self._root_widget: Tk | None = None
        self._selected_difficulty: str | None = None

    def select(self):
        self._show()
        return self._selected_difficulty

    def _show(self):
        window = Tk()
        window.resizable(False, False)
        try:
            window.iconphoto(False, PhotoImage(file='./icon.png'))
        except:
            print("problem while loading icon")

        window.title("Select difficulty")

        easy_btn = Button(text=Difficulty.easy,
                          command=lambda: self._on_select(Difficulty.easy))
        mid_btn = Button(text=Difficulty.mid,
                         command=lambda: self._on_select(Difficulty.mid))
        hard_btn = Button(text=Difficulty.hard,
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
