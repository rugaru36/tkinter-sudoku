from math import sqrt
from tkinter import NS, W, Button, Frame, Label, PhotoImage, Tk
from typing import Callable, Final
from domain.game_process import Game_Process
from domain.game_status import Game_Status


class Main_Screen:

    def __init__(self, cb_on_element_selected: Callable[[], None], cb_on_reload: Callable[[], None]) -> None:
        self._cb_on_element_selected: Final = cb_on_element_selected
        self._cb_on_reload: Final = cb_on_reload

        self._root_widget: None | Tk = None
        self._num_buttons: list[list[Button]] = []
        self._game_process: Game_Process | None = None
        self._selected_row: int | None = None
        self._selected_col: int | None = None
        self._is_in_progress: bool = True

        self._status_label: Label | None = None

    def on_new_value(self, value: int):
        if self._game_process is None:
            return
        row = self._selected_row
        col = self._selected_col
        if row is None or col is None:
            raise ValueError("element was not selected earlier!")
        is_correct = self._game_process.on_new_value(value, row, col)
        if is_correct:
            correct_value = self._game_process.get_num_field_value(row, col)
            self._num_buttons[row][col]["text"] = str(correct_value)
        self._update_status_label()

    def run(self, difficulty: str):
        if self._game_process:
            self._game_process.reload(difficulty)
            self._reload_values_to_default()
        else:
            self._game_process = Game_Process(difficulty)
        self._show()

    def _on_element_select(self, row: int, col: int):
        if self._game_process is None:
            return
        is_unknown = self._game_process.check_is_unknown(row, col)
        if not is_unknown or not self._is_in_progress:
            return
        self._selected_row = row
        self._selected_col = col
        self._cb_on_element_selected()

    def _on_reload(self):
        if self._root_widget is not None:
            self._root_widget.destroy()
            self._root_widget = None
        self._cb_on_reload()

    def _show(self):
        window = Tk()
        window.resizable(False, False)
        try:
            window.iconphoto(False, PhotoImage(file='icon.png'))
        except:
            print("problem while loading icon")

        self._draw_top_menu()
        self._draw_num_field()

        window.title("Game")

        self._root_widget = window
        window.mainloop()

    def _draw_top_menu(self):
        frame = Frame(self._root_widget, padx=5, pady=5)
        frame.grid(row=0, column=0, columnspan=3, sticky=W)

        reload_btn = Button(frame, text="Reload", command=self._on_reload)
        reload_btn.grid(row=0, column=0, rowspan=1, ipady=15)

        status_label = Label(frame, text="", justify="left")
        status_label.grid(row=0, column=1, rowspan=1, sticky=NS, padx=5)

        self._status_label = status_label
        self._update_status_label()

    def _draw_num_field(self):
        if self._game_process is None:
            return
        field_size = self._game_process.get_num_field_size()

        # generate empty frames (groups)
        field_frames: list[list[Frame]] = []
        needed_to_have_frames = int(sqrt(field_size))
        for block_row in range(needed_to_have_frames):
            curr_blocks_row: list[Frame] = []
            for block_col in range(needed_to_have_frames):
                frame = Frame(padx=5, pady=5)
                frame.grid(column=block_col, row=block_row + 1)
                curr_blocks_row.append(frame)
            field_frames.append(curr_blocks_row)

        # fill frames with elements
        block_elements = int(sqrt(field_size))
        curr_frame: Frame | None = None
        for row in range(field_size):
            row_buttons: list[Button] = []
            for col in range(field_size):
                curr_frame = field_frames[row //
                                          block_elements][col // block_elements]
                is_unknown = self._game_process.check_is_unknown(row, col)
                btn_text = "" if is_unknown else str(
                    self._game_process.get_num_field_value(row, col))
                btn = Button(curr_frame, text=btn_text, width=1,
                             command=lambda row=row, col=col: self._on_element_select(row, col))
                btn.grid(column=col, row=row)
                row_buttons.append(btn)
            self._num_buttons.append(row_buttons)

    def _update_status_label(self):
        if self._game_process is None:
            return
        left_elements = self._game_process.get_unknown_elements_count()
        # left
        left_mistakes = self._game_process.get_left_mistakes()
        status = Game_Status.get_status(left_elements, left_mistakes)
        if self._status_label is not None:
            self._status_label["text"] = f"Game status: {status}.\nLeft to fill: {left_elements}\nMistakes left: {left_mistakes}"
        self._is_in_progress = status == Game_Status.in_process

    def _reload_values_to_default(self):
        if self._root_widget:
            self._root_widget.destroy()
            self._root_widget = None
        self._num_buttons = []
        self._selected_row = None
        self._selected_col = None
        self._is_in_progress = True
        self._status_label = None
