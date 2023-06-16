import os

import pygame

from GameSettings import gameSettings
from util import collide, scaleSurface, scaleSurfaceBase


class Laser:
    def __init__(self, x, y, img, y_velocity, x_velocity=0):
        self.x = x
        self.y = y
        self.img = scaleSurfaceBase(img)
        self.imgSrc = img
        self.mask = pygame.mask.from_surface(self.img)
        self.y_velocity = y_velocity * gameSettings.h_scale_base
        self.x_velocity = x_velocity * gameSettings.h_scale_base

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.y_velocity
        self.x += self.x_velocity

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def resize(self):
        self.x = self.x * gameSettings.w_scale
        self.y = self.y * gameSettings.h_scale

        self.img = scaleSurface(self.img, self.imgSrc)
        self.mask = pygame.mask.from_surface(self.img)
        self.y_velocity = self.y_velocity * gameSettings.h_scale
        self.x_velocity = self.x_velocity * gameSettings.h_scale
