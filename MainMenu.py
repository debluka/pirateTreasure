import pygame
from pygame import Surface

from GameScreen import GameScreen
from ScreenType import ScreenType
from fonts import title_font
from util import WIDTH


class MainMenu(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(window)

    # Renders the main menu
    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

    def render(self):
        self.window.fill((14, 194, 249))
        title_label = title_font.render("Click to start the game", True, (255, 255, 255))
        self.window.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))

    def click_handler(self, button: int, position: tuple[int, int]):
        match button:
            case 1:
                self.nextScreen = ScreenType.MAIN_GAME
        print("Main menu click_handler")

    def mouse_move_handler(self, button: int, position: tuple[int, int]):
        print("Main menu mouse_move_handler")

    def keyboard_button_handler(self, keys: tuple[bool, ...]):
        print("Main menu keyboard_button_handler")
