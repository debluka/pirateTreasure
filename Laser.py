import pygame

from GameSettings import gameSettings
from util import collide, scaleSurface, scaleSurfaceBase


class Laser:
    def __init__(self, x: int, y: int, img: pygame.Surface, y_velocity: float, x_velocity: float = 0):
        self.x: int = x
        self.y: int = y
        self.img: pygame.Surface = scaleSurfaceBase(img)
        self.imgSrc: pygame.Surface = img
        self.mask: pygame.Mask = pygame.mask.from_surface(self.img)
        self.y_velocity: float = y_velocity * gameSettings.h_scale_base
        self.x_velocity: float = x_velocity * gameSettings.h_scale_base
        self.isSlowed: bool = False
        self.health: int = 3

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.img, (self.x, self.y))

    def move(self) -> None:
        self.y += self.y_velocity
        self.x += self.x_velocity

    def off_screen(self, height: int) -> bool:
        return not (height >= self.y >= 0)

    def collision(self, obj: any) -> tuple[int, int] | None:
        return collide(self, obj)

    def resize(self) -> None:
        self.x = self.x * gameSettings.w_scale
        self.y = self.y * gameSettings.h_scale

        self.img = scaleSurface(self.img, self.imgSrc)
        self.mask = pygame.mask.from_surface(self.img)
        self.y_velocity = self.y_velocity * gameSettings.h_scale
        self.x_velocity = self.x_velocity * gameSettings.h_scale
