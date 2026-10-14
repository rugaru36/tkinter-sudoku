from enum import Enum, StrEnum

GAME_FIELD_SIZE = 9

class GameStatus:
    in_process: str = "In Progress"
    game_is_lost: str = "Game Is Lost"
    game_is_won: str = "Game Is Won"

    @staticmethod
    def get_status(elements_left: int, mistakes_left: int, time_left: int) -> str:
        if mistakes_left <= 0 or time_left <= 0 and elements_left > 0:
            return GameStatus.game_is_lost
        elif elements_left == 0:
            return GameStatus.game_is_won
        else:
            return GameStatus.in_process

# DifficultyNameLiteral = Literal["easy", "mid", "hard"]

class DifficultyNameEnum(StrEnum):
    Easy = "easy"
    Medium = "mid"
    Hard = "hard"

DifficultyDataByNames = {
    DifficultyNameEnum.Easy: {
        "name": DifficultyNameEnum.Easy.value,
        "time_seconds": 15 * 60,
        "count_of_unknown_elements": 20,
        "count_of_mistakes": 10
    },
    DifficultyNameEnum.Medium: {
        "name": DifficultyNameEnum.Medium.value,
        "time_seconds": 10 * 60,
        "count_of_unknown_elements": 30,
        "count_of_mistakes": 7
    },
    DifficultyNameEnum.Hard: {
        "name": DifficultyNameEnum.Hard.value,
        "time_seconds": 5 * 60,
        "count_of_unknown_elements": 40,
        "count_of_mistakes": 4
    }
}

DifficultyDataAsArray = list(DifficultyDataByNames.values())