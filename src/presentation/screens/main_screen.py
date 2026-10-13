from math import sqrt
from tkinter import NS, W, Button, Frame, Label, Menu, TclError, Tk
from typing import Callable, Final, Literal, override
from config.config_manager import ConfigManager
from domain.ports.difficulty import Difficulty
from domain.game_process import GameProcess
from domain.ports.game_status import GameStatus
from presentation.locales.locale_manager import LocaleInfo
from presentation.screens.common.screen_with_keyboard_element_selection import ScreenWithKeyboardElementSelection
from presentation.screens.common.screen_with_keyboard_handling import ArrowKeysSymLiteral


class MainScreen(ScreenWithKeyboardElementSelection):

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
        self._focused_element_index: list[int] = [0, 0]
        super().__init__([9, 10])

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
        window.mainloop()

    def _focus_button_needed_to_focus(self):
        if self._focused_element_index[0] == -1 and self._reload_button:
            self._reload_button.focus()
            return
        elif self._focused_element_index[0] == -1:
            return
        x_index = self._focused_element_index[0]
        y_index = self._focused_element_index[1]
        target_button = self._num_buttons[x_index][y_index]
        if target_button:
            target_button.focus()
            self._is_any_key_focused = True

    def _remove_key_focus(self):
        if self._root_widget:
            self._root_widget.focus()
        self._focused_element_index = [0, 0]
        self._is_any_key_focused = False

    def _draw_top_menu(self):
        if not self._root_widget:
            return
        main_menu = Menu()

        diff_menu = Menu(tearoff=0)
        for diff_info in Difficulty.get_all():
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
        self._is_any_key_focused = False

    def _get_top_bar_difficulty_label(self, difficulty: str):
        localized_diff = self._cb_get_text(f"select_diff.{difficulty}")
        if self._config_manager.get_difficulty_level() == difficulty:
            return "> " + localized_diff
        return localized_diff

    def _get_top_bar_locale_label(self, locale_info: LocaleInfo):
        label = locale_info["name"]
        if locale_info["code"] == self._config_manager.get_locale():
            label = "> " + label
        return label

    @override
    def _handle_arrow_key(self, direction: ArrowKeysSymLiteral):
        if not self._game_process:
            return
        if not self._is_any_key_focused:
            self._focus_button_needed_to_focus()
            return

        field_size = self._game_process.get_num_field_size()
        hor_or_vert: Literal["horizontal", "vertical"] | None = None
        new_index: None | int = None

        if direction == "Down":
            new_index = self._focused_element_index[0] + 1
            hor_or_vert = "vertical"
        elif direction == "Up":
            new_index = self._focused_element_index[0] - 1
            hor_or_vert = "vertical"
        elif direction == "Right":
            new_index = self._focused_element_index[1] + 1
            hor_or_vert = "horizontal"
        elif direction == "Left":
            new_index = self._focused_element_index[1] - 1
            hor_or_vert = "horizontal"

        if hor_or_vert == "horizontal" and new_index == field_size:
            new_index = 0
        elif hor_or_vert == "vertical" and new_index == field_size:
            new_index = -1
        elif hor_or_vert == "horizontal" and new_index == -1:
            new_index = field_size - 1
        elif hor_or_vert == "vertical" and new_index == -2:
            new_index = field_size - 1

        if hor_or_vert == "horizontal" and self._focused_element_index[1] == -1:
            return
        if hor_or_vert == "horizontal" and new_index < field_size and new_index >= 0:
            self._focused_element_index[1] = new_index
        elif hor_or_vert == "vertical" and new_index < field_size and new_index >= -1:
            self._focused_element_index[0] = new_index
        self._focus_button_needed_to_focus()

    @override
    def _handle_enter_key(self):
        x_index = self._focused_element_index[0]
        y_index = self._focused_element_index[1]
        self._on_element_select(x_index, y_index)

    @override
    def _handle_escape_key(self):
        self._remove_key_focus()
