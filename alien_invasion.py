'''
General file with class used to game management.
'''

import sys

import pygame
from pygame.surface import Surface

from settings import Settings
from spaceship import Spaceship


class AlienInvasion():
    ''' General class to game management. '''

    def __init__(self) -> None:
        ''' Game initialization. '''
        pygame.init()  # Initialization of screen.
        pygame.display.set_caption('Alien Invasion')
        self.settings: Settings = Settings()
        self.screen: Surface = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        self.ship: Spaceship = Spaceship(self)

    def run_game(self) -> None:
        ''' Main loop of the game. '''
        while True:
            self._check_events()
            self._update_screen()

    def _check_events(self) -> None:
        ''' Check reaction to button press and mouse interaction. '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self) -> None:
        ''' Updates the screen. '''
        self.screen.fill(self.settings.background_color)
        self.ship.blitme()
        pygame.display.flip()  # Update of the screen.


if __name__ == '__main__':
    # Instance of game
    ai: AlienInvasion = AlienInvasion()
    ai.run_game()
