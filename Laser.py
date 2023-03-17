import os

import pygame

from util import collide

RED_LASER = pygame.image.load(os.path.join("assets", "red_projectile.png"))
GREEN_LASER = pygame.image.load(
    os.path.join("assets", "green_projectile.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "blue_projectile.png"))
YELLOW_LASER = pygame.image.load(
    os.path.join("assets", "cannonBall.png"))

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)