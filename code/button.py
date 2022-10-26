'''
General module with a menu's button implementation.
'''

import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect


class Button():
    ''' Class representing menu's button. '''

    def __init__(self, ai_game, msg: str, offset: int = 0) -> None:
        ''' Initialize default button properties. Offset = 0 means centre of the screen height. '''
        self.screen: Surface = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect

        self.width: int = 250
        self.height: int = 50
        self.released_color = pg.Color(0, 255, 0)
        self.pressed_color = pg.Color(0, 60, 0)
        self.text_color = pg.Color(255, 255, 255)
        self.font = pg.font.SysFont('freesansbold', 48)

        self.rect: Rect = pg.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += offset

        # Puts message on the rect and centres the message.
        self.msg_image: Surface = self.font.render(msg, True, self.text_color)
        self.msg_image_rect: Rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self, is_pressed=False) -> None:
        ''' Draws a button rect with the message on the screen. '''
        current_color = self.released_color
        if is_pressed is True:
            current_color = self.pressed_color

        self.screen.fill(current_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
