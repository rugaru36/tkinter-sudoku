class Game_Status:
    in_process: str = "In Progress"
    game_is_lost: str = "Game Is Lost"
    game_is_won: str = "Game Is Won"

    @staticmethod
    def get_status(elements_left: int, mistakes_left: int, time_left: int) -> str:
        if mistakes_left <= 0 or time_left <= 0 and elements_left > 0:
            return Game_Status.game_is_lost
        elif elements_left == 0:
            return Game_Status.game_is_won
        else:
            return Game_Status.in_process
