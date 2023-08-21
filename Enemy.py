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
    GREEN_SHIP1, RED_LASER, BLUE_LASER, GREEN_LASER, CANNONBALL, GHOST_SHIP1
from WaterParticles import ParticlePrinciple


class Enemy(Ship):
    COLOR_MAP: dict[str, tuple[pygame.Surface, pygame.Surface]] = {
        "red": ((RED_SHIP1, RED_SHIP2, RED_SHIP3), RED_LASER),
        "green": ((GREEN_SHIP1, GREEN_SHIP2, GREEN_SHIP3), GREEN_LASER),
        "blue": ((BLUE_SHIP1, BLUE_SHIP2, BLUE_SHIP3), BLUE_LASER),
        "ghost": ((GHOST_SHIP1, GHOST_SHIP1, GHOST_SHIP1), BLUE_LASER)
    }

    def __init__(self, isTracker: bool, isDodger: bool, shipType: ShipType, x: int, y: int, color: str, velocity, window: pygame.Surface, health=10):
        super().__init__(shipType, self.COLOR_MAP[color][0], self.COLOR_MAP[color][1], x, y, velocity, health)
        self.color: str = color
        self.particles = ParticlePrinciple(window)
        self.isTracker: bool = isTracker
        self.isDodger: bool = isDodger

    def move(self, playerLasers: [Laser]) -> None:
        addedSpeed: float = 0

        if self.isDodger:
            if len(playerLasers) > 0:
                minDistance: float = math.sqrt((self.x - playerLasers[0].x) ** 2 + (self.y - playerLasers[0].y) ** 2)
                laserToAvoid: Laser = playerLasers[0]

                for laser in playerLasers:
                    distance: float = math.sqrt((self.x - laser.x) ** 2 + (self.y - laser.y) ** 2)
                    if distance < minDistance:
                        laserToAvoid = laser
                        minDistance = distance

                xDiff: float = self.x - laserToAvoid.x
                yDiff: float = self.y - laserToAvoid.y

                xRatio: float = - (1 if xDiff > 0 else -1 - (xDiff / (abs(yDiff) + abs(xDiff))))
                yRatio: float = - (1 if yDiff > 0 else -1 - (yDiff / (abs(yDiff) + abs(xDiff))))
                if minDistance < (350 * gameSettings.h_scale):
                    addedSpeed = 2 * minDistance / (350 * gameSettings.h_scale)

                self.y -= (addedSpeed * yRatio / 2)
                if 15 * gameSettings.w_scale_base < self.x and self.x + self.ship_img.get_width() < gameSettings.width:
                    self.x -= (addedSpeed * (2 * xRatio if yDiff < 0 else 0))


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
                if laser.appliesEffects is True:
                    match self.color:
                        case 'red':
                            pygame.mixer.Sound.play(vulnerableFX)
                            obj.effects['vulnerable'] = gameSettings.FPS * 3
                        case 'green':
                            pygame.mixer.Sound.play(poisonFX)
                            obj.effects['poisoned'] = gameSettings.FPS * 3
                        case 'blue':
                            pygame.mixer.Sound.play(freezeFX)
                            obj.effects['slowed'] = gameSettings.FPS * 3
                        case 'ghost':
                            pygame.mixer.Sound.play(blindFX)
                            obj.effects['short_sighted'] = gameSettings.FPS * 3
                damage: int = gameSettings.ENEMY_LASER_BASE_DAMAGE * (2 if obj.effects.get('vulnerable', 0) > 0 else 1)
                if obj.armor > 0:
                    obj.armor -= damage
                else:
                    obj.health -= damage
                self.lasers.remove(laser)

    def shoot(self) -> None:
        base_probability = 0.05
        increase_factor = 0.1
        probability = min(base_probability + (increase_factor * (mainGameState.level - 1)), 1.0)

        if self.cool_down_counter == 0:
            if random.random() < probability:
                appliesEffects: bool = True
                laserImage: pygame.Surface = self.laser_img
            else:
                appliesEffects: bool = False
                laserImage: pygame.Surface = CANNONBALL

            laser = Laser(int(self.x + self.get_width() / 2 - self.laser_img.get_width() / 2),
                          self.y + self.get_height(),
                          appliesEffects,
                          laserImage,
                          gameSettings.LASER_BASE_VELOCITY)
            self.lasers.append(laser)
            self.cool_down_counter = 1
