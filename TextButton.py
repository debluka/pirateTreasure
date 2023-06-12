import pygame

from fonts import main_font


# button class
class TextButton():
    def __init__(self, x: float, y: float, text: str, surface: pygame.Surface, margin=10):
        fontWidth, fontHeight = main_font.size(text)
        
        self.margin = margin
        self.buttonRect: pygame.Rect = pygame.Rect(x - self.margin,
                                                   y - self.margin,
                                                   fontWidth + self.margin * 2,
                                                   fontHeight + self.margin * 2)
        self.textRect: pygame.Rect = pygame.Rect(x, y, fontWidth, fontHeight)
        self.clicked: bool = False
        self.text: str = text
        self.surface: pygame.Surface = surface

    def draw(self):
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
        self.surface.blit(main_font.render(self.text, True, (255, 255, 255)), (self.textRect.x, self.textRect.y))

        return action