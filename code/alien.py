'''
General module with an alien implementation.
'''

import pygame as pg
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.rect import Rect


class Alien(Sprite):
    ''' Class representing an individual alien ship. '''

    __ALIENS: tuple[str, ...] = ("Spaceship_03_ORANGE.png", "Spaceship_04_ORANGE.png", "Spaceship_05_ORANGE.png")

    def __init__(self, ai_game, ship_model: int = 2) -> None:
        ''' Initialise the alien ship. '''
        super().__init__()
        self.screen_rect: Rect = ai_game.screen_rect
        self.settings = ai_game.settings

        alien_path: str = f"../assets/aliens_ships/{self.__ALIENS[ship_model-1]}"
        self.image: Surface = pg.image.load(alien_path).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        # Place the alien ship near the top-left screen edge.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x: float = float(self.rect.x)

    def check_left_right_screen_edge(self) -> bool:
        ''' 
        Returns true if the alien ship is near the left or right 
        edge of the screen; otherwise, it returns false. 
        '''
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self, *args, **kwargs) -> None:
        ''' Updates alien ship x-position by speed displacement defined in settings. '''
        self.x += self.settings.alien_ship_speed*self.settings.aliens_fleet_direction
        self.rect.x = int(self.x)


class AliensGeneral():
    ''' Class representing the alien boss ship. '''

    __BOSSES: tuple[str, ...] = ("spaceship1.png", "spaceship3.png", "spaceship55.png")

    def __init__(self, ai_game, ship_model: int = 2) -> None:
        ''' Initialise the boss ship. '''
        self.screen: Surface = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect
        self.settings = ai_game.settings

        boss_path: str = f"../assets/aliens_ships/{self.__BOSSES[ship_model-1]}"
        self.image: Surface = pg.image.load(boss_path).convert_alpha()
        self.rect: Rect = self.image.get_rect()

        # Place the boss in the centre.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.settings.screen_height // 3
        self.x: float = float(self.rect.x)

        self.life_bar_color: tuple[int, ...] = (255, 255, 255)
        self.life_bar_rect = pg.Rect(0, 0, 200, 15)
        self.life_bar_rect.centerx = self.rect.centerx
        self.life_bar_rect.y = self.rect.top - 20
        self.bar_x: float = float(self.life_bar_rect.x)

    def check_left_right_screen_edge(self) -> bool:
        ''' 
        Returns true if the alien ship is near the left or right 
        edge of the screen; otherwise, it returns false. 
        '''
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self, *args, **kwargs) -> None:
        ''' Updates alien ship x-position by speed displacement defined in settings. '''
        self.x += self.settings.aliens_general_ship_speed*self.settings.aliens_fleet_direction
        self.rect.x = int(self.x)

        self.bar_x += self.settings.aliens_general_ship_speed*self.settings.aliens_fleet_direction
        self.life_bar_rect.x = int(self.bar_x)

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
        pg.draw.rect(self.screen, self.life_bar_color, self.life_bar_rect)  # type: ignore
