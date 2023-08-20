import pygame

from GameSettings import gameSettings
from MainGameState import mainGameState
from util import collide, scaleSurface, scaleSurfaceBase, collide1


class Laser:
    def __init__(self, x: int, y: int, appliesEffects:bool, img: pygame.Surface, y_velocity: float, x_velocity: float = 0, isPlayer = False):
        self.x: int = x
        self.y: int = y
        self.img: pygame.Surface = scaleSurfaceBase(img)
        self.imgSrc: pygame.Surface = img
        self.mask: pygame.Mask = pygame.mask.from_surface(self.img)
        self.y_velocity: float = y_velocity * gameSettings.h_scale_base
        self.x_velocity: float = x_velocity * gameSettings.h_scale_base
        self.isSlowed: bool = False
        self.health: int = 3
        self.appliesEffects: bool = appliesEffects
        self.isPlayer = isPlayer

    def draw(self, window: pygame.Surface) -> None:
        if pygame.Rect(self.x, self.y + mainGameState.yOffset, self.img.get_width(), self.img.get_height()).colliderect(mainGameState.cameraRect):
            window.blit(self.img, (self.x, self.y + mainGameState.yOffset))

    def move(self) -> None:
        self.y += self.y_velocity
        self.x += self.x_velocity

    def off_screen(self, height: int) -> bool:
        return not (height - gameSettings.minY >= self.y >= 0 - gameSettings.maxY and 0 <= self.x <= gameSettings.width)

    def collision(self, obj: any) -> tuple[int, int] | None:
        if self.isPlayer:
            return collide1(self, obj)
        else:
         return collide(self, obj)

    def resize(self) -> None:
        self.x = self.x * gameSettings.w_scale
        self.y = self.y * gameSettings.h_scale

        self.img = scaleSurface(self.img, self.imgSrc)
        self.mask = pygame.mask.from_surface(self.img)
        self.y_velocity = self.y_velocity * gameSettings.h_scale
        self.x_velocity = self.x_velocity * gameSettings.h_scale
