import pygame

from Enemy import Enemy
from ExplosionAnimation import ExplosionAnimation
from GameSettings import gameSettings
from MainGameState import mainGameState
from PlayerUpgrades import playerUpgrades
from Ship import Ship
from ShipType import ShipType
from Textures import PLAYER_IMAGE1, PLAYER_IMAGE2, PLAYER_IMAGE3, CANNONBALL
from fonts import healthbarFont

class Player(Ship):
    def __init__(self, window: pygame.Surface, shipType: ShipType, x: int, y: int, velocity: float, health: int = 100):
        super().__init__(shipType, (PLAYER_IMAGE1, PLAYER_IMAGE2, PLAYER_IMAGE3), CANNONBALL, x, y, velocity, health)
        self.laser_base_damage: int = gameSettings.PLAYER_LASER_BASE_DAMAGE
        self.laser_damage: int = gameSettings.PLAYER_LASER_BASE_DAMAGE
        self.COOLDOWN: int = 30
        self.armor: int = 0
        self.max_armor: int = 0
        self.updateUpgrades()
        self.window: pygame.Surface = window

    def move_lasers(self, enemies: list[Enemy], animations: list[ExplosionAnimation]) -> None:
        # handle player's shooting cooldown
        self.cooldown()
        for playerLaser in self.lasers:
            # move player's laser and remove those that are off-screen
            playerLaser.move()
            if playerLaser.off_screen(gameSettings.height):
                self.lasers.remove(playerLaser)
            else:
                for enemy in enemies:
                    if playerLaser.collision(enemy):
                        # check for laser collision with the enemy and damage/kill the enemy and remove the laser
                        enemy.health -= self.laser_damage
                        if enemy.health <= 0:
                            mainGameState.score += 10
                            mainGameState.money += 10
                            enemies.remove(enemy)
                            animations.append(ExplosionAnimation(int(enemy.x + enemy.get_width() / 2), int(enemy.y + enemy.get_height() / 2), self.window))
                        if playerLaser in self.lasers:
                            self.lasers.remove(playerLaser)
                    for targetLaser in enemy.lasers:
                        if playerLaser.collision(targetLaser):
                            # if we have the first stage of laser collision upgrades,
                            # we can slow and push them back slightly
                            if playerUpgrades.bulletCollision > 0:
                                targetLaser.y -= (30 + 3 * playerUpgrades.projectileSpeed) * gameSettings.h_scale_base
                                if targetLaser.isSlowed is False:
                                    targetLaser.isSlowed = True
                                    targetLaser.y_velocity *= (0.8 - 0.1 * playerUpgrades.projectileSpeed)

                            # if we have the second stage of laser collision upgrades,
                            # we can destroy the laser
                            if playerUpgrades.bulletCollision > 1:
                                targetLaser.health -= 1

                            # remove player's laser on hit and enemy's laser if the have no health left
                            if playerLaser in self.lasers:
                                self.lasers.remove(playerLaser)
                            if targetLaser.health <= 0 and targetLaser in enemy.lasers:
                                enemy.lasers.remove(targetLaser)

    def draw(self, window: pygame.Surface) -> None:
        super().draw(window)
        self.healthbar(window)

        if self.max_armor > 0:
            self.armorBar(window)

    def healthbar(self, window: pygame.Surface) -> None:
        # Red part of the health bar
        pygame.draw.rect(window,
                         (255, 0, 0),
                         (self.x,
                          self.y + self.ship_img.get_height() + 2 + self.healthbarHeight,
                          self.ship_img.get_width(), self.healthbarHeight))

        # Green part of the health bar
        pygame.draw.rect(window,
                         (0, 255, 0),
                         (self.x,
                          self.y + self.ship_img.get_height() + 2 + self.healthbarHeight,
                          self.ship_img.get_width() * (self.health/self.max_health),
                          self.healthbarHeight))

        window.blit(healthbarFont.render(str(int(self.health)) + " / " + str(self.max_health),
                                         True,
                                         pygame.Color(255, 255, 255)),
                    (self.x,
                     self.y + self.ship_img.get_height() + 2 + self.healthbarHeight,
                     self.ship_img.get_width(),
                     self.healthbarHeight))

    def armorBar(self, window: pygame.Surface):
        # Red part of the armor bar
        pygame.draw.rect(window,
                         (255, 0, 0),
                         (self.x + self.ship_img.get_width() + 10,
                          self.y,
                          healthbarFont.get_height(),
                          self.ship_img.get_height()))

        # Grey part of the health bar
        pygame.draw.rect(window,
                         (120, 120, 120),
                         (self.x + self.ship_img.get_width() + 10,
                          self.y,
                          healthbarFont.get_height(),
                          self.ship_img.get_height() * (self.armor/self.max_armor)))

        window.blit(pygame.transform.rotate(healthbarFont.render(str(self.armor) + " / " + str(self.max_armor),
                                            True,
                                            pygame.Color(255, 255, 255)), 270),
                    (self.x + self.ship_img.get_width() + 10,
                     self.y,
                     healthbarFont.get_height(),
                     self.ship_img.get_height()))

    def updateUpgrades(self) -> None:
        self.COOLDOWN = 30 - 5 * playerUpgrades.shootingSpeed
        self.max_health = self.BASE_MAX_HEALTH + mainGameState.HEALTH_PER_UPGRADE * playerUpgrades.maxHealth
        self.velocity = self.base_velocity + mainGameState.VELOCITY_PER_UPGRADE * playerUpgrades.velocity

        isArmorFull: bool = self.armor == self.max_armor
        self.max_armor = mainGameState.ARMOR_PER_UPGRADE * playerUpgrades.armor
        if isArmorFull:
            self.armor = self.max_armor

        self.laser_damage = self.laser_base_damage + mainGameState.PROJECTILE_DAMAGE_PER_UPGRADE * playerUpgrades.projectileDamage

    def updateHealthAndArmor(self) -> None:
        if self.armor < 0:
            self.armor = 0

        if self.health <= self.max_health and self.effects.get('poisoned', 0) <= 0:
            self.health += mainGameState.HEALTH_REGENERATION_PER_UPGRADE * playerUpgrades.healthRegeneration
            if self.health > self.max_health:
                self.health = self.max_health
