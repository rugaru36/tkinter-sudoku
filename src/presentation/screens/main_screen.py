from math import sqrt
from tkinter import NS, W, Button, Frame, Label, Menu, TclError, Tk
from typing import Callable, Final, override
from config.config_manager import ConfigManager
# from domain.ports.difficulty import DifficultyClass, DifficultyLiteral
from domain.game_process import GameProcess
from domain.ports.game_rules import GAME_FIELD_SIZE, DifficultyDataAsArray, DifficultyNameEnum, GameStatus
from lib.string import safe_str_to_enum
from presentation.locales.locale_manager import LocaleInfo
from presentation.screens.common.screen_with_keyboard_element_selection import ScreenWithKeyboardElementSelection


class MainScreen(ScreenWithKeyboardElementSelection[list[int]]):

    def __init__(self,
                 config_manager: ConfigManager,
                 locale_info_list: list[LocaleInfo],
                 cb_on_element_selected: Callable[[], None],
                 cb_get_text: Callable[[str], str],
                 cb_change_locale: Callable[[str], None],
                 cb_change_difficulty: Callable[[str], None]
                 ) -> None:

        self._cb_on_element_selected: Final = cb_on_element_selected
        self._cb_get_text: Final = cb_get_text
        self._cb_on_change_locale: Final = cb_change_locale
        self._cb_on_change_difficulty: Final = cb_change_difficulty

        self._config_manager: ConfigManager = config_manager
        self._locale_info_list: Final = locale_info_list

        self._root_widget: None | Tk = None
        self._num_buttons: list[list[Button]] = []
        self._reload_button: Button | None = None
        self._game_process: GameProcess | None = None
        self._selected_row: int | None = None
        self._selected_col: int | None = None
        self._is_in_progress: bool = True
        self._left_seconds_time: int = -1
        self._is_any_key_focused: bool = False

        self._status_label: Label | None = None
        default_focus_coordinates = [1, 0]
        super().__init__([GAME_FIELD_SIZE + 1, GAME_FIELD_SIZE], default_focus_coordinates)

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

    def run(self, difficulty: DifficultyNameEnum):
        if self._game_process:
            self._drop_screen_data()
            self._game_process.restart_process()
        else:
            self._game_process = GameProcess(self._update_status)

        need_to_restart_process = self._game_process.get_curr_difficulty != difficulty and self._game_process.get_is_in_progress()
        need_to_start_process = not self._game_process.get_is_in_progress()
        if need_to_restart_process or need_to_start_process:
            self._game_process.start_new_process(difficulty)
        self._show()

    def restart(self, with_game_process_reload: bool = True):
        difficulty_level = self._config_manager.get_difficulty_level()
        if with_game_process_reload and self._game_process and difficulty_level:
            self._game_process.start_new_process(difficulty_level)

        if not self._game_process and difficulty_level:
            self.run(difficulty_level)

        elif self._root_widget is not None:
            self._drop_screen_data()
            self._show()

    def _on_element_select(self, row: int, col: int):
        if not self._game_process:
            return
        is_unknown = self._game_process.check_is_unknown(row, col)
        if not is_unknown or not self._is_in_progress:
            return
        self._selected_row = row
        self._selected_col = col
        if self._cb_on_element_selected is not None:
            self._cb_on_element_selected()

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
        self._bind_default_key_handler(window)
        self._bind_dummy_for_focus(window)
        window.mainloop()

    def _draw_top_menu(self):
        if not self._root_widget:
            return
        main_menu = Menu()

        diff_menu = Menu(tearoff=0)
        for diff_info in DifficultyDataAsArray:
            diff_name_from_info = str(diff_info["name"])
            diff_menu.add_command(
                label=self._get_top_bar_difficulty_label(diff_name_from_info), command=lambda name=diff_name_from_info: self._on_change_difficulty(str(name)))

        locale_menu = Menu(tearoff=0)
        for locale_info in self._locale_info_list:
            locale_menu.add_command(
                label=self._get_top_bar_locale_label(locale_info), command=lambda code=locale_info["code"]: self._on_change_locale(code))

        main_menu.add_cascade(label=self._cb_get_text(
            "main_screen.top_menu.difficulty"), menu=diff_menu)
        main_menu.add_cascade(label=self._cb_get_text(
            "main_screen.top_menu.lang"), menu=locale_menu)
        _ = self._root_widget.config(menu=main_menu)

    def _draw_status_row(self):
        frame = Frame(self._root_widget, padx=5, pady=5)
        frame.grid(row=0, column=0, columnspan=3, sticky=W)
        reload_btn = Button(frame, text=self._cb_get_text(
            "main_screen.reload"), command=self.restart)
        reload_btn.grid(row=0, column=0, rowspan=1, ipady=15)
        self._reload_button = reload_btn
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

        status = GameStatus.get_status(
            left_elements, left_mistakes, left_seconds_time_total)

        time_msg = f"{self._cb_get_text("main_screen.time_left_msg")}: {left_mins}:{left_seconds}"
        tries_msg = f"{self._cb_get_text("main_screen.tries_left_msg")}: {left_mistakes}"
        left_to_fill_msg = f"{self._cb_get_text("main_screen.empty_left_msg")}: {left_elements}"

        try:
            if self._status_label is not None and self._root_widget is not None:
                self._status_label["text"] = f"{time_msg}\n{left_to_fill_msg}\n{tries_msg}"
        except TclError:
            pass
        self._is_in_progress = status == GameStatus.in_process

    def _on_destroy(self):
        if self._game_process is not None:
            self._game_process.stop_timer()
        if self._root_widget is not None:
            self._root_widget.destroy()

    def _on_change_difficulty(self, new_value: str):
        if not self._game_process:
            print("no game process")
            return
        if new_value == self._game_process.get_curr_difficulty():
            return
        self._cb_on_change_difficulty(new_value)
        self.restart(True)

    def _on_change_locale(self, new_value: str):
        if new_value == self._config_manager.get_locale():
            return
        self._cb_on_change_locale(new_value)
        self.restart(False)

    def _drop_screen_data(self):
        if self._root_widget:
            self._root_widget.destroy()
            self._root_widget = None
        self._num_buttons = []
        self._selected_row = None
        self._selected_col = None
        self._is_in_progress = True
        self._status_label = None
        self._drop_focused_element()

    def _get_top_bar_difficulty_label(self, difficulty: str):
        localized_diff = self._cb_get_text(f"select_diff.{difficulty}")
        casted_diff_lvl = safe_str_to_enum(difficulty, DifficultyNameEnum)
        if self._config_manager.get_difficulty_level() == casted_diff_lvl:
            return "> " + localized_diff
        return localized_diff

    def _get_top_bar_locale_label(self, locale_info: LocaleInfo):
        label = locale_info["name"]
        if locale_info["code"] == self._config_manager.get_locale():
            label = "> " + label
        return label

    @override
    def _get_focused_element_value(self):
        return self._focused_element_index

    @override
    def _check_coordinates_exist(self, row: int, col: int) -> bool:
        return not (row == 0 and col != self._focused_element_index[1])
    
    @override
    def _get_element_needed_to_focus(self):
        if self._focused_element_index[0] == 0 and self._reload_button:
            return self._reload_button
        row = self._focused_element_index[0]
        col = self._focused_element_index[1]
        target_button = self._num_buttons[row - 1][col]
        return target_button