"""
This module provides a Menu object, which provides an interactive GUI.
"""

import textwrap

import pygame as pg
from pygame.surface import Surface
from pygame.rect import Rect

from button import Button


class Menu():
    """Menu object provides an interactive GUI with buttons used for gameplay manipulation."""

    __GAME_TITLE_TEXT: str = "Alien Invasion!"
    __PAUSE_TEXT: str = "PAUSE"
    __HELP_TEXT: str = "Welcome to Alien Invasion! The Milky Way has been attacked by "\
        "hostile creatures. You have been chosen by the Starfleet general to be the "\
        "captain of the 'Eagle 2' spaceship. The Eagle 2 is the best spaceship of Starfleet "\
        "and one of the engineering miracles. The Eagle 2 has a modern guidance system and "\
        "hypersonic missiles, which should help shoot aliens down. You cannot allow aliens "\
        "to arrive on Earth! We believe in You. Press 'Esc' to return to the control centre. "\
        "Press 'g' or click 'Play' to go on the mission. Press 'r' during the mission to return "\
        "to the base. Press 's' or click 'Settings' to travel to a more dangerous part of the "\
        "galaxy. Press '1', '2' or '3' being in settings to choose your mission or click "\
        "appropriate option. Press 'p' to pause the current mission. Press 'q' or click "\
        "'Exit' to give up."
    __GAME_COMPLETION_TEXT: str = "Congratulations! You've defeated the alien general "\
        "and saved Earth against alien invasion! The Starfleet general awarded you with "\
        "the medal of courage, and the president honoured you as a hero of the nation. "\
        "Press 'Esc' to return on Earth. "

    def __init__(self, ai_game) -> None:
        """Initialise Menu object."""
        self.screen: Surface = ai_game.screen
        self.screen_rect = ai_game.screen_rect
        self.settings = ai_game.settings

        # Buttons in the menu section.
        self.play_button: Button = Button(ai_game, "Play", offset=-105)
        self.settings_button: Button = Button(ai_game, "Settings", offset=-35)
        self.help_button: Button = Button(ai_game, "Help", offset=35)
        self.exit_button: Button = Button(ai_game, "Exit", offset=105)

        # Buttons in the settings section.
        self.easy_mode_button: Button = Button(ai_game, "Perseus Arm", offset=-105)
        self.medium_mode_button: Button = Button(ai_game, "Outer Arm", offset=-35)
        self.hard_mode_button: Button = Button(ai_game, "Norma Arm", offset=35)
        self.back_button: Button = Button(ai_game, "Back", offset=105)

        # For the tracking active menu section and which buttons can be currently pressed.
        self.menu_is_active: bool = True
        self.settings_is_active: bool = False
        self.help_is_active: bool = False

        # For tracking changes in game difficulty mode and the highlight of buttons.
        self.easy_btn_pressed: bool = False
        self.medium_btn_pressed: bool = False
        self.hard_btn_pressed: bool = False

        # For getting text to draw in the `draw_message` method.
        self.messages_to_draw: dict[str, str] = {
            "Title": self.__GAME_TITLE_TEXT,
            "Pause": self.__PAUSE_TEXT,
            "Help": self.__HELP_TEXT,
            "Congratulations": self.__GAME_COMPLETION_TEXT
        }

    def draw_menu(self) -> None:
        """Displays the current menu state (Menu, Settings or Help)."""
        if self.menu_is_active:
            self.draw_message("Title", fontsize=128, ypos=150)
            self.play_button.draw()
            self.settings_button.draw()
            self.exit_button.draw()
            self.help_button.draw()
        elif self.settings_is_active:
            self.easy_mode_button.draw(self.easy_btn_pressed)
            self.medium_mode_button.draw(self.medium_btn_pressed)
            self.hard_mode_button.draw(self.hard_btn_pressed)
            self.back_button.draw()
        elif self.help_is_active:
            self.draw_message("Help", ypos=150)

    def draw_message(self, message_key: str, **kwargs) -> None:
        """ 
        Draws one-line or multiline message on the screen. 

        Parameters
        ----------
        text_key : `str`
            "Title", "Pause", "Help", "Congratulations" - the key of the message to draw.
        **kwargs : `dict`, `optional`
            max_width : `int`, default=60
                Maximum length of the text line.
            vertical_offset: `int`, default=42
                Vertical offset between subsequent text lines.
            text_color : `pygame.Color`, default=pygame.Color("#f0f0f0")
            fontsize : `int`, default=42
            ypos : `int`
                Initial vertical position of the first text line.
        """

        text: str = self.messages_to_draw.get(message_key, "There is no such key.")
        max_width: int = kwargs.get("max_width", 60)
        text_lines: list[str] = textwrap.wrap(text, max_width)
        vertical_offset: int = kwargs.get("vertical_offset", 42)

        text_color = kwargs.get("color", self.settings.text_color)
        background = self.settings.background_color
        fontsize: int = kwargs.get("fontsize", 42)
        font = pg.font.SysFont("freesansbold", fontsize)

        for line_number, text_line in enumerate(text_lines):
            line_img: Surface = font.render(text_line, True, text_color, background)
            line_rect: Rect = line_img.get_rect()
            line_rect.center = self.screen_rect.center
            if "ypos" in kwargs:
                line_rect.y = kwargs["ypos"] + line_number*vertical_offset
            self.screen.blit(line_img, line_rect)

    def check_button_press(self, mouse_pos: tuple[int, int], btn_key: str) -> bool:
        """
        Checks if the mouse presses the given button. Return True if yes, otherwise return False.

        Parameters
        ----------
        mouse_pos : `tuple[int, int]`
            The position of the mouse - pygame.mouse.get_pos().
        btn_key : `str`
            "Play", "Settings", "Easy Mode", "Medium Mode", "Hard Mode", "Back", "Help", "Exit Game".
        """
        buttons: dict[str, tuple[Button, bool]] = {
            "Play": (self.play_button, self.menu_is_active),
            "Settings": (self.settings_button, self.menu_is_active),
            "Easy Mode": (self.easy_mode_button, self.settings_is_active),
            "Medium Mode": (self.medium_mode_button, self.settings_is_active),
            "Hard Mode": (self.hard_mode_button, self.settings_is_active),
            "Back": (self.back_button, self.settings_is_active),
            "Help": (self.help_button, self.menu_is_active),
            "Exit Game": (self.exit_button, self.menu_is_active)
        }

        button: Button
        related_menu_state: bool  # The press possibility is related to the active menu section.
        button, related_menu_state = buttons[btn_key]
        pressed: bool = button.rect.collidepoint(mouse_pos)

        if pressed and related_menu_state:
            return True
        return False

    def show_settings(self) -> None:
        """Changes activity of Settings section to True. Menu and Help to False."""
        self.menu_is_active = False
        self.settings_is_active = True
        self.help_is_active = False

    def show_help(self) -> None:
        """Changes activity of Help section to True. Menu and Settings to False."""
        self.menu_is_active = False
        self.settings_is_active = False
        self.help_is_active = True

    def return_to_menu(self) -> None:
        """Changes activity of Menu section to True. Settings and Help to False."""
        self.menu_is_active = True
        self.settings_is_active = False
        self.help_is_active = False

    def switch_to_easy_mode(self) -> None:
        """
        Switches game difficulty mode to easy if the button is pressed,
        otherwise, switches to medium mode if released.
        """
        if self.easy_btn_pressed and self.settings_is_active:
            self.easy_btn_pressed = False
            self.settings.reset_difficulty()
        elif self.settings_is_active:
            self.settings.switch_difficulty(1)
            self.easy_btn_pressed = True
            self.medium_btn_pressed = self.hard_btn_pressed = False

    def switch_to_medium_mode(self) -> None:
        """
        Switches game difficulty mode to medium if the button is pressed,
        otherwise, switches to medium mode if released.
        """
        if self.medium_btn_pressed and self.settings_is_active:
            self.medium_btn_pressed = False
            self.settings.reset_difficulty()
        elif self.settings_is_active:
            self.settings.switch_difficulty(2)
            self.medium_btn_pressed = True
            self.easy_btn_pressed = self.hard_btn_pressed = False

    def switch_to_hard_mode(self) -> None:
        """
        Switches game difficulty mode to hard if the button is pressed,
        otherwise, switches to medium mode if released.
        """
        if self.hard_btn_pressed and self.settings_is_active:
            self.hard_btn_pressed = False
            self.settings.reset_difficulty()
        elif self.settings_is_active:
            self.settings.switch_difficulty(3)
            self.hard_btn_pressed = True
            self.easy_btn_pressed = self.medium_btn_pressed = False
