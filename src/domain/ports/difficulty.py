from typing import Final


class Difficulty:
    easy: Final = "Easy"
    mid: Final = "Medium"
    hard: Final = "Hard"

    @staticmethod
    def get_dif_data(name: str) -> dict[str, str | int]:
        match name:
            case Difficulty.easy:
                return {
                    "name": name,
                    "time_seconds": 15 * 60,
                    "count_of_unknown_elements": 20,
                    "count_of_mistakes": 10}
            case Difficulty.mid:
                return {
                    "name": name,
                    "time_seconds": 10 * 60,
                    "count_of_unknown_elements": 30,
                    "count_of_mistakes": 7
                }
            case Difficulty.hard:
                return {
                    "name": name,
                    "time_seconds": 5 * 60,
                    "count_of_unknown_elements": 40,
                    "count_of_mistakes": 4
                }
            case _: return Difficulty.get_dif_data(Difficulty.mid)
