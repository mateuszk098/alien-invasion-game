"""
This module provides a GameStats object, which store statistics acquired during the game.
"""


class GameStats():
    """GameStats object provides tracking of the game statistics."""

    def __init__(self, ai_game) -> None:
        """Initialise GameStats object."""
        self.settings = ai_game.settings
        self.highest_score: int = 0
        self.current_score: int = 0
        self.current_level: int = 1
        self.remaining_player_ships: int = self.settings.player_ships_limit

    def reset_stats(self) -> None:
        """Resets game statistics to the initial state."""
        self.current_score = 0
        self.current_level = 1
        self.remaining_player_ships = self.settings.player_ships_limit
