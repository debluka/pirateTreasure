import pygame

from ScreenType import ScreenType


class GameScreen():
    def __init__(self, window):
        self.window: pygame.Surface = window
        self.nextScreen: ScreenType | None = None

    def update(self):
        pass

    def render(self):
        pass

    def click_handler(self, button: int, position: tuple[int, int]):
        pass

    def mouse_move_handler(self, button: int, position: tuple[int, int]):
        pass

    def keyboard_button_handler(self, keys: tuple[bool, ...]):
        pass

