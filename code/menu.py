''' 
General file with menu management.
'''

import pygame.font

from button import Button


class Menu():

    def __init__(self, ai_game) -> None:
        ''' Initialize menu buttons in the game. '''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        self.play_button: Button = Button(ai_game, 'Play', -105)
        self.settings_button: Button = Button(ai_game, 'Settings', -35)
        self.help_button: Button = Button(ai_game, 'Help', 35)
        self.exit_button: Button = Button(ai_game, 'Exit', 105)

        self.easy_mode_button: Button = Button(ai_game, 'Easy Mode', -105)
        self.medium_mode_button: Button = Button(ai_game, 'Medium Mode', -35)
        self.hard_mode_button: Button = Button(ai_game, 'Hard Mode', 35)
        self.back_button: Button = Button(ai_game, 'Back', 105)

        self.game_active: bool = False
        
        self.menu_active: bool = True
        self.settings_active: bool = False
        self.help_active: bool = False

        self.easy_pressed: bool = False
        self.medium_pressed: bool = False
        self.hard_pressed: bool = False

        self.text_color: tuple[int, int, int] = (255, 255, 255)
        self.font = pygame.font.SysFont('freesansbold', 36)
        self._prep_help_window()

    def draw_menu(self) -> None:
        ''' Display the menu/settings/help on the screen. '''
        if self.menu_active is True:
            self.play_button.draw_button()
            self.settings_button.draw_button()
            self.exit_button.draw_button()
            self.help_button.draw_button()

        if self.settings_active is True:
            self.easy_mode_button.draw_button(self.easy_pressed)
            self.medium_mode_button.draw_button(self.medium_pressed)
            self.hard_mode_button.draw_button(self.hard_pressed)
            self.back_button.draw_button()

        if self.help_active is True:
            self.show_help()

    def _prep_help_window(self) -> None:
        ''' Transforms message into image. '''
        help_str: str = f'Welcome to Aliens Invasion!'
        self.help_image = self.font.render(
            help_str, True, self.text_color, self.settings.background_color)

        # Display this on the top.
        self.help_rect = self.help_image.get_rect()
        self.help_rect.centerx = self.screen_rect.centerx
        self.help_rect.centery = self.screen_rect.centery

    def show_help(self) -> None:
        ''' Display help message on the screen. '''
        self.screen.blit(self.help_image, self.help_rect)

    def check_play_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the play button is clicked by mouse. '''
        button_clicked: bool = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked is True and self.menu_active is True:
            return True
        return False

    def check_settings_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the settings button is clicked by mouse. '''
        button_clicked: bool = self.settings_button.rect.collidepoint(mouse_pos)
        if button_clicked is True and self.menu_active is True:
            return True
        return False

    def check_exit_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the exit button is clicked by mouse. '''
        button_clicked: bool = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked is True and self.menu_active is True:
            return True
        return False

    def check_help_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the help button is clicked by mouse. '''
        button_clicked: bool = self.help_button.rect.collidepoint(mouse_pos)
        if button_clicked is True and self.menu_active is True:
            return True
        return False

    def enter_settings(self) -> None:
        ''' Changes flags related to enter settings. '''
        self.menu_active = False
        self.settings_active = True

    def exit_settings(self) -> None:
        ''' Changes flags related to exit settings. '''
        self.menu_active = True
        self.settings_active = False

    def enter_help(self) -> None:
        self.menu_active = False
        self.help_active = True

    def exit_help(self) -> None:
        self.menu_active = True
        self.help_active = False

    def reset_mode_buttons(self) -> None:
        ''' Reset difficulty buttons to default. '''
        self.easy_pressed = False
        self.medium_pressed = False
        self.hard_pressed = False

    def game_mode_management(self, mouse_pos: tuple[int, int]) -> None:
        ''' Management of game difficulty mode. '''
        easy_clicked: bool = self.easy_mode_button.rect.collidepoint(mouse_pos)
        medium_clicked: bool = self.medium_mode_button.rect.collidepoint(mouse_pos)
        hard_clicked: bool = self.hard_mode_button.rect.collidepoint(mouse_pos)
        back_clicked: bool = self.back_button.rect.collidepoint(mouse_pos)

        # Check if mode has been changed, otherwise exit settings.
        self._switch_mode(easy_clicked, medium_clicked, hard_clicked)
        self._check_back_button(back_clicked)

    def _check_back_button(self, back_clicked) -> None:
        ''' Checks if the back button is clicked by mouse. '''
        if back_clicked is True:
            self.exit_settings()

    def _switch_mode(self, easy_clicked, medium_clicked, hard_clicked) -> None:
        ''' Switch difficulty button. Only one difficulty button can be clicked at a time. '''
        if easy_clicked is True and self.easy_pressed is True:
            self.easy_pressed = False
            self.settings.reset_difficulty()
        elif easy_clicked is True:
            self.settings.switch_difficulty(1)
            self.easy_pressed = True
            self.medium_pressed = self.hard_pressed = False

        if medium_clicked is True and self.medium_pressed is True:
            self.medium_pressed = False
            self.settings.reset_difficulty()
        elif medium_clicked is True:
            self.settings.switch_difficulty(2)
            self.medium_pressed = True
            self.easy_pressed = self.hard_pressed = False

        if hard_clicked is True and self.hard_pressed is True:
            self.hard_pressed = False
            self.settings.reset_difficulty()
        elif hard_clicked is True:
            self.settings.switch_difficulty(3)
            self.hard_pressed = True
            self.easy_pressed = self.medium_pressed = False
