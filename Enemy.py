import os
import pygame

from GameSettings import gameSettings
from Laser import RED_LASER, GREEN_LASER, BLUE_LASER, Laser
from Ship import Ship
from ShipType import ShipType
from util import scaleSurface, scaleSurfaceBase

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

    def __init__(self, shipType: ShipType, x, y, color, velocity, health=100):
        super().__init__(shipType, self.COLOR_MAP[color][0], self.COLOR_MAP[color][1], x, y, velocity, health)
        self.color = color

    def move(self):
        self.y += self.velocity

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.get_width()/2 - self.laser_img.get_width()/2, self.y + self.get_height(), self.laser_img, gameSettings.LASER_BASE_VELOCITY)
            self.lasers.append(laser)
            self.cool_down_counter = 1