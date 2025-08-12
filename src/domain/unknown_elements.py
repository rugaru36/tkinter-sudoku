import random
# state of fullfilling process


class Unknown_Elements_Storage:
    def __init__(self) -> None:
        self._unknown_elements_coordinates: list[list[int]] = []
        # self._size_of_field: Final = size_of_field
        # self._num_of_unknown_elements: Final = num_of_unknown

    def generate(self, num_of_unknown: int, size_of_field: int = 9):
        self._unknown_elements_coordinates = []
        min = 0
        max = size_of_field - 1
        for _ in range(num_of_unknown):
            global row
            global col
            row = random.randint(min, max)
            col = random.randint(min, max)
            while self._get_unknown_element_index(row, col):
                row = random.randint(min, max)
                col = random.randint(min, max)
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
