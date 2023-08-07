import pygame
from pygame import Surface

from GameScreen import GameScreen
from GameSettings import gameSettings
from ScreenType import ScreenType
from TextButton import TextButton
from fonts import main_font, title_font


class CreditsScreen(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(ScreenType(ScreenType.CREDITS_SCREEN), window)
        self.buttons: dict[str, TextButton] = {"Back": TextButton(self.window, gameSettings.height - main_font.get_height() - 20, "Back"),}
        self.credits: [str] = ["Sounds: https://pixabay.com/",
                               " ",
                               " ",
                               "Game assets: https://www.kenney.nl/assets/pirate-pack",
                               "         and own drawings                        "]

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
        creditsLabel: pygame.Surface = title_font.render("Credits", True, (218, 237, 9))
        self.window.blit(creditsLabel, (gameSettings.width / 2 - creditsLabel.get_width() / 2,
                                            gameSettings.height * 0.05,
                                            creditsLabel.get_width(),
                                            creditsLabel.get_height()))

        offset: int = int(gameSettings.height * 0.3)
        for text in self.credits:
            textLabel: pygame.Surface = main_font.render(text, True, (255, 255, 255))
            self.window.blit(textLabel, (gameSettings.width / 2 - textLabel.get_width() / 2,
                                            offset,
                                            textLabel.get_width(),
                                            textLabel.get_height()))
            offset += main_font.get_height() + 10
        for _, button in self.buttons.items():
            button.draw()

    def window_resize_handler(self) -> None:
        for _, button in self.buttons.items():
            button.resize()

    def keyboard_press_button_handler(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.nextScreen = ScreenType.MAIN_MENU
