from math import sqrt
import random
from typing import Final
from lib.shift_looped_sequence import shift_looped_sequence


class Game_Num_Matrix:

    def __init__(self) -> None:
        self._matrix: list[list[int]] = []
        # self._generate_game_matrix()

    def generate(self):
        self._matrix = []
        self._generate_game_matrix()

    def get_size(self):
        return len(self._matrix)

    def get_matrix(self):
        return self._matrix

    def get_single_val(self, row: int, col: int):
        return self._matrix[row][col]

    def _generate_game_matrix(self):
        size: Final[int] = 9
        block_size: Final[int] = int(sqrt(size))
        dictionary: Final[list[int]] = list(range(1, size + 1))
        random.shuffle(dictionary)
        row_num_in_block = 0
        row_block_num = 0
        # generate base non-random game matrix with dictionary
        for row in range(size):
            if row > 0 and row % block_size == 0:
                row_num_in_block = 0
                row_block_num += 1
            row = shift_looped_sequence(
                dictionary, row_num_in_block*3 + row_block_num)
            self._matrix.append(row)
            row_num_in_block += 1
        # randomize game matrix
        for _ in range(10):
            block_index = 0
            for diag_index in range(size):
                if diag_index > 0 and diag_index % block_size == 0:
                    block_index += 1
                min_to_swap = block_size * block_index
                max_to_swap = block_size * (block_index + 1) - 1
                random_col_pair_to_swap = random.randint(
                    min_to_swap, max_to_swap)
                random_row_pair_to_swap = random.randint(
                    min_to_swap, max_to_swap)
                self._swap_matrix_cols(diag_index, random_col_pair_to_swap)
                self._swap_matrix_rows(diag_index, random_row_pair_to_swap)

    def _swap_matrix_cols(self, sourceCol: int, targetCol: int) -> None:
        if sourceCol == targetCol:
            return
        for row in range(len(self._matrix)):
            buff = self._matrix[row][targetCol]
            self._matrix[row][targetCol] = self._matrix[row][sourceCol]
            self._matrix[row][sourceCol] = buff

    def _swap_matrix_rows(self, sourceRow: int, targetRow: int) -> None:
        if sourceRow == targetRow:
            return
        for col in range(len(self._matrix)):
            buff = self._matrix[targetRow][col]
            self._matrix[targetRow][col] = self._matrix[sourceRow][col]
            self._matrix[sourceRow][col] = buff
