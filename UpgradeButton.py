import pygame

from MainGameState import mainGameState
from UpgradeType import UpgradeType
from fonts import main_font
from PlayerUpgrades import playerUpgrades


# button class
from util import scaleRect


class UpgradeButton:
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, upgradeType: UpgradeType):
        self.buttonRect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.clicked: bool = False
        self.window: pygame.Surface = window
        self.upgradeType: UpgradeType = upgradeType

    def update(self) -> None:
        # Get mouse position
        pos: tuple[int, int] = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.buttonRect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.addPlayerUpgrade()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def draw(self) -> None:

        # Draw button on screen
        pygame.draw.rect(self.window, pygame.Color(255, 255, 255), self.buttonRect, 2)
        self.window.blit(main_font.render(self.upgradeType.name, True, pygame.Color(255, 255, 255)), self.buttonRect)

    def resize(self) -> None:
        scaleRect(self.buttonRect)

    def addPlayerUpgrade(self) -> None:
        match self.upgradeType:
            case UpgradeType.HEALTH:
                playerUpgrades.maxHealth += 1
            case UpgradeType.HEALTH_REGENERATION:
                playerUpgrades.healthRegeneration += 1
            case UpgradeType.ARMOR:
                playerUpgrades.armor += 1
            case UpgradeType.VELOCITY:
                playerUpgrades.velocity += 1
            case UpgradeType.SHOOTING_SPEED:
                playerUpgrades.shootingSpeed += 1
            case UpgradeType.NUMBER_OF_BULLETS:
                playerUpgrades.numberOfBullets += 1
            case UpgradeType.PROJECTILE_COLLISION:
                playerUpgrades.bulletCollision += 1
            case UpgradeType.PROJECTILE_SPEED:
                playerUpgrades.projectileSpeed += 1
            case UpgradeType.PROJECTILE_DAMAGE:
                playerUpgrades.projectileDamage += 1



