import pygame.event
from pygame import Surface

from GameScreen import GameScreen
from GameSettings import gameSettings
from InputField import InputField
from ScreenType import ScreenType
from TextButton import TextButton
from fonts import title_font, main_font


class WelcomeScreen(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(ScreenType(ScreenType.WELCOME_SCREEN), window)
        self.welcomeText = "Please click the input and enter your name for the leaderboard"
        self.nameInput = InputField(self.window,
                                    int(gameSettings.width * 0.1),
                                    int(gameSettings.height * 0.4),
                                    int(gameSettings.width * 0.8),
                                    title_font.get_height() + 10)

    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

    def render(self) -> None:
        self.window.fill((14, 194, 249))

        welcomeTextSurface = main_font.render(self.welcomeText, True, (255, 255, 255))
        self.window.blit(welcomeTextSurface, (int(gameSettings.width / 2 - main_font.size(self.welcomeText)[0] / 2),
                                              int(gameSettings.height * 0.3),
                                              welcomeTextSurface.get_width(),
                                              welcomeTextSurface.get_height()))

        self.nameInput.draw()

    def click_handler(self, event: pygame.event.Event) -> None:
        self.nameInput.event_handler(event)

    def keyboard_press_button_handler(self, event: pygame.event.Event) -> None:
        match event.key:
            case pygame.K_RETURN:
                if len(self.nameInput.text) > 0:
                    self.nextScreen = ScreenType.MAIN_MENU
                    gameSettings.username = self.nameInput.text
            case _:
                if len(self.nameInput.text) < 20:
                    self.nameInput.event_handler(event)

    def window_resize_handler(self) -> None:
        self.nameInput.resize()
