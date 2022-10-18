'''
General file with class representing game statistics.
'''

import pygame


class GameStats():
    ''' Class representing game statistics. '''

    def __init__(self, ai_game) -> None:
        ''' Initialize statistics. '''
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active: bool = False

    def reset_stats(self) -> None:
        ''' Initialize statistical data, which can change during game. '''
        self.ships_left: int = self.settings.ship_limit
