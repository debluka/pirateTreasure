import os
import pygame

from Laser import RED_LASER, GREEN_LASER, BLUE_LASER, Laser
from Ship import Ship

RED_SHIP = pygame.image.load(
    os.path.join("assets", "enemy_red.png"))
GREEN_SHIP = pygame.image.load(
    os.path.join("assets", "enemy_green.png"))
BLUE_SHIP = pygame.image.load(
    os.path.join("assets", "enemy_blue.png"))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.get_width()/2 - self.laser_img.get_width()/2, self.y + self.get_height(), self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1