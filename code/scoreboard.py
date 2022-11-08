"""
This module provides displaying a current level, score, best score
and remaining player's ships.
"""

import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect

from spaceship import Spaceship


class Scoreboard():
    """Scoreboard object is responsible for displaying game statistics."""

    def __init__(self, ai_game) -> None:
        """Initialize scoreboard."""
        self.ai_game = ai_game
        self.screen: Surface = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.text_font = pg.font.SysFont("freesansbold", 48)

        self.prepare_current_score()
        self.prepare_highest_score()
        self.prepare_current_level()
        self.prepare_remaining_player_ships()

    def prepare_current_score(self) -> None:
        """Transforms a current score into an image placed in the top-right corner."""
        # Comma is important, it separates the score if it's higher than 1000.
        text: str = f"Score: {self.stats.current_score:,}"
        color = self.settings.text_color
        background = self.settings.background_color

        self.current_score_img: Surface = self.text_font.render(text, True, color, background)
        self.current_score_rect: Rect = self.current_score_img.get_rect()
        self.current_score_rect.right = self.screen_rect.right - 20
        self.current_score_rect.top = 20

    def prepare_highest_score(self) -> None:
        """Transforms the best score into an image placed in the top-centre edge."""
        text: str = f"Best Score: {self.stats.highest_score:,}"
        color = self.settings.text_color
        background = self.settings.background_color

        self.highest_score_img: Surface = self.text_font.render(text, True, color, background)
        self.highest_score_rect: Rect = self.highest_score_img.get_rect()
        self.highest_score_rect.centerx = self.screen_rect.centerx
        self.highest_score_rect.top = self.current_score_rect.top

    def prepare_current_level(self) -> None:
        """ 
        Transforms a current score into an image placed in the top-right corner
        under the current score. 
        """
        text: str = f"Level: {self.stats.current_level}"
        color = self.settings.text_color
        background = self.settings.background_color

        self.current_level_img: Surface = self.text_font.render(text, True, color, background)
        self.current_level_rect: Rect = self.current_level_img.get_rect()
        self.current_level_rect.right = self.current_score_rect.right
        self.current_level_rect.top = self.current_score_rect.bottom + 10

    def prepare_remaining_player_ships(self) -> None:
        """ 
        Create a group of ships which compose the remaining lives. 
        Placed them in the top-left corner of the screen.
        """
        self.remaining_player_ships = pg.sprite.Group()
        for ship_number in range(self.stats.remaining_player_ships):
            ship = Spaceship(self.ai_game, resized=True)
            ship.rect.x = self.screen_rect.left + 20 + ship_number*(ship.rect.width + 20)
            ship.rect.y = self.current_score_rect.top
            self.remaining_player_ships.add(ship)

    def check_the_highest_score(self) -> None:
        """
        Checks if, in the current game, we have the best score.
        Updates the best score if the condition is met.
        """
        if self.stats.current_score > self.stats.highest_score:
            self.stats.highest_score = self.stats.current_score
            self.prepare_highest_score()

    def show_scoreboard_and_stats(self) -> None:
        """Draws current score, level, the best score and remaining lives on the screen."""
        self.screen.blit(self.current_score_img, self.current_score_rect)
        self.screen.blit(self.highest_score_img, self.highest_score_rect)
        self.screen.blit(self.current_level_img, self.current_level_rect)
        self.remaining_player_ships.draw(self.screen)
