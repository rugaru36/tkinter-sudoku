def shift_looped_sequence(sequence: list[int], offset: int = 0):
    if offset <= 0:
        return sequence
    first_part = sequence[:offset]
    second_part = sequence[offset:]
    return second_part + first_part
