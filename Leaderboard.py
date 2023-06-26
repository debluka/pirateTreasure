import pygame

from GameScreen import GameScreen
from GameSettings import gameSettings
from ScreenType import ScreenType
from util import scaleRect
from fonts import main_font
from dbModifyScores import getHighscores


class Leaderboard(GameScreen):
    def __init__(self, window: pygame.Surface):
        super().__init__(ScreenType(ScreenType.LEADERBOARD), window)
        self.x: int = int(gameSettings.width * 0.05)
        self.y: int = int(gameSettings.height * 0.15)
        self.width: int = int(gameSettings.width * 0.9)
        self.height: int = int(gameSettings.height * 0.8)
        self.leaderboardRect: pygame.Rect = pygame.Rect((self.x, self.y, self.width, self.height))
        self.highscores: dict[str, int] = getHighscores()

    # Renders the main menu
    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

    def render(self) -> None:
        self.window.fill((14, 194, 249))
        leaderboardLabel: pygame.Surface = main_font.render("Leaderboard", True, (255, 255, 255))
        self.window.blit(leaderboardLabel, (self.leaderboardRect.center[0] - leaderboardLabel.get_width() / 2,
                                            gameSettings.height * 0.05,
                                            leaderboardLabel.get_width(),
                                            leaderboardLabel.get_height()))
        pygame.draw.rect(self.window, (255, 255, 255), self.leaderboardRect, 2)

        position: int = 1
        for name, score in self.highscores.items():
            highscoreLabel: pygame.Surface = main_font.render(f"{position}. {name}: {score}", True, (255, 255, 255))
            self.window.blit(highscoreLabel, (self.leaderboardRect.center[0] - highscoreLabel.get_width() / 2,
                                              self.leaderboardRect.y + (self.leaderboardRect.height * (position - 1)) / 10 + self.leaderboardRect.height * 0.02,
                                              highscoreLabel.get_width(),
                                              highscoreLabel.get_height()))
            position += 1
            if position > 10:
                break

    def keyboard_press_button_handler(self, event: pygame.event.Event) -> None:
        match event.key:
            case pygame.K_ESCAPE:
                self.nextScreen = ScreenType.MAIN_MENU

    def window_resize_handler(self) -> None:
        scaleRect(self.leaderboardRect)
