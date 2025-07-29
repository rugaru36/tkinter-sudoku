from typing import TypeVar

GenericListType = TypeVar('GenericListType')


def shift_looped_sequence(sequence: list[GenericListType], offset: int = 0):
    if offset <= 0:
        return sequence
    first_part = sequence[:offset]
    second_part = sequence[offset:]
    return second_part + first_part
