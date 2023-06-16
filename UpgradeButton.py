import pygame

from GameSettings import gameSettings
from UpgradeType import UpgradeType
from fonts import main_font
from PlayerUpgrades import playerUpgrades


# button class
from util import scaleRect


class UpgradeButton:
    def __init__(self, window: pygame.Surface, x: float, y: float, width: float, height: float, upgradeType: UpgradeType):
        self.buttonRect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.clicked: bool = False
        self.window: pygame.Surface = window
        self.upgradeType: UpgradeType = upgradeType

    def update(self):
        # Get mouse position
        pos: tuple[int, int] = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.buttonRect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.addPlayerUpgrade()

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def draw(self):

        # Draw button on screen
        pygame.draw.rect(self.window, pygame.Color(255, 255, 255), self.buttonRect, 2)
        self.window.blit(main_font.render(self.upgradeType.name, True, pygame.Color(255, 255, 255)), self.buttonRect)

    def resize(self):
        scaleRect(self.buttonRect)

    def addPlayerUpgrade(self):
        match self.upgradeType:
            case UpgradeType.SHOOTING_SPEED:
                playerUpgrades.shootingSpeed += 1
            case UpgradeType.NUMBER_OF_BULLETS:
                playerUpgrades.numberOfBullets += 1
            case UpgradeType.BULLET_COLLISION:
                playerUpgrades.bulletCollision += 1



