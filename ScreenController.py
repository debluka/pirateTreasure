import pygame

from GameScreen import GameScreen
from MainGame import MainGame
from MainMenu import MainMenu
from ScreenType import ScreenType


class ScreenController:
    def __init__(self, window: pygame.Surface):
        self.window = window
        self.currentScreen: GameScreen = MainMenu(window)

    def process_game_update(self):
        quit_game = False

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return True
                case pygame.MOUSEMOTION:
                    self.currentScreen.mouse_move_handler(event.buttons, pygame.mouse.get_pos())
                case pygame.MOUSEBUTTONDOWN:
                    self.currentScreen.click_handler(event.button, pygame.mouse.get_pos())

        keys = pygame.key.get_pressed()
        self.currentScreen.keyboard_button_handler(keys)

        if self.currentScreen.update():
            self.switch_screen()
            return False

        self.currentScreen.render()

        return quit_game

    def switch_screen(self) -> None:
        match self.currentScreen.nextScreen:
            case None:
                return
            case ScreenType.MAIN_MENU:
                self.currentScreen = MainMenu(self.window)
            case ScreenType.MAIN_GAME:
                self.currentScreen = MainGame(self.window)
