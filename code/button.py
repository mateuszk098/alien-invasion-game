'''
File with class representing game button.
'''

import pygame
import pygame.font


class Button():
    ''' Class representing menu button. '''

    def __init__(self, ai_game, msg: str, offset: int = 0) -> None:
        ''' Initialize default button properties.'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self.width: int = 250
        self.height: int = 50
        self.button_color: tuple[int, ...] = (0, 255, 0)
        self.button_color_clicked: tuple[int, ...] = (0, 60, 0)
        self.text_color: tuple[int, int, int] = (255, 255, 255)
        self.font = pygame.font.SysFont('freesansbold', 48)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += offset

        self._prep_msg(msg)

    def draw_button(self, is_clicked=False) -> None:
        ''' Draws button rect with message on the screen. '''
        color: tuple[int, ...] = self.button_color

        if is_clicked is True:
            color = self.button_color_clicked

        self.screen.fill(color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def _prep_msg(self, msg) -> None:
        ''' Puts message on the rect and center the message. '''
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
