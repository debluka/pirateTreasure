import pygame

from MainGameState import mainGameState
from UpgradeType import UpgradeType
from PlayerUpgrades import playerUpgrades

# button class
from util import scaleRect


class UpgradeButton:
    def __init__(self, window: pygame.Surface, x: int, y: int, width: int, height: int, upgradeType: UpgradeType):
        self.buttonRect: pygame.Rect = pygame.Rect(x, y, width, height)
        self.clicked: bool = False
        self.window: pygame.Surface = window
        self.upgradeType: UpgradeType = upgradeType
        # self.img: pygame.Surface = pygame.transform.scale(GHOST_SHIP1, (
        #     GHOST_SHIP1.get_width() * self.buttonRect.width / 2 / GHOST_SHIP1.get_width(),
        #     GHOST_SHIP1.get_height() * self.buttonRect.height / 2 / GHOST_SHIP1.get_height()))
        # self.img.set_alpha(128)
        self.upgradeTitleFont: pygame.font.Font = pygame.font.SysFont("bahnschrift", 20)
        self.upgradeExplanationFont: pygame.font.Font = pygame.font.SysFont("bahnschrift", 18)
        self.upgradeLevel: int = 0
        self.displayText: str = ''
        self.explanationText: [str] = []
        self.cost: int = 0
        self.maxLevel: int = 0

        match self.upgradeType:
            case UpgradeType.HEALTH:
                self.displayText = "Max health"
                self.explanationText = ["Increase your max",
                                        "health by 20"]
                self.cost = 25
                self.maxLevel = 10
            case UpgradeType.HEALTH_REGENERATION:
                self.displayText = "Health regen"
                self.explanationText = ["Increase your health",
                                        "regen by 0.6/s"]
                self.cost = 20
                self.maxLevel = 10
            case UpgradeType.ARMOR:
                self.displayText = "Armor"
                self.explanationText = ["Increase your armor",
                                        "by 20. Armor blocks",
                                        "damage from enemy",
                                        "projectiles but does",
                                        "not block damage",
                                        "from ship collisions"]
                self.cost = 30
                self.maxLevel = 10
            case UpgradeType.VELOCITY:
                self.displayText = "Move speed"
                self.explanationText = ["Increase your move",
                                        "speed"]
                self.cost = 20
                self.maxLevel = 5
            case UpgradeType.SHOOTING_SPEED:
                self.displayText = "Shooting speed"
                self.explanationText = ["Increase your rate",
                                        "of fire"]
                self.cost = 30
                self.maxLevel = 5
            case UpgradeType.NUMBER_OF_BULLETS:
                self.displayText = "No. of projectiles"
                self.explanationText = ["Increase your projectile",
                                        "count per shot fired"]
                self.cost = 150
                self.maxLevel = 3
            case UpgradeType.PROJECTILE_COLLISION:
                self.displayText = "Projectile collision"
                self.explanationText = ["Your projectiles slow",
                                        "and knockback enemy",
                                        "projectiles. At level 2",
                                        "you can also destroy",
                                        "them with 3 hits"]
                self.cost = 75
                self.maxLevel = 2
            case UpgradeType.PROJECTILE_SPEED:
                self.displayText = "Projectile speed"
                self.explanationText = ["Increase projectile",
                                        "move speed, which also",
                                        "increase slow and",
                                        "knocback strength",
                                        "if you have the required",
                                        "collision upgrade"]
                self.cost = 20
                self.maxLevel = 10
            case UpgradeType.PROJECTILE_DAMAGE:
                self.displayText = "Projectile damage"
                self.explanationText = ["Projectile's damage",
                                        "is increased by 5"]
                self.cost = 50
                self.maxLevel = 4

    def update(self) -> None:
        match self.upgradeType:
            case UpgradeType.HEALTH:
                self.upgradeLevel = playerUpgrades.maxHealth
            case UpgradeType.HEALTH_REGENERATION:
                self.upgradeLevel = playerUpgrades.healthRegeneration
            case UpgradeType.ARMOR:
                self.upgradeLevel = playerUpgrades.armor
            case UpgradeType.VELOCITY:
                self.upgradeLevel = playerUpgrades.velocity
            case UpgradeType.SHOOTING_SPEED:
                self.upgradeLevel = playerUpgrades.shootingSpeed
            case UpgradeType.NUMBER_OF_BULLETS:
                self.upgradeLevel = playerUpgrades.numberOfBullets
            case UpgradeType.PROJECTILE_COLLISION:
                self.upgradeLevel = playerUpgrades.bulletCollision
            case UpgradeType.PROJECTILE_SPEED:
                self.upgradeLevel = playerUpgrades.projectileSpeed
            case UpgradeType.PROJECTILE_DAMAGE:
                self.upgradeLevel = playerUpgrades.projectileDamage

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

        # Button background and border
        if self.clicked:
            backgroundColor = (90, 90, 90)
        else:
            backgroundColor = (80, 80, 80)
        pygame.draw.rect(self.window, backgroundColor, self.buttonRect)
        pygame.draw.rect(self.window, pygame.Color(255, 255, 255), self.buttonRect, 2)

        # # Background image
        # self.window.blit(self.img, (self.buttonRect.x + self.buttonRect.width / 2 - self.img.get_width() / 2,
        #                             self.buttonRect.y + self.buttonRect.height / 2 - self.img.get_height() / 2))

        # Upgrade name
        self.window.blit(self.upgradeTitleFont.render(self.displayText + " " + str(self.upgradeLevel),
                                                      True,
                                                      pygame.Color(220, 220, 58)),
                         (self.buttonRect.x + 10,
                          self.buttonRect.y + 10))

        # Upgrade explanation
        textOffset: int = self.buttonRect.y + 10 + self.upgradeTitleFont.get_height() + 5
        for text in self.explanationText:
            self.window.blit(self.upgradeExplanationFont.render(text,
                                                                True,
                                                                pygame.Color(255, 255, 255)),
                             (self.buttonRect.x + 10,
                              textOffset))
            textOffset += self.upgradeExplanationFont.get_height()

        # Upgrade cost
        self.window.blit(self.upgradeTitleFont.render("Cost: " + str(self.cost),
                                                      True,
                                                      pygame.Color(6, 197, 207)),
                         (self.buttonRect.x + 10,
                          self.buttonRect.y + self.buttonRect.height - 10 - self.upgradeTitleFont.get_height()))

    def resize(self) -> None:
        scaleRect(self.buttonRect)

    def addPlayerUpgrade(self) -> None:
        if mainGameState.money < self.cost or self.upgradeLevel >= self.maxLevel:
            return

        mainGameState.money -= self.cost
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
