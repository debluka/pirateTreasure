import pygame

from GameSettings import gameSettings
from Laser import Laser
from Ship import Ship
from ShipType import ShipType
from Textures import RED_SHIP, BLUE_SHIP, GREEN_SHIP, RED_LASER, BLUE_LASER, GREEN_LASER


class Enemy(Ship):
    COLOR_MAP: dict[str, tuple[pygame.Surface, pygame.Surface]] = {
        "red": (RED_SHIP, RED_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
        "blue": (BLUE_SHIP, BLUE_LASER)
    }

    def __init__(self, shipType: ShipType, x: int, y: int, color: str, velocity, health=100):
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
                match self.color:
                    case 'red':
                        obj.effects['vulnerable'] = gameSettings.FPS * 3
                    case 'green':
                        obj.effects['poisoned'] = gameSettings.FPS * 3
                    case 'blue':
                        obj.effects['slowed'] = gameSettings.FPS * 3
                obj.health -= 10
                self.lasers.remove(laser)

    def shoot(self) -> None:
        if self.cool_down_counter == 0:
            laser = Laser(int(self.x + self.get_width()/2 - self.laser_img.get_width()/2), self.y + self.get_height(), self.laser_img, gameSettings.LASER_BASE_VELOCITY)
            self.lasers.append(laser)
            self.cool_down_counter = 1
