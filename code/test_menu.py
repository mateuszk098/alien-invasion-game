'''
Simple pygame blue window.
'''


import sys

import pygame as pg

from menu import Menu
from settings import Settings
from game_stats import GameStats


class BlueWindow():
    ''' Simple class representing a blue pygame window. '''

    def __init__(self) -> None:
        pg.init()
        self.settings: Settings = Settings()
        self.stats: GameStats = GameStats(self)
        self.screen = pg.display.set_mode((1280, 720))
        self.screen_rect = self.screen.get_rect()
        self.screen.fill((21, 24, 56))  # Blue screen.
        self.menu: Menu = Menu(self)

    def run_game(self) -> None:
        while True:
            self.screen.fill((21, 24, 56))
            self._check_events()
            self.menu.draw_menu()
            pg.display.flip()  # Update of the screen.

    def _check_events(self) -> None:
        ''' Check reaction to button press/release and mouse interaction. '''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    sys.exit()
                if event.key == pg.K_ESCAPE:
                    self.menu.return_to_menu()
                if event.key == pg.K_h:
                    self.menu.show_help()
                if event.key == pg.K_s:
                    self.menu.show_settings()
                if event.key == pg.K_1:
                    self.menu.switch_to_easy_mode()
                if event.key == pg.K_2:
                    self.menu.switch_to_medium_mode()
                if event.key == pg.K_3:
                    self.menu.switch_to_hard_mode()
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos: tuple[int, int] = pg.mouse.get_pos()
                if self.menu.check_exit_button(mouse_pos):
                    sys.exit()
                if self.menu.check_help_button(mouse_pos):
                    self.menu.show_help()
                if self.menu.check_easy_button(mouse_pos):
                    self.menu.switch_to_easy_mode()
                if self.menu.check_medium_button(mouse_pos):
                    self.menu.switch_to_medium_mode()
                if self.menu.check_hard_button(mouse_pos):
                    self.menu.switch_to_hard_mode()
                if self.menu.check_settings_button(mouse_pos):
                    self.menu.show_settings()
                if self.menu.check_exit_from_settings(mouse_pos):
                    self.menu.return_to_menu()


if __name__ == '__main__':
    my_window = BlueWindow()
    my_window.run_game()
