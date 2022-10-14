'''
General file with class used to game management.
'''

import sys

import pygame
from pygame.surface import Surface

from settings import Settings


class AlienInvasion():
    ''' General class to game management. '''

    def __init__(self) -> None:
        ''' Game initialization. '''
        pygame.init()  # Initialization of screen.
        pygame.display.set_caption('Alien Invasion')
        self.settings: Settings = Settings()
        self.screen: Surface = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

    def run_game(self) -> None:
        ''' Main loop of the game. '''
        while True:
            for event in pygame.event.get():  # Wait for button press.
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.settings.background_color)
            pygame.display.flip()  # Update of the screen.


if __name__ == '__main__':
    # Instance of game
    ai: AlienInvasion = AlienInvasion()
    ai.run_game()
