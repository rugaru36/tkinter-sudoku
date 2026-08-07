import random
# state of fulfilling process


class UnknownElementsStorage:
    def __init__(self) -> None:
        self._unknown_elements_coordinates: list[list[int]] = []

    def generate(self, num_of_unknown: int, size_of_field: int = 9):
        self._unknown_elements_coordinates = []
        low = 0
        high = size_of_field - 1
        for _ in range(num_of_unknown):
            row = random.randint(low, high)
            col = random.randint(low, high)
            while self._get_unknown_element_index(row, col) is not None:
                row = random.randint(low, high)
                col = random.randint(low, high)
            self._unknown_elements_coordinates.append([row, col])

    def get_count(self):
        return len(self._unknown_elements_coordinates)

    def get_coordinates(self):
        return self._unknown_elements_coordinates

    def remove_pair(self, row: int, col: int):
        index = self._get_unknown_element_index(row, col)
        if index is not None:
            del self._unknown_elements_coordinates[index]

    def check_is_actually_unknown(self, row: int, col: int):
        index = self._get_unknown_element_index(row, col)
        return index is not None

    def _get_unknown_element_index(self, row: int, col: int):
        for index in range(len(self._unknown_elements_coordinates)):
            element = self._unknown_elements_coordinates[index]
            element_row = element[0]
            element_col = element[1]
            if element_row == row and element_col == col:
                return index
        return None
