''' 
General file with menu management.
'''

import textwrap

import pygame.font
from pygame.surface import Surface
from pygame.rect import Rect

from button import Button


class Menu():

    def __init__(self, ai_game) -> None:
        ''' Initialize menu buttons in the game. '''
        self.screen: Surface = ai_game.screen
        self.screen_rect: Rect = ai_game.screen_rect
        self.settings = ai_game.settings

        self.play_button: Button = Button(ai_game, 'Play', -105)
        self.settings_button: Button = Button(ai_game, 'Settings', -35)
        self.help_button: Button = Button(ai_game, 'Help', 35)
        self.exit_button: Button = Button(ai_game, 'Exit', 105)

        self.easy_mode_button: Button = Button(ai_game, 'Perseus Arm', -105)
        self.medium_mode_button: Button = Button(ai_game, 'Outer Arm', -35)
        self.hard_mode_button: Button = Button(ai_game, 'Norma Arm', 35)
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
        self.title_font = pygame.font.SysFont('freesansbols', 72)

    def draw_menu(self) -> None:
        ''' Display the menu/settings/help on the screen. '''
        if self.menu_active is True:
            self.show_title()
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

    def show_title(self) -> None:
        ''' Displays the game title on the screen. '''
        title: str = 'Aliens Invasion!'
        title_img: Surface = self.title_font.render(
            title, True, self.text_color, self.settings.background_color)
        title_rect: Rect = title_img.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.y = 100
        self.screen.blit(title_img, title_rect)

    def show_help(self, text_vertical_offset: int = 36) -> None:
        ''' Displays the help message on the screen. '''
        help_text: str = 'Welcome to Aliens Invasion! The Milky Way has been attacked by '\
            'hostile creatures. You have been chosen by the Starfleet general to be the '\
            'captain of the "Eagle 2" spaceship. The Eagle 2 is the best spaceship of Starfleet '\
            'and one of the engineering miracles. The Eagle 2 has a modern guidance system and '\
            'hypersonic missiles, which should help shoot aliens down. You cannot allow '\
            'aliens to arrive on Earth. We believe in You. Press "Esc" to return to the control '\
            'centre. Press "g" or click "Play" to go on the mission. Press "r" during the mission '\
            'to return to the base. Click "Settings" to travel to a more dangerous part of the '\
            'galaxy. Press "q" or click "Exit" to give up.'
        text_lines: list[str] = textwrap.wrap(help_text, 50)

        for line_number, text_line in enumerate(text_lines):
            cent: Surface = self.font.render(
                text_line, True, self.text_color, self.settings.background_color)
            cent_rect: Rect = cent.get_rect()
            cent_rect.centerx = self.screen_rect.centerx
            cent_rect.y = 60 + line_number*text_vertical_offset
            self.screen.blit(cent, cent_rect)

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

    def _check_back_button(self, back_clicked) -> None:
        ''' Checks if the back button is clicked by mouse. '''
        if back_clicked is True:
            self.exit_settings()
