import pygame


# button class
class Button:
    def __init__(self, x: int, y: int, image: pygame.Surface, scale: float):
        width: int = image.get_width()
        height: int = image.get_height()
        self.image: pygame.Surface = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked: bool = False

    def draw(self, surface) -> bool:
        action: bool = False
        # Get mouse position
        pos: tuple[int, int] = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked :
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
