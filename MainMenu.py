import pygame
from pygame import Surface

from GameScreen import GameScreen
from GameSettings import gameSettings
from ScreenType import ScreenType
from TextButton import TextButton
from fonts import main_font, title_font


class MainMenu(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(ScreenType(ScreenType.MAIN_MENU), window)
        TOP_OFFSET: int = int(270 * gameSettings.h_scale_base)
        BUTTON_SPACING: int = int(60 * gameSettings.h_scale_base)
        self.buttons: dict[str, TextButton] = {"Start game": TextButton(self. window, TOP_OFFSET, "Start game"),
                                               "Leaderboard": TextButton(self.window, TOP_OFFSET + BUTTON_SPACING, "Leaderboard"),
                                               "Options": TextButton(self.window, TOP_OFFSET + BUTTON_SPACING * 2, "Options"),
                                               "Credits": TextButton(self.window, gameSettings.height - main_font.get_height() - 20, "Credits", 20),
                                               "How to play": TextButton(self.window, gameSettings.height - main_font.get_height() - 20, "How to play", gameSettings.width - main_font.size("How to play")[0] - 20),
                                               "Exit": TextButton(self.window, TOP_OFFSET + BUTTON_SPACING * 3, "Exit")}
        if pygame.mixer.music.get_busy() is False:
            pygame.mixer.music.load('assets/audio/mainTheme.mp3')
            pygame.mixer.music.play(-1)

    # Renders the main menu
    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

        for key, button in self.buttons.items():
            if button.clicked is True:
                match key:
                    case "Start game":
                        self.nextScreen = ScreenType.MAIN_GAME
                        pygame.mixer.music.stop()
                    case "Leaderboard":
                        self.nextScreen = ScreenType.LEADERBOARD
                    case "Options":
                        self.nextScreen = ScreenType.OPTIONS_MENU
                    case "Credits":
                        self.nextScreen = ScreenType.CREDITS_SCREEN
                    case "How to play":
                        self.nextScreen = ScreenType.HOW_TO_PLAY_SCREEN
                    case "Exit":
                        return True

    def render(self) -> None:
        self.window.fill((14, 194, 249))

        titleLabel: pygame.Surface = title_font.render("Pirate's Treasure", True, (200, 11, 11))
        self.window.blit(titleLabel, (gameSettings.width / 2 - titleLabel.get_width() / 2,
                                        gameSettings.height * 0.05,
                                        titleLabel.get_width(),
                                        titleLabel.get_height()))

        for _, button in self.buttons.items():
            button.draw()

    def window_resize_handler(self) -> None:
        for _, button in self.buttons.items():
            button.resize()

    def click_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            for _, button in self.buttons.items():
                if button.buttonRect.collidepoint(event.pos):
                    button.clicked = True
