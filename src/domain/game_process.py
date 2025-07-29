from typing import Final
from domain.difficulty import Difficulty
from domain.filling_state import Filling_State
from domain.num_field import Num_Field

# main interface for gui modules


class Game_Process:

    def __init__(self, diffculty_name: str = Difficulty.mid) -> None:
        self._diffculty_name: str = diffculty_name
        self._init_unknown_elements_count: int = 0
        self._unknown_elements_left: int = 0
        self._mistakes_left: int = 0

        # self._selected_row: int | None = None
        # self._selected_col: int | None = None

        self._parse_difficulty()
        self._num_field: Final = Num_Field()
        self._filling_state: Final = Filling_State(
            self._num_field.get_matrix_size(), self._init_unknown_elements_count)

    def reload(self, diffculty_name: str | None):
        if diffculty_name is not None:
            self._diffculty_name = diffculty_name
        self._filling_state.reload()
        self._num_field.reload()
        self._parse_difficulty()

    def on_new_value(self, value: int, row: int, col: int) -> bool:
        is_actually_unknown = self._filling_state.check_is_actually_unknown(
            row, col)
        if not is_actually_unknown:
            raise ValueError("something gone wrong!")
        correct_value = self._num_field.get_matrix_val(row, col)
        is_correct_value = value == correct_value
        if is_correct_value:
            self._filling_state.remove_unknown_coordinates_pair(row, col)
            self._unknown_elements_left -= 1
        else:
            self._mistakes_left -= 1
        return is_correct_value

    def get_num_field_value(self, row: int, col: int):
        return self._num_field.get_matrix_val(row, col)

    def get_num_field_size(self):
        return self._num_field.get_matrix_size()

    def get_unknown_elements_coordinates(self):
        return self._filling_state.get_unknown_elements_coordinates()

    def get_unknown_elements_count(self):
        return self._filling_state.get_unknown_elements_count()

    def get_left_mistakes(self):
        return self._mistakes_left

    def check_is_unknown(self, row: int, col: int):
        return self._filling_state.check_is_actually_unknown(row, col)

    def _parse_difficulty(self):
        difficulty_data = Difficulty.get_dif_data(self._diffculty_name)
        self._mistakes_left = int(difficulty_data["count_of_mistakes"])
        self._init_unknown_elements_count = int(
            difficulty_data["count_of_unknown_elements"])
        self._unknown_elements_left = self._init_unknown_elements_count
