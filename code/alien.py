"""
This module provides Alien and AliensGeneral objects.
"""

from abc import ABCMeta, abstractmethod

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Alien(Sprite, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, ai_game, img, speed) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect
        self.image: Surface = pg.image.load(img).convert_alpha()
        self.rect: Rect = self.image.get_rect()
        self.speed: float = speed
        self.x: float  # Float type for horizontal position due to more accurate tracking.

    def check_left_right_screen_edge(self) -> bool:
        """
        Returns true if the alien ship is near the left or right
        edge of the screen; otherwise, it returns false.
        """
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
        return False


class Soldier(Alien):

    __IMGS: tuple[str, ...] = ("perseus_arm_alien.png", "outer_arm_alien.png", "norma_arm_alien.png")

    def __init__(self, ai_game) -> None:
        self.settings = ai_game.settings
        ship_model: int = self.settings.alien_ship_model
        img: str = f"../assets/aliens_ships/{self.__IMGS[ship_model-1]}"
        speed: float = self.settings.alien_ship_speed
        super().__init__(ai_game, img, speed)
        self.x: float = float(self.rect.x)

    def update(self, *args, **kwargs) -> None:
        """ Updates alien ship x-position by speed displacement defined in settings. """
        self.x += self.settings.aliens_fleet_direction*self.speed
        self.rect.x = int(self.x)


class General(Alien):

    __IMGS: tuple[str, ...] = ("perseus_arm_general.png", "outer_arm_general.png", "norma_arm_general.png")

    def __init__(self, ai_game) -> None:
        self.settings = ai_game.settings
        ship_model: int = ai_game.settings.aliens_general_ship_model
        img: str = f"../assets/aliens_ships/{self.__IMGS[ship_model-1]}"
        speed: float = ai_game.settings.aliens_general_ship_speed
        super().__init__(ai_game, img, speed)

        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.settings.screen_height // 3
        self.x: float = float(self.rect.x)

        self.life_points: int = self.settings.aliens_general_life_points
        self.life_bar_color = self.settings.aliens_general_life_bar_color
        self.life_bar_outline_color = self.settings.aliens_general_life_bar_outline_color
        self.life_bar_rect: Rect = pg.Rect(0, 0, self.life_points, 15)

        # Place the life bar above the general ship.
        self.life_bar_rect.centerx = self.rect.centerx
        self.life_bar_rect.y = self.rect.top - 20

    def reset_aliens_general_ship(self) -> None:
        """ Reset aliens' general ship position and its life bar. """
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.settings.screen_height // 3
        self.x = float(self.rect.x)

        self.life_points = self.settings.aliens_general_life_points
        self.life_bar_rect.centerx = self.rect.centerx
        self.life_bar_rect.y = self.rect.top - 20

    def update(self, *args, **kwargs) -> None:
        """ Updates alien ship x-position by speed displacement defined in settings. """
        self.x += self.settings.aliens_fleet_direction*self.settings.aliens_general_ship_speed
        self.rect.x = int(self.x)

        self.life_bar_rect = pg.Rect(0, 0, self.life_points, 15)
        self.life_bar_rect.centerx = self.rect.centerx
        self.life_bar_rect.y = self.rect.top - 20

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
        pg.draw.rect(self.screen, self.life_bar_color, self.life_bar_rect)  # type: ignore
        pg.draw.rect(self.screen, self.life_bar_outline_color, self.life_bar_rect, 2)
