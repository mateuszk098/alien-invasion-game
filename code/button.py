'''
File with class representing game button.
'''

import pygame.font
from pygame.rect import Rect


class Button():
    def __init__(self, ai_game, msg, offset=0) -> None:
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 250, 50
        self.button_color = (0, 255, 0)
        self.button_color_clicked = (0, 60, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # type: ignore

        self.rect = pygame.Rect(0, 0, self.width, self.height)  # type: ignore
        self.rect.center = self.screen_rect.center
        self.rect.y += offset

        self.msg = msg
        self._prep_msg(msg, self.button_color)

    def draw_button(self, is_clicked=False) -> None:
        if not is_clicked:
            self.screen.fill(self.button_color, self.rect)
            self._prep_msg(self.msg, self.button_color)
        else:
            self.screen.fill(self.button_color_clicked, self.rect)
            self._prep_msg(self.msg, self.button_color_clicked)

        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _prep_msg(self, msg, color) -> None:
        ''' Puts message on the rect and center the message. '''
        self.msg_image = self.font.render(msg, True, self.text_color, color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
