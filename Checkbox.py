import pygame

import util
from GameSettings import gameSettings
from OptionsButton import OptionsButtonType
from fonts import main_font


# button class

class Checkbox:
    def __init__(self, surface: pygame.Surface, buttonType: OptionsButtonType, clicked: bool, y: int, text: str, x: int = None, margin: int = 10):
        self.fontWidth, self.fontHeight = main_font.size(text)
        if x is None:
            x = (gameSettings.width - self.fontWidth) / 2 - margin

        self.Xmargin: int = margin
        self.Ymargin: int = margin
        self.textRect: pygame.Rect = pygame.Rect(x, y, self.fontWidth, self.fontHeight)
        self.buttonRect: pygame.Rect = pygame.Rect(self.textRect.x + self.textRect.width + 10,
                                                   y,
                                                   self.textRect.height,
                                                   self.textRect.height)

        self.clicked: bool = clicked
        self.text: str = text
        self.surface: pygame.Surface = surface
        self.buttonType: OptionsButtonType = buttonType

    def draw(self) -> None:
        # Draw button on screen
        pygame.draw.rect(self.surface, pygame.Color(255, 255, 255), self.buttonRect, 2)
        self.surface.blit(main_font.render(self.text, True, (255, 255, 255)), self.textRect)

        # Draw a cross in a checkbox
        if self.clicked:
            pygame.draw.line(self.surface, (255, 255, 255), (self.buttonRect.x + 4, self.buttonRect.y), (self.buttonRect.x + self.buttonRect.width - 4, self.buttonRect.y + self.buttonRect.height - 2), 9)
            pygame.draw.line(self.surface, (255, 255, 255), (self.buttonRect.x + self.buttonRect.width - 4, self.buttonRect.y), (self.buttonRect.x + 4, self.buttonRect.y + self.buttonRect.height - 2), 9)

    def click_handler(self, event: pygame.event.Event):
        if (event.type == pygame.MOUSEBUTTONDOWN and
            self.buttonRect.collidepoint(pygame.mouse.get_pos()) and
            pygame.mouse.get_pressed()[0] == 1):

            self.clicked = not self.clicked
            match self.buttonType:
                case OptionsButtonType.SCREEN_RESIZE:
                    gameSettings.resizableScreen = not gameSettings.resizableScreen
                    if gameSettings.fullScreen is False:
                        self.surface = pygame.display.set_mode((gameSettings.width, gameSettings.height), pygame.RESIZABLE if gameSettings.resizableScreen == True else 0)
                case OptionsButtonType.SOUND_ENABLED:
                    gameSettings.resizableScreen = not gameSettings.soundEnabled
                case OptionsButtonType.FULL_SCREEN:
                    gameSettings.fullScreen = not gameSettings.fullScreen
                    if gameSettings.fullScreen is True:
                        self.surface = pygame.display.set_mode((gameSettings.width, gameSettings.height),
                                                               pygame.FULLSCREEN if gameSettings.resizableScreen == True else 0)
                    else:
                        self.surface = pygame.display.set_mode((gameSettings.width, gameSettings.height),
                                                               pygame.RESIZABLE if gameSettings.resizableScreen == True else 0)

    def resize(self) -> None:
        util.scaleRect(self.textRect)
        util.scaleRect(self.buttonRect)
        self.buttonRect.x = self.textRect.x + self.textRect.width + 10
        # self.buttonRect.x = (gameSettings.width - self.fontWidth) / 2 - self.Xmargin
        # self.buttonRect.y = self.buttonRect.y * gameSettings.h_scale
