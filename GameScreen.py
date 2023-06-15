import pygame

from ScreenType import ScreenType


class GameScreen():
    def __init__(self, screenType: ScreenType, window: pygame.Surface):
        self.window: pygame.Surface = window
        self.screenType: ScreenType = screenType
        self.nextScreen: ScreenType | None = None

    def update(self):
        pass

    def render(self):
        pass

    def click_handler(self, button: int, position: tuple[int, int]):
        pass

    def mouse_move_handler(self, button: int, position: tuple[int, int]):
        pass

    def keyboard_hold_button_handler(self, keys: tuple[bool, ...]):
        pass

    def keyboard_press_button_handler(self, key: int):
        pass

    def window_resize_handler(self):
        pass