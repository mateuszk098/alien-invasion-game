'''
General file with class representing game statistics.
'''

import pygame


class GameStats():
    ''' Class representing game statistics. '''

    ships_left: int
    score: int
    game_level: int

    def __init__(self, ai_game) -> None:
        ''' Initialize statistics. '''
        self.settings = ai_game.settings
        self.game_active: bool = False
        self.high_score: int = 0
        self.reset_stats()

    def reset_stats(self) -> None:
        ''' Initialize statistical data, which can change during game. '''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.game_level = 1
