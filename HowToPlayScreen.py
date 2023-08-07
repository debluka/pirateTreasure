import pygame
from pygame import Surface

from GameScreen import GameScreen
from GameSettings import gameSettings
from ScreenType import ScreenType
from TextButton import TextButton
from fonts import main_font, title_font
from Textures import HOW_TO_PLAY
from util import scaleSurface, scaleSurfaceBase


class HowToPlayScreen(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(ScreenType(ScreenType.CREDITS_SCREEN), window)
        self.x: int = int(gameSettings.width * 0.05)
        self.y: int = int(gameSettings.height * 0.15)
        self.width: int = int(gameSettings.width * 0.9)
        self.height: int = int(gameSettings.height * 0.7)
        self.buttons: dict[str, TextButton] = {"Back": TextButton(self.window, gameSettings.height - main_font.get_height() - 20, "Back"),}
        self.imgSrc: pygame.Surface = scaleSurfaceBase(HOW_TO_PLAY)

    # Renders the main menu
    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

        for key, button in self.buttons.items():
            if button.clicked is True:
                match key:
                    case "Back":
                        self.nextScreen = ScreenType.MAIN_MENU

    def render(self) -> None:
        self.window.fill((14, 194, 249))
        creditsLabel: pygame.Surface = title_font.render("How to play", True, (250, 114, 2))
        self.window.blit(creditsLabel, (gameSettings.width / 2 - creditsLabel.get_width() / 2,
                                            gameSettings.height * 0.05,
                                            creditsLabel.get_width(),
                                            creditsLabel.get_height()))

        self.window.blit(self.imgSrc, (self.x, self.y, self.width, self.height))
        for _, button in self.buttons.items():
            button.draw()

    def window_resize_handler(self) -> None:
        for _, button in self.buttons.items():
            button.resize()

    def keyboard_press_button_handler(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.nextScreen = ScreenType.MAIN_MENU

    def window_resize_handler(self) -> None:
        for _, button in self.buttons.items():
            button.resize()

        self.x: int = int(gameSettings.width * 0.05)
        self.y: int = int(gameSettings.height * 0.15)
        self.width: int = int(gameSettings.width * 0.9)
        self.height: int = int(gameSettings.height * 0.7)

        self.imgSrc = scaleSurface(HOW_TO_PLAY, self.imgSrc)
