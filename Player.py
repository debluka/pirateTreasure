import os

import pygame

from Enemy import Enemy
from GameSettings import gameSettings
from PlayerUpgrades import playerUpgrades
from Ship import Ship
from ShipType import ShipType
from Textures import PLAYER_IMAGE, YELLOW_LASER
from fonts import healthbarFont
from util import scaleSurface, scaleSurfaceBase

class Player(Ship):
    def __init__(self, shipType: ShipType, x, y, velocity, health=1000):
        super().__init__(shipType, PLAYER_IMAGE, YELLOW_LASER, x, y, velocity, health)
        self.laser_damage = playerUpgrades.laserDamage
        self.COOLDOWN = 30
        self.updateUpgrades()

    def move_lasers(self, enemies: list[Enemy]):
        # handle player's shooting cooldown
        self.cooldown()
        for playerLaser in self.lasers:
            # move player's laser and remove those thate are off screen
            playerLaser.move()
            if playerLaser.off_screen(gameSettings.height):
                self.lasers.remove(playerLaser)
            else:
                for enemy in enemies:
                    if playerLaser.collision(enemy):
                        # check for laser collision with the enemy and damage/kill the enemy and remove the laser
                        enemy.health -= self.laser_damage
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        if playerLaser in self.lasers:
                            self.lasers.remove(playerLaser)
                    for targetLaser in enemy.lasers:
                        if playerLaser.collision(targetLaser):
                            # if we have the first stage of laser collision upgrades,
                            # we can slow and push them back slightly
                            if playerUpgrades.bulletCollision > 0:
                                targetLaser.y -= 30
                                if targetLaser.isSlowed is False:
                                    targetLaser.isSlowed = True
                                    targetLaser.y_velocity *= 0.8

                            # if we have the second stage of laser collision upgrades,
                            # we can destroy the laser
                            if playerUpgrades.bulletCollision > 1:
                                targetLaser.health -= 1

                            # remove player's laser on hit and enemy's laser if the have no health left
                            if playerLaser in self.lasers:
                                self.lasers.remove(playerLaser)
                            if targetLaser.health <= 0 and targetLaser in enemy.lasers:
                                enemy.lasers.remove(targetLaser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y +
                         self.ship_img.get_height() + 2 + self.healthbarHeight, self.ship_img.get_width(), self.healthbarHeight))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() +
                         2 + self.healthbarHeight, self.ship_img.get_width() * (self.health/self.max_health), self.healthbarHeight))
        window.blit(healthbarFont.render(str(self.health) + " / " + str(self.max_health),
                                         True,
                                         pygame.Color(255, 255, 255)),
                    (self.x, self.y + self.ship_img.get_height() + 2 + self.healthbarHeight, self.ship_img.get_width(), self.healthbarHeight))

    def updateUpgrades(self):
        self.COOLDOWN = 30 - 5 * playerUpgrades.shootingSpeed
