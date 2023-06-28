import random

import pygame

from GameSettings import gameSettings
from Laser import Laser
from MainGameState import mainGameState
from Ship import Ship
from ShipType import ShipType
from Textures import RED_SHIP3, RED_SHIP2, RED_SHIP1, BLUE_SHIP3, BLUE_SHIP2, BLUE_SHIP1, GREEN_SHIP3, GREEN_SHIP2, \
    GREEN_SHIP1, RED_LASER, BLUE_LASER, GREEN_LASER, CANNONBALL, GHOST_SHIP1


class Enemy(Ship):
    COLOR_MAP: dict[str, tuple[pygame.Surface, pygame.Surface]] = {
        "red": ((RED_SHIP1, RED_SHIP2, RED_SHIP3), RED_LASER),
        "green": ((GREEN_SHIP1, GREEN_SHIP2, GREEN_SHIP3), GREEN_LASER),
        "blue": ((BLUE_SHIP1, BLUE_SHIP2, BLUE_SHIP3), BLUE_LASER),
        "ghost": ((GHOST_SHIP1, GHOST_SHIP1, GHOST_SHIP1), BLUE_LASER)
    }

    def __init__(self, shipType: ShipType, x: int, y: int, color: str, velocity, health=10):
        super().__init__(shipType, self.COLOR_MAP[color][0], self.COLOR_MAP[color][1], x, y, velocity, health)
        self.color: str = color

    def move(self) -> None:
        self.y += self.velocity

    def move_lasers(self, obj: any) -> None:
        self.cooldown()
        for laser in self.lasers:
            laser.move()
            if laser.off_screen(gameSettings.height):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                # Apply laser effects
                if laser.appliesEffects is True:
                    match self.color:
                        case 'red':
                            obj.effects['vulnerable'] = gameSettings.FPS * 3
                        case 'green':
                            obj.effects['poisoned'] = gameSettings.FPS * 3
                        case 'blue':
                            obj.effects['slowed'] = gameSettings.FPS * 3
                        case 'ghost':
                            obj.effects['short_sighted'] = gameSettings.FPS * 3
                if obj.armor > 0:
                    obj.armor -= 10
                else:
                    obj.health -= 10
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
