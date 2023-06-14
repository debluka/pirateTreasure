import os

import pygame

from GameSettings import gameSettings
from Laser import YELLOW_LASER
from Ship import Ship

# Player player
PLAYER_IMAGE = pygame.image.load(
    os.path.join("assets", "player_ship.png"))


class Player(Ship):
    def __init__(self, x, y, velocity, health=100):
        super().__init__(x, y, velocity, health)
        self.ship_img = PLAYER_IMAGE
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
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