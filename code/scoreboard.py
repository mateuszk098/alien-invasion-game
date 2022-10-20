'''
General file with class representing game statitstics.
'''

import pygame.font


class Scoreboard():
    ''' Class representing game statistics. '''

    def __init__(self, ai_game) -> None:
        ''' Initialize game statistics. '''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings.
        self.text_color: tuple[int, ...] = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 36)  # type: ignore

        self.prep_score()

    def prep_score(self) -> None:
        ''' Transforms punctation into image. '''
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
