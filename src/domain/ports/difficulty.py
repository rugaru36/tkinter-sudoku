from typing import Final


class Difficulty:
    easy: Final = "easy"
    mid: Final = "mid"
    hard: Final = "hard"

    @staticmethod
    def get_dif_data_by_name(name: str) -> dict[str, str | int]:
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
            case _: return Difficulty.get_dif_data_by_name(Difficulty.mid)

    @staticmethod
    def get_all():
        return [{
                "name": Difficulty.easy,
                "time_seconds": 15 * 60,
                "count_of_unknown_elements": 20,
                "count_of_mistakes": 10},
            {
                "name": Difficulty.mid,
                "time_seconds": 10 * 60,
                "count_of_unknown_elements": 30,
                "count_of_mistakes": 7
            },
            {
                "name": Difficulty.hard,
                "time_seconds": 5 * 60,
                "count_of_unknown_elements": 40,
                "count_of_mistakes": 4
            }
        ]