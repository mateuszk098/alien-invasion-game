'''
Simple pygame blue window.
'''


import sys

import pygame

from menu import Menu
from settings import Settings
from game_stats import GameStats


class BlueWindow():
    ''' Simple class representing a blue pygame window. '''

    def __init__(self) -> None:
        pygame.init()
        self.settings: Settings = Settings()
        self.stats: GameStats = GameStats(self)
        self.screen = pygame.display.set_mode((1280, 720))
        self.screen.fill((21, 24, 56))  # Blue screen.
        self.menu: Menu = Menu(self)

    def run_game(self) -> None:
        while True:
            self._check_events()
            self.menu.draw_menu()
            pygame.display.flip()  # Update of the screen.

    def _check_events(self) -> None:
        ''' Check reaction to button press/release and mouse interaction. '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos: tuple[int, int] = pygame.mouse.get_pos()
                self.menu.check_play_button(mouse_pos)
                self.menu.check_difficulty_button(mouse_pos)


if __name__ == '__main__':
    my_window = BlueWindow()
    my_window.run_game()
