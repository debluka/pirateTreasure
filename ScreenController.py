import pygame

from CreditsScreen import CreditsScreen
from GameScreen import GameScreen
from GameSettings import gameSettings
from HowToPlayScreen import HowToPlayScreen
from Leaderboard import Leaderboard
from MainGame import MainGame
from MainGameState import mainGameState
from MainMenu import MainMenu
from OptionsMenu import OptionsMenu
from ScreenType import ScreenType
from WelcomeScreen import WelcomeScreen


class ScreenController:
    def __init__(self, window: pygame.Surface):
        self.window: pygame.Surface = window
        self.currentScreen: GameScreen = WelcomeScreen(window)

    def process_game_update(self) -> bool:
        quit_game: bool = False

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    return True
                case pygame.MOUSEMOTION:
                    self.currentScreen.mouse_move_handler(event.buttons, pygame.mouse.get_pos())
                case pygame.MOUSEBUTTONDOWN:
                    self.currentScreen.click_handler(event)
                case pygame.VIDEORESIZE:
                    if event.w < 750 or event.h < 750:
                        sizeTaken = 750
                    else:
                        if event.w > gameSettings.prevWidth or event.h > gameSettings.prevHeight:
                            sizeTaken = max(event.w, event.h)
                        else:
                            sizeTaken = min(event.w, event.h)
                    gameSettings.prevWidth = sizeTaken
                    gameSettings.prevHeight = sizeTaken
                    gameSettings.w_scale = sizeTaken / gameSettings.width
                    gameSettings.h_scale = sizeTaken / gameSettings.height
                    gameSettings.w_scale_base = sizeTaken / gameSettings.BASE_WIDTH
                    gameSettings.h_scale_base = sizeTaken / gameSettings.BASE_HEIGHT
                    gameSettings.width = sizeTaken
                    gameSettings.height = sizeTaken
                    gameSettings.minY *= gameSettings.w_scale
                    gameSettings.maxY *= gameSettings.w_scale
                    gameSettings.baseHeight *= gameSettings.w_scale

                    mainGameState.yOffset *= gameSettings.w_scale
                    self.window = pygame.display.set_mode((gameSettings.width, gameSettings.height), pygame.RESIZABLE)
                    self.currentScreen.window_resize_handler()
                case pygame.KEYDOWN:
                    self.currentScreen.keyboard_press_button_handler(event)

        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()

        self.currentScreen.keyboard_hold_button_handler(keys)

        if self.currentScreen.update():
            if self.currentScreen.nextScreen is None:
                return True
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
            case ScreenType.OPTIONS_MENU:
                self.currentScreen = OptionsMenu(self.window)
            case ScreenType.LEADERBOARD:
                self.currentScreen = Leaderboard(self.window)
            case ScreenType.HOW_TO_PLAY_SCREEN:
                self.currentScreen = HowToPlayScreen(self.window)
            case ScreenType.CREDITS_SCREEN:
                self.currentScreen = CreditsScreen(self.window)
