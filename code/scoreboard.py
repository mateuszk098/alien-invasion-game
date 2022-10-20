'''
General file with class representing game statitstics.
'''

import pygame.font
from pygame.sprite import Group

from spaceship import Spaceship


class Scoreboard():
    ''' Class representing game statistics. '''

    def __init__(self, ai_game) -> None:
        ''' Initialize game statistics. '''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings.
        self.text_color: tuple[int, ...] = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)  # type: ignore

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self) -> None:
        ''' Transforms current score into image. '''
        score_str: str = f'Score: {self.stats.score:,}'
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.background_color)  # type: ignore

        # Display this in the right-top corner.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self) -> None:
        ''' Display punctation on the screen. '''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self) -> None:
        ''' Transforms best score into image. '''
        high_score_str: str = f'Best Score: {self.stats.high_score:,}'
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.settings.background_color)  # type: ignore

        # Display this on the top.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self) -> None:
        ''' Check if we have the best score in the game. '''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self) -> None:
        level_str: str = f'Level: {self.stats.game_level}'
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.background_color)  # type: ignore

        # Display this under the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self) -> None:
        ''' Displays number of ships remaining in the game. '''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship: Spaceship = Spaceship(self.ai_game, resized=True)
            ship.rect.x = self.screen_rect.left + 20 + ship_number*(ship.rect.width + 20)  # type: ignore
            ship.rect.y = self.score_rect.top  # type: ignore
            self.ships.add(ship)
