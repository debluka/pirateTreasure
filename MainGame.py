import math
import random

import pygame

import Textures
from Enemy import Enemy
from GameScreen import GameScreen
from GameSettings import gameSettings
from MainGameState import mainGameState
from Player import Player
from ScreenType import ScreenType
from ShipType import ShipType
from UpgradeMenu import UpgradeMenu
from dbModifyScores import saveScore
from fonts import lost_font, main_font
from util import collide, scaleSurfaceBase


class MainGame(GameScreen):
    def __init__(self, window: pygame.Surface):
        super().__init__(ScreenType(ScreenType.MAIN_GAME), window)
        self.lives: int = 5
        self.enemies: [Enemy] = []
        self.waveLength: int = 0
        self.player = Player(ShipType(ShipType.PLAYER), int(gameSettings.width / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE).get_width() / 2), int(gameSettings.height * 0.8), gameSettings.PLAYER_BASE_VELOCITY)
        self.gameLost: bool = False
        self.lostCount: int = 0

        self.upgradeMenu: UpgradeMenu = UpgradeMenu(self.window)

    # Renders the main menu
    def update(self) -> bool:
        if mainGameState.isPaused is False:
            if self.nextScreen is not None:
                return True

            self.checkEndgameConditions()

            # Endgame text timer
            if self.gameLost:
                if self.lostCount > gameSettings.FPS * 3:
                    self.nextScreen = ScreenType.MAIN_MENU
                    return True
                else:
                    return False

            self.updateEnemies()
            self.updatePlayer()

        if self.upgradeMenu.isShown:
            self.upgradeMenu.update()
            self.player.updateUpgrades()

    def render(self) -> None:
        self.window.fill((14, 194, 249))

        # Enemies and player's character
        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw(self.window)

        # Lose screen
        if self.gameLost:
            lost_label: pygame.Surface = lost_font.render("GAME OVER", True, (255, 255, 255))
            self.window.blit(lost_label, (gameSettings.width / 2 - lost_label.get_width() / 2, gameSettings.height / 2 - lost_font.get_height() / 2))

        # Lives and level display
        lives_label: pygame.Surface = main_font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        level_label: pygame.Surface = main_font.render(f"Level: {self.level}", True, (255, 255, 255))

        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (gameSettings.width - level_label.get_width() - 10, 10))

        # Pause text
        if mainGameState.isPaused:
            pause_label: pygame.Surface = main_font.render("GAME PAUSED", True, (255, 255, 255))
            self.window.blit(pause_label, (gameSettings.width / 2 - pause_label.get_width() / 2, gameSettings.height / 2 - main_font.get_height() / 2))

        if self.upgradeMenu.isShown:
            self.upgradeMenu.draw()

        pygame.display.update()

    def click_handler(self, button: int, position: tuple[int, int]) -> None:
        pass

    def mouse_move_handler(self, button: int, position: tuple[int, int]) -> None:
        pass

    def keyboard_hold_button_handler(self, keys: tuple[bool, ...]) -> None:
        if mainGameState.isPaused is False:
            if not self.gameLost:
                if keys[pygame.K_a] and self.player.x - self.player.velocity * gameSettings.w_scale_base > 0:  # left
                    self.player.x -= self.player.velocity * gameSettings.w_scale_base
                if keys[pygame.K_d] and self.player.x + self.player.velocity * gameSettings.w_scale_base + self.player.get_width() < gameSettings.width:  # right
                    self.player.x += self.player.velocity * gameSettings.w_scale_base
                if keys[pygame.K_w] and self.player.y - self.player.velocity * gameSettings.w_scale_base > 0:  # up
                    self.player.y -= self.player.velocity * gameSettings.h_scale_base
                if keys[pygame.K_s] and self.player.y + self.player.velocity * gameSettings.w_scale_base + self.player.get_height() + 15 < gameSettings.height:  # down
                    self.player.y += self.player.velocity * gameSettings.h_scale_base
                if keys[pygame.K_SPACE]:
                    self.player.shoot()

    def keyboard_press_button_handler(self, key: int) -> None:
        match key:
            case pygame.K_ESCAPE:
                if self.upgradeMenu.isShown is False:
                    mainGameState.isPaused = not mainGameState.isPaused
            case pygame.K_u:
                self.upgradeMenu.isShown = not self.upgradeMenu.isShown
                if mainGameState.isPaused is False and self.upgradeMenu.isShown is True:
                    mainGameState.isPaused = True
                else:
                    mainGameState.isPaused = False

    def window_resize_handler(self) -> None:
        self.player.resize()
        self.upgradeMenu.resize()
        for enemy in self.enemies:
            enemy.resize()

    def checkEndgameConditions(self) -> None:
        if self.lives <= 0 or self.player.health <= 0:
            self.gameLost = True
            self.lostCount += 1

    def updatePlayer(self) -> None:
        self.player.move_lasers(self.enemies)
        self.player.updateEffects()

    def updateEnemies(self) -> None:
        if len(self.enemies) == 0:
            self.goToNextLevel()

        for enemy in self.enemies[:]:
            enemy.updateEffects()
            enemy.move()
            enemy.move_lasers(self.player)

            # Shooting
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            # Collision checking
            if collide(enemy, self.player):
                self.player.health -= 10
                self.enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > gameSettings.height:
                # If enemy gets to the bottom of the screen we also lose lives
                self.lives -= 1
                self.enemies.remove(enemy)

    def goToNextLevel(self) -> None:
        mainGameState.level += 1
        self.waveLength += mainGameState.WAVE_SIZE
        for i in range(self.waveLength):
            enemy = Enemy(ShipType(ShipType.ENEMY),
                          random.randrange(math.ceil(scaleSurfaceBase(Textures.RED_SHIP).get_width() / 2), math.ceil(gameSettings.width - scaleSurfaceBase(Textures.RED_SHIP).get_width())),
                          random.randrange(math.ceil(-1500 * gameSettings.h_scale_base), math.ceil(-100 * gameSettings.h_scale_base)),
                          random.choice(["red", "blue", "green"]),
                          gameSettings.ENEMY_BASE_VELOCITY * gameSettings.h_scale_base)
            self.enemies.append(enemy)