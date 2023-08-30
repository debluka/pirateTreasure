import math
import random

import pygame

from GameSettings import gameSettings
from Laser import Laser
from MainGameState import mainGameState
from Ship import Ship
from ShipType import ShipType
from SoundFx import hitFX, poisonFX, freezeFX, blindFX, vulnerableFX
from Textures import RED_SHIP3, RED_SHIP2, RED_SHIP1, BLUE_SHIP3, BLUE_SHIP2, BLUE_SHIP1, GREEN_SHIP3, GREEN_SHIP2, \
    GREEN_SHIP1, RED_LASER, BLUE_LASER, GREEN_LASER, CANNONBALL, GHOST_SHIP1, HEALTH_LASER, YELLOW_SHIP3, YELLOW_SHIP1, YELLOW_SHIP2
from WaterParticles import ParticlePrinciple


class Ally(Ship):

    def __init__(self, shipType: ShipType, x: int, y: int, color: str, velocity, window: pygame.Surface, health=10, isTracker: bool = True):
        super().__init__(shipType, (YELLOW_SHIP1, YELLOW_SHIP2, YELLOW_SHIP3), HEALTH_LASER, x, y, velocity, health)
        self.color: str = color
        self.particles = ParticlePrinciple(window)
        self.isTracker = isTracker

    def move(self) -> None:
        addedSpeed: float = 0

        if self.isTracker:
            dist: float = math.sqrt((self.x - mainGameState.pX) ** 2 + (self.y + mainGameState.yOffset - mainGameState.pY) ** 2)
            xDiff: float = self.x - mainGameState.pX
            yDiff: float = self.y + mainGameState.yOffset - mainGameState.pY

            xRatio: float = - (xDiff / (abs(yDiff) + abs(xDiff)))
            yRatio: float = - (yDiff / (abs(yDiff) + abs(xDiff)))
            if dist < (350 * gameSettings.h_scale):
                addedSpeed = 2 * dist / (350 * gameSettings.h_scale)

            self.y += (addedSpeed * (yRatio if yDiff < 0 else 0))
            if 15 * gameSettings.w_scale_base < self.x and self.x + self.ship_img.get_width() < gameSettings.width:
                self.x += (addedSpeed * xRatio)

        self.y += self.velocity

    def draw(self, window: pygame.Surface) -> None:
        self.particles.draw()
        super().draw(window)

    def updateParticles(self) -> None:
        self.particles.update()
        self.particles.add_particles(self.x + self.get_width() / 2, self.y + mainGameState.yOffset + self.get_height() * 0.7, -1)
        self.particles.add_particles(self.x + self.get_width() / 2, self.y + mainGameState.yOffset + self.get_height() * 0.4, -1)
        self.particles.add_particles(self.x + self.get_width() / 2, self.y + mainGameState.yOffset + self.get_height() * 0.1, -1)

    def move_lasers(self, obj: any) -> None:
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen(gameSettings.height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                pygame.mixer.Sound.play(hitFX)
                # Apply laser effects
                if obj.health <= obj.max_health - 10:
                    obj.health += 10
                self.lasers.remove(laser)

    def shoot(self) -> None:
        if self.cool_down_counter == 0:
            laserImage: pygame.Surface = self.laser_img

            laser = Laser(int(self.x + self.get_width() / 2 - self.laser_img.get_width() / 2),
                          self.y + self.get_height(),
                          True,
                          laserImage,
                          gameSettings.LASER_BASE_VELOCITY)
            self.lasers.append(laser)
            self.cool_down_counter = 1
