import pygame

from GameSettings import gameSettings
from RebindButtonType import RebindButtonType
from fonts import main_font


# button class

class RebindButton:
    def __init__(self, surface: pygame.Surface, buttonType: RebindButtonType, y: int, text: str, x: int = None, margin: int = 10):
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
        self.buttonType: RebindButtonType = buttonType
        self.baseTextColor: (int, int, int) = (255, 255, 255)
        self.clickedTextColor: (int, int, int) = (255, 150, 255)
        self.bindingText: pygame.font.Font = pygame.font.SysFont("bahnschrift", self.buttonRect.height)

    def draw(self):
        # Draw button on screen

        pygame.draw.rect(self.surface, self.clickedTextColor if self.clicked else self.baseTextColor, self.buttonRect, 2)
        self.surface.blit(main_font.render(self.text, True, (255, 255, 255)), (self.buttonRect.center[0] - self.textRect.width / 2, self.buttonRect.center[1] - self.textRect.height / 2))
        match self.buttonType:
            case RebindButtonType.UP:
                binding: int = gameSettings.moveUpBinding
            case RebindButtonType.DOWN:
                binding: int = gameSettings.moveDownBinding
            case RebindButtonType.LEFT:
                binding: int = gameSettings.moveLeftBinding
            case RebindButtonType.RIGHT:
                binding: int = gameSettings.moveRightBinding
            case RebindButtonType.SHOOT:
                binding: int = gameSettings.shootBinding

        self.surface.blit(self.bindingText.render(pygame.key.name(binding),
                         True,
                         (255, 255, 255)),
                         (self.buttonRect.x + self.buttonRect.width + 10,
                               self.buttonRect.y))
    def click_handler(self, event: pygame.event.Event, selectedRebindButtonType: RebindButtonType) -> bool:
        self.clicked = False
        if (event.type == pygame.MOUSEBUTTONDOWN and
            self.buttonRect.collidepoint(pygame.mouse.get_pos()) and
            pygame.mouse.get_pressed()[0] == 1):
            self.clicked = not self.clicked
        return self.clicked

    def resize(self) -> None:
        self.buttonRect.x = (gameSettings.width - self.fontWidth) / 2 - self.Xmargin
        self.buttonRect.y = self.buttonRect.y * gameSettings.h_scale
