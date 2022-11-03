"""
General module with game statistics implementation.
"""


class GameStats():
    """ Class representing game statistics. """

    def __init__(self, ai_game) -> None:
        """ Initialize game statistics. """
        self.settings = ai_game.settings

        self.highest_score: int = 0
        self.current_score: int = 0
        self.current_level: int = 1
        self.remaining_player_ships: int = self.settings.player_ships_limit

    def reset_stats(self) -> None:
        """ Resets statistical data, which can change during the game. """
        self.current_score = 0
        self.current_level = 1
        self.remaining_player_ships = self.settings.player_ships_limit
