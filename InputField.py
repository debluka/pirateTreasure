import pygame

from GameSettings import gameSettings
from fonts import title_font

COLOR_INACTIVE = (255, 255, 255)
COLOR_ACTIVE = (0, 255, 0)

class InputField:
    def __init__(self, window: pygame.Surface, x: int, y: int, w: int, h: int, text: str = ''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = title_font.render(text, True, self.color)
        self.window = window
        self.active = False

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pygame.KEYDOWN and event.key:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = title_font.render(self.text, True, COLOR_INACTIVE)

    def draw(self):
        self.window.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(self.window, self.color, self.rect, 2)

    def resize(self):
        self.rect.x = self.rect.x * gameSettings.w_scale
        self.rect.y = self.rect.y * gameSettings.h_scale

        self.rect.w = self.rect.w * gameSettings.w_scale
