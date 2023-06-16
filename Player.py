import os

import pygame

from GameSettings import gameSettings
from PlayerUpgrades import playerUpgrades
from Ship import Ship
from ShipType import ShipType
from Textures import PLAYER_IMAGE, YELLOW_LASER
from util import scaleSurface, scaleSurfaceBase

class Player(Ship):
    def __init__(self, shipType: ShipType, x, y, velocity, health=100):
        super().__init__(shipType, PLAYER_IMAGE, YELLOW_LASER, x, y, velocity, health)
        self.max_health = health
        self.COOLDOWN = 30

    def move_lasers(self, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen(gameSettings.height):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +
                         10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def updateUpgrades(self):
        self.COOLDOWN = 30 - 5 * playerUpgrades.shootingSpeed
