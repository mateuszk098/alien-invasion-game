'''
File with class representing game button.
'''

import pygame.font
from pygame.rect import Rect


class Button():
    def __init__(self, ai_game, msg) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # type: ignore

        self.rect = pygame.Rect(0, 0, self.width, self.height)  # type: ignore
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def draw_button(self) -> None:
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _prep_msg(self, msg) -> None:
        ''' Puts message on the rect and center the message. '''
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
