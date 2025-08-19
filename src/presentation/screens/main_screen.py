from math import sqrt
from tkinter import NS, W, Button, Frame, Label, Menu, Tk
from tkinter.messagebox import askyesno, showinfo
from typing import Callable, Final
from domain.difficulty import Difficulty
from domain.game_process import Game_Process
from domain.game_status import Game_Status
from presentation.locales.locale_manager import Locale_Info


class Main_Screen:

    def __init__(self,
                 locale_info_list: list[Locale_Info],
                 cb_on_element_selected: Callable[[], None],
                 cb_on_reload: Callable[[], None],
                 cb_get_text: Callable[[str], str],
                 cb_change_locale: Callable[[str], None],
                 cb_change_difficulty: Callable[[str], None]
                 ) -> None:
        self._cb_on_element_selected: Callable[[
        ], None] = cb_on_element_selected
        self._cb_on_reload: Callable[[], None] = cb_on_reload
        self._cb_get_text: Callable[[str], str] = cb_get_text
        self._cb_change_locale: Callable[[str], None] = cb_change_locale
        self._cb_change_difficulty: Callable[[
            str], None] = cb_change_difficulty

        self._difficulty: str | None = None
        self._locale_info_list: Final = locale_info_list

        self._root_widget: None | Tk = None
        self._num_buttons: list[list[Button]] = []
        self._game_process: Game_Process | None = None
        self._selected_row: int | None = None
        self._selected_col: int | None = None
        self._is_in_progress: bool = True
        self._left_seconds_time: int = -1

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
        self._update_status()

    def get_is_in_progress(self):
        return self._is_in_progress

    def run(self, difficulty: str):
        self._difficulty = difficulty
        if self._game_process:
            self._reload_values_to_default()
        else:
            self._game_process = Game_Process(self._update_status)
        self._game_process.start(difficulty)
        self._show()

    def _on_element_select(self, row: int, col: int):
        if self._game_process is None:
            return
        is_unknown = self._game_process.check_is_unknown(row, col)
        if not is_unknown or not self._is_in_progress:
            return
        self._selected_row = row
        self._selected_col = col
        if not self._cb_on_element_selected is None:
            self._cb_on_element_selected()

    def _on_reload(self):
        self._on_destroy()
        if self._root_widget is not None:
            self._root_widget = None
        self._cb_on_reload()

    def _show(self):
        window = Tk()
        window.resizable(False, False)
        window.protocol("WM_DELETE_WINDOW", self._on_destroy)

        self._draw_status_row()
        self._draw_num_field()

        window.title(self._cb_get_text("main_screen.title"))

        self._root_widget = window
        self._update_status()
        self._draw_top_menu()
        window.mainloop()

    def _draw_top_menu(self):
        if self._root_widget is not None:
            main_menu = Menu()

            diff_menu = Menu(tearoff=0)
            diff_menu.add_command(
                label="Easy", command=lambda: self._on_change_difficulty(Difficulty.easy))
            diff_menu.add_command(
                label="Mid", command=lambda: self._on_change_difficulty(Difficulty.mid))
            diff_menu.add_command(
                label="Hard", command=lambda: self._on_change_difficulty(Difficulty.hard))

            locale_menu = Menu(tearoff=0)
            for locale_info in self._locale_info_list:
                locale_menu.add_command(
                    label=locale_info.name, command=lambda code=locale_info.code: self._cb_change_locale(code))

            main_menu.add_cascade(label="Difficulty", menu=diff_menu)
            main_menu.add_cascade(label="Locale", menu=locale_menu)
            _ = self._root_widget.config(menu=main_menu)

    def _draw_status_row(self):
        frame = Frame(self._root_widget, padx=5, pady=5)
        frame.grid(row=0, column=0, columnspan=3, sticky=W)

        reload_btn = Button(frame, text=self._cb_get_text(
            "main_screen.reload"), command=self._on_reload)
        reload_btn.grid(row=0, column=0, rowspan=1, ipady=15)

        status_label = Label(frame, text="", justify="left")
        status_label.grid(row=0, column=1, rowspan=1, sticky=NS, padx=5)

        self._status_label = status_label
        self._update_status()

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

    def _update_status(self):
        if self._game_process is None:
            return
        left_elements = self._game_process.get_unknown_elements_count()
        left_mistakes = self._game_process.get_left_mistakes()
        left_seconds_time_total = self._game_process.get_time_left()
        left_mins, left_seconds = divmod(left_seconds_time_total, 60)

        status = Game_Status.get_status(
            left_elements, left_mistakes, left_seconds_time_total)

        time_msg = f"{self._cb_get_text("main_screen.time_left_msg")}: {left_mins}:{left_seconds}"
        tries_msg = f"{self._cb_get_text("main_screen.tries_left_msg")}: {left_mistakes}"
        left_to_fill_msg = f"{self._cb_get_text("main_screen.empty_left_msg")}: {left_elements}"

        try:
            if self._status_label is not None and self._root_widget is not None:
                self._status_label["text"] = f"{time_msg}\n{left_to_fill_msg}\n{tries_msg}"
        except:
            pass
        self._is_in_progress = status == Game_Status.in_process

    def _on_destroy(self):
        if self._game_process is not None:
            self._game_process.stop()
        if self._root_widget is not None:
            self._root_widget.destroy()

    def _on_change_difficulty(self, new_value: str):
        if new_value == self._difficulty:
            _ = showinfo("same diff", "da same diff bro")
            return
        is_change_confirmed = askyesno("u sure?", "ar u sure bout dis?")
        if is_change_confirmed: 
            self._reload_values_to_default()
            self._cb_change_difficulty(new_value)

    def _reload_values_to_default(self):
        if self._root_widget:
            self._root_widget.destroy()
            self._root_widget = None
        if not self._game_process is None:
            self._game_process.stop()
        self._num_buttons = []
        self._selected_row = None
        self._selected_col = None
        self._is_in_progress = True
        self._status_label = None
