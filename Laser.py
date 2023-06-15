import os

import pygame

from GameSettings import gameSettings
from util import collide, scaleSurface, scaleSurfaceBase

RED_LASER = pygame.image.load(os.path.join("assets", "red_projectile.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "green_projectile.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "blue_projectile.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "cannonBall.png"))

class Laser:
    def __init__(self, x, y, img, velocity):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.velocity = velocity * gameSettings.h_scale_base


    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        print(self.velocity)
        self.y += self.velocity

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def resize(self):
        self.x = self.x * gameSettings.w_scale
        self.y = self.y * gameSettings.h_scale

        self.img = scaleSurface(self.img)
        self.mask = pygame.mask.from_surface(self.img)
        self.velocity = self.velocity * gameSettings.h_scale
