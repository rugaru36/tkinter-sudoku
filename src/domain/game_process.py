from typing import Callable, Final
from domain.difficulty import Difficulty
from domain.game_num_matrix import Game_Num_Matrix
from domain.unknown_elements import Unknown_Elements_Storage
from lib.timer import Timer

# main interface for gui modules


class Game_Process:
    def __init__(self, cb_timer_tick_handler: Callable[[], None] | None = None) -> None:
        self._cb_timer_tick_handler: Final = cb_timer_tick_handler
        self._init_unknown_elements_count: int = 0
        self._unknown_elements_left: int = 0
        self._mistakes_left: int = 0
        self._left_seconds_time: int = -1
        self._timer: Final = Timer(1, self._timer_handler, 'game_timer')

        self._diffculty_name: str = Difficulty.mid
        self._game_num_matrix: Final = Game_Num_Matrix()
        self._filling_state: Final = Unknown_Elements_Storage()

        self._is_in_progress: bool = False

    def start(self, diffculty_name: str):
        self._diffculty_name = diffculty_name
        self._parse_difficulty()
        self._is_in_progress = True
        self._filling_state.generate(self._init_unknown_elements_count)
        self._game_num_matrix.generate()
        self._timer.start()

    def stop(self):
        self._timer.stop()

    def on_new_value(self, value: int, row: int, col: int) -> bool:
        if not self._is_in_progress:
            return False

        is_actually_unknown = self._filling_state.check_is_actually_unknown(
            row, col)
        if not is_actually_unknown:
            raise ValueError("something gone wrong!")
        correct_value = self._game_num_matrix.get_single_val(row, col)
        is_correct_value = value == correct_value
        if is_correct_value:
            self._filling_state.remove_pair(row, col)
            self._unknown_elements_left -= 1
        else:
            self._mistakes_left -= 1
            if self._mistakes_left == 0:
                self._is_in_progress = False
        return is_correct_value

    def get_is_in_progress(self):
        return self._is_in_progress

    def get_time_left(self):
        return self._left_seconds_time

    def get_num_field_value(self, row: int, col: int):
        return self._game_num_matrix.get_single_val(row, col)

    def get_num_field_size(self):
        return self._game_num_matrix.get_size()

    def get_unknown_elements_coordinates(self):
        return self._filling_state.get_coordinates()

    def get_unknown_elements_count(self):
        return self._filling_state.get_count()

    def get_left_mistakes(self):
        return self._mistakes_left

    def check_is_unknown(self, row: int, col: int):
        return self._filling_state.check_is_actually_unknown(row, col)

    def _parse_difficulty(self):
        difficulty_data = Difficulty.get_dif_data(self._diffculty_name)
        self._mistakes_left = int(difficulty_data["count_of_mistakes"])
        self._init_unknown_elements_count = int(
            difficulty_data["count_of_unknown_elements"])
        self._left_seconds_time = int(difficulty_data["time_seconds"])
        self._unknown_elements_left = self._init_unknown_elements_count

    def _timer_handler(self):
        if self._left_seconds_time > 0:
            self._left_seconds_time -= 1
        else:
            self._is_in_progress = False
            self._timer.stop()
        if self._cb_timer_tick_handler is not None:
            self._cb_timer_tick_handler()
