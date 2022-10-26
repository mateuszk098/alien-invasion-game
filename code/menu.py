''' 
General module with menu management implementation.
'''

import textwrap

import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect

from button import Button


class Menu():

    __GAME_TITLE_TEXT: str = 'Aliens Invasion!'
    __HELP_TEXT: str = 'Welcome to Aliens Invasion! The Milky Way has been attacked by '\
        'hostile creatures. You have been chosen by the Starfleet general to be the '\
        'captain of the "Eagle 2" spaceship. The Eagle 2 is the best spaceship of Starfleet '\
        'and one of the engineering miracles. The Eagle 2 has a modern guidance system and '\
        'hypersonic missiles, which should help shoot aliens down. You cannot allow '\
        'aliens to arrive on Earth. We believe in You. Press "Esc" to return to the control '\
        'centre. Press "g" or click "Play" to go on the mission. Press "r" during the mission '\
        'to return to the base. Click "Settings" to travel to a more dangerous part of the '\
        'galaxy. Press "q" or click "Exit" to give up.'

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

        self.easy_btn_pressed: bool = False
        self.medium_btn_pressed: bool = False
        self.hard_btn_pressed: bool = False

        self.help_text_color = pg.Color(255, 255, 255)
        self.help_text_font = pg.font.SysFont('freesansbold', 36)

        self.game_title_color = pg.Color(255, 255, 255)
        self.game_title_font = pg.font.SysFont('freesansbols', 72)

    def draw_menu(self) -> None:
        ''' Draws the current menu state on the screen. '''
        if self.menu_active is True:
            self.draw_title()
            self.play_button.draw_button()
            self.settings_button.draw_button()
            self.exit_button.draw_button()
            self.help_button.draw_button()

        if self.settings_active is True:
            self.easy_mode_button.draw_button(self.easy_btn_pressed)
            self.medium_mode_button.draw_button(self.medium_btn_pressed)
            self.hard_mode_button.draw_button(self.hard_btn_pressed)
            self.back_button.draw_button()

        if self.help_active is True:
            self.draw_help()

    def draw_title(self) -> None:
        ''' Displays the game title on the screen. '''
        text: str = self.__GAME_TITLE_TEXT
        color = self.game_title_color
        background = self.settings.background_color

        title_img = self.game_title_font.render(text, True, color, background)
        title_rect = title_img.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.y = 100

        self.screen.blit(title_img, title_rect)

    def draw_help(self, text_vertical_offset: int = 36) -> None:
        ''' Displays the help message on the screen. '''
        text: str = self.__HELP_TEXT
        color = self.help_text_color
        background = self.settings.background_color

        text_lines: list[str] = textwrap.wrap(text, 50)

        for line_number, text_line in enumerate(text_lines):
            line_img = self.help_text_font.render(text_line, True, color, background)
            line_rect = line_img.get_rect()
            line_rect.centerx = self.screen_rect.centerx
            line_rect.y = 60 + line_number*text_vertical_offset

            self.screen.blit(line_img, line_rect)

    def check_play_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the play button is pressed by mouse. '''
        button_pressed: bool = self.play_button.rect.collidepoint(mouse_pos)
        if button_pressed is True and self.menu_active is True:
            return True
        return False

    def check_settings_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the settings button is pressed by mouse. '''
        button_pressed: bool = self.settings_button.rect.collidepoint(mouse_pos)
        if button_pressed is True and self.menu_active is True:
            return True
        return False

    def check_exit_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the exit button is pressed by mouse. '''
        button_pressed: bool = self.exit_button.rect.collidepoint(mouse_pos)
        if button_pressed is True and self.menu_active is True:
            return True
        return False

    def check_help_button(self, mouse_pos: tuple[int, int]) -> bool:
        ''' Checks if the help button is pressed by mouse. '''
        button_pressed: bool = self.help_button.rect.collidepoint(mouse_pos)
        if button_pressed is True and self.menu_active is True:
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
        ''' Changes flags related to enter help. '''
        self.menu_active = False
        self.help_active = True

    def exit_help(self) -> None:
        ''' Changes flags related to exit help. '''
        self.menu_active = True
        self.help_active = False

    def game_mode_management(self, mouse_pos: tuple[int, int]) -> None:
        ''' 
        Checks if any button in the setting is pressed or released 
        and switches game difficulty mode. 
        '''
        easy_btn_pressed: bool = self.easy_mode_button.rect.collidepoint(mouse_pos)
        medium_btn_pressed: bool = self.medium_mode_button.rect.collidepoint(mouse_pos)
        hard_btn_pressed: bool = self.hard_mode_button.rect.collidepoint(mouse_pos)
        back_btn_pressed: bool = self.back_button.rect.collidepoint(mouse_pos)

        # Check if game mode has been changed, otherwise exit settings.
        self._switch_game_mode(easy_btn_pressed, medium_btn_pressed, hard_btn_pressed)
        self._check_exit_from_settings(back_btn_pressed)

    def _switch_game_mode(self, easy_btn_pressed, medium_btn_pressed, hard_btn_pressed) -> None:
        ''' Switch difficulty button. Only one difficulty button can be pressed at a time. '''
        if easy_btn_pressed is True and self.easy_btn_pressed is True:
            self.easy_btn_pressed = False
            self.settings.reset_difficulty()
        elif easy_btn_pressed is True:
            self.settings.switch_difficulty(1)
            self.easy_btn_pressed = True
            self.medium_btn_pressed = self.hard_btn_pressed = False

        if medium_btn_pressed is True and self.medium_btn_pressed is True:
            self.medium_btn_pressed = False
            self.settings.reset_difficulty()
        elif medium_btn_pressed is True:
            self.settings.switch_difficulty(2)
            self.medium_btn_pressed = True
            self.easy_btn_pressed = self.hard_btn_pressed = False

        if hard_btn_pressed is True and self.hard_btn_pressed is True:
            self.hard_btn_pressed = False
            self.settings.reset_difficulty()
        elif hard_btn_pressed is True:
            self.settings.switch_difficulty(3)
            self.hard_btn_pressed = True
            self.easy_btn_pressed = self.medium_btn_pressed = False

    def _check_exit_from_settings(self, back_pressed) -> None:
        ''' Exits from settings if the back button is pressed by the mouse. '''
        if back_pressed is True:
            self.exit_settings()
