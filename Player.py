import os

import pygame

from GameSettings import gameSettings
from Laser import YELLOW_LASER
from Ship import Ship
from ShipType import ShipType
from util import scaleSurface, scaleSurfaceBase

# Player player
PLAYER_IMAGE = pygame.image.load(
    os.path.join("assets", "player_ship.png"))


class Player(Ship):
    def __init__(self, shipType: ShipType, x, y, velocity, health=100):
        super().__init__(shipType, PLAYER_IMAGE, YELLOW_LASER, x, y, velocity, health)
        self.max_health = health

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
