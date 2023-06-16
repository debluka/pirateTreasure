import pygame

import util
from GameSettings import gameSettings
from UpgradeButton import UpgradeButton
from UpgradeType import UpgradeType
from fonts import main_font


class UpgradeMenu:
    def __init__(self, window: pygame.Surface):
        self.window: pygame.Surface = window
        self.borderRadius = 6
        self.isShown: bool = False
        self.wMargin = 20

        self.x: int = gameSettings.width * 0.05
        self.y: int = gameSettings.height * 0.05
        self.width: int = gameSettings.width * 0.9
        self.height: int = gameSettings.height * 0.9

        self.backgroundRect: pygame.Rect = pygame.Rect((self.x, self.y, self.width, self.height))

        self.titleText: str = "Upgrade menu"
        self.textRect: pygame.Rect = pygame.Rect(self.backgroundRect.center[0] - main_font.size(self.titleText)[0] / 2,
                                                 self.backgroundRect.y + 0.05 * self.height,
                                                 main_font.size(self.titleText)[0],
                                                 main_font.size(self.titleText)[1])

        self.menuRect: pygame.Rect = pygame.Rect(self.backgroundRect.x + self.wMargin,
                                                 self.backgroundRect.y + self.backgroundRect.height * 0.15,
                                                 self.backgroundRect.width - 2 * self.wMargin,
                                                 self.backgroundRect.bottomleft[1] - (self.backgroundRect.y + self.backgroundRect.height * 0.15) - self.wMargin)

        self.upgradeButtons = self.initUpgradeButtons()

    def update(self):
        for button in self.upgradeButtons:
            button.update()

    def draw(self):
        pygame.draw.rect(self.window, (87, 217, 255), self.backgroundRect, border_radius=self.borderRadius)
        pygame.draw.rect(self.window, (0, 255, 0), self.menuRect)
        self.window.blit(main_font.render(self.titleText, True, (255, 255, 255)),
                         (self.backgroundRect.center[0] - self.textRect.width / 2, self.textRect.y))

        for button in self.upgradeButtons:
            button.draw()


    def resize(self):
        self.wMargin *= gameSettings.w_scale
        util.scaleRect(self.menuRect)
        util.scaleRect(self.backgroundRect)

        self.textRect.x = (gameSettings.width - main_font.size(self.titleText)[0]) / 2
        self.textRect.y = self.textRect.y * gameSettings.h_scale

        for button in self.upgradeButtons:
            button.resize()

    def initUpgradeButtons(self):
        return [UpgradeButton(self.window, self.menuRect.x, self.menuRect.y, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.SHOOTING_SPEED),
                UpgradeButton(self.window, self.menuRect.x + self.menuRect.width * 1 / 3, self.menuRect.y, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.HEALTH),
                UpgradeButton(self.window, self.menuRect.x + self.menuRect.width * 2 / 3, self.menuRect.y, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.WIND_IGNORE),
                UpgradeButton(self.window, self.menuRect.x, self.menuRect.y + self.menuRect.height * 1 / 3, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.BULLET_COLLISION),
                UpgradeButton(self.window, self.menuRect.x + self.menuRect.width * 1 / 3, self.menuRect.y + self.menuRect.height * 1 / 3, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.ARMOR),
                UpgradeButton(self.window, self.menuRect.x + self.menuRect.width * 2 / 3, self.menuRect.y + self.menuRect.height * 1 / 3, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.MULTI_CANNON),
                UpgradeButton(self.window, self.menuRect.x, self.menuRect.y + self.menuRect.height * 2 / 3, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.HEALTH_REGENERATION),
                UpgradeButton(self.window, self.menuRect.x + self.menuRect.width * 1 / 3, self.menuRect.y + self.menuRect.height * 2 / 3, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.NUMBER_OF_BULLETS),
                UpgradeButton(self.window, self.menuRect.x + self.menuRect.width * 2 / 3, self.menuRect.y + self.menuRect.height * 2 / 3, self.menuRect.width * 1 / 3, self.menuRect.height * 1 / 3, UpgradeType.DUMMY_2),
        ]