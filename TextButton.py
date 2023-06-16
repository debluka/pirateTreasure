import pygame

from GameSettings import gameSettings
from fonts import main_font


# button class

class TextButton():
    def __init__(self, surface: pygame.Surface, y: int, text: str, x: int = None, margin: int = 10):
        self.fontWidth, self.fontHeight = main_font.size(text)
        if x is None:
            x = (gameSettings.width - self.fontWidth) / 2 - margin

        self.Xmargin: int = margin
        self.Ymargin: int = margin
        self.buttonRect: pygame.Rect = pygame.Rect(x - self.Xmargin,
                                                   y - self.Ymargin,
                                                   self.fontWidth + self.Xmargin * 2,
                                                   self.fontHeight + self.Ymargin * 2)
        self.textRect: pygame.Rect = pygame.Rect(x, y, self.fontWidth, self.fontHeight)

        self.clicked: bool = False
        self.text: str = text
        self.surface: pygame.Surface = surface

    def draw(self) -> bool:
        action: bool = False
        # Get mouse position
        pos: tuple[int, int] = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.buttonRect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        pygame.draw.rect(self.surface, pygame.Color(255, 255, 255), self.buttonRect, 2)
        self.surface.blit(main_font.render(self.text, True, (255, 255, 255)), (self.buttonRect.center[0] - self.textRect.width / 2, self.buttonRect.center[1] - self.textRect.height / 2))

        return action

    def resize(self) -> None:
        self.buttonRect.x = (gameSettings.width - self.fontWidth) / 2 - self.Xmargin
        self.buttonRect.y = self.buttonRect.y * gameSettings.h_scale
