import pygame

from GameSettings import gameSettings
from Laser import Laser
from PlayerUpgrades import playerUpgrades
from ShipType import ShipType
from fonts import healthbarFont
from util import scaleSurface, scaleSurfaceBase


class Ship:
    COOLDOWN: int = 30

    def __init__(self, shipType: ShipType, shipImg: pygame.Surface, laserImg: pygame.Surface, x: int, y: int, velocity: float, health: int = 100):
        self.x: int = x
        self.y: int = y
        self.health: int = health
        self.BASE_MAX_HEALTH: int = health
        self.max_health: int = health
        self.imgSrc: pygame.Surface = shipImg
        self.ship_img: pygame.Surface = scaleSurfaceBase(shipImg)
        self.laser_img: pygame.Surface = laserImg
        self.lasers: list[Laser] = []
        self.effects: dict[str, int] = dict()
        self.cool_down_counter: int = 0
        self.base_velocity: float = velocity
        self.velocity: float = velocity
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.ship_img)
        self.shipType: ShipType = shipType
        self.healthbarHeight: int = healthbarFont.get_height()

    def draw(self, window: pygame.Surface) -> None:
        window.blit(self.ship_img, (self.x, self.y))
        self.healthbar(window)
        for laser in self.lasers:
            laser.draw(window)

    def healthbar(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y - 2 - self.healthbarHeight, self.ship_img.get_width(), self.healthbarHeight))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y - 2 - self.healthbarHeight, self.ship_img.get_width() * (self.health / self.max_health), self.healthbarHeight))
        window.blit(healthbarFont.render(str(self.health) + " / " + str(self.max_health),
                                         True,
                                         pygame.Color(255, 255, 255)),
                    (self.x, self.y - 2 - self.healthbarHeight, self.ship_img.get_width(), self.healthbarHeight))

    def updateEffects(self) -> None:
        for effect, duration in self.effects.items():
            if duration > 0:
                self.effects[effect] = duration - 1
                match effect:
                    case 'slowed':
                        self.velocity = self.base_velocity * 0.6 if duration > 1 else 5
                    case 'poisoned':
                        if duration % 10 == 0:
                            self.health = self.health - 1

    def cooldown(self) -> None:
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self) -> None:
        if self.cool_down_counter == 0:
            laser = Laser(int(self.x + self.get_width()/2 - self.laser_img.get_width()/2), self.y, self.laser_img, -gameSettings.LASER_BASE_VELOCITY)
            self.lasers.append(laser)

            if self.shipType is ShipType.PLAYER:
                if playerUpgrades.numberOfBullets >= 2:
                    laser = Laser(int(self.x + self.get_width() / 2 - self.laser_img.get_width() / 2), self.y,
                                  self.laser_img, -gameSettings.LASER_BASE_VELOCITY, -gameSettings.LASER_BASE_VELOCITY * 0.1)
                    self.lasers.append(laser)
                if playerUpgrades.numberOfBullets >= 3:
                    laser = Laser(int(self.x + self.get_width() / 2 - self.laser_img.get_width() / 2), self.y,
                                  self.laser_img, -gameSettings.LASER_BASE_VELOCITY, gameSettings.LASER_BASE_VELOCITY * 0.1)
                    self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self) -> int:
        return self.ship_img.get_width()

    def get_height(self) -> int:
        return self.ship_img.get_height()

    def resize(self) -> None:
        self.x = self.x * gameSettings.w_scale
        self.y = self.y * gameSettings.h_scale

        self.ship_img = scaleSurface(self.ship_img, self.imgSrc)
        self.mask = pygame.mask.from_surface(self.ship_img)

        if self.shipType is ShipType.ENEMY:
            self.velocity *= gameSettings.h_scale

        for laser in self.lasers:
            laser.resize()
