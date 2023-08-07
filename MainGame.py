import math
import random

import pygame

import Textures
from Enemy import Enemy
from ExplosionAnimation import ExplosionAnimation
from GameScreen import GameScreen
from GameSettings import gameSettings
from MainGameState import mainGameState
from Player import Player
from PlayerUpgrades import playerUpgrades
from ScreenType import ScreenType
from ShipType import ShipType
from SoundFx import deathFX, newLevelFX, shipCollisionFX, thunderStrikeFX
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
        self.player = Player(self.window, ShipType(ShipType.PLAYER), int(gameSettings.width / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE3).get_width() / 2), int(gameSettings.height * 0.8), gameSettings.PLAYER_BASE_VELOCITY)
        self.gameLost: bool = False
        self.lostCount: int = 0
        self.animations: list[ExplosionAnimation] = []

        self.upgradeMenu: UpgradeMenu = UpgradeMenu(self.window)
        self.waterColor: (int, int, int) = (14, 194, 249)

        pygame.mixer.music.load('assets/audio/ambient.mp3')
        pygame.mixer.music.play(-1)
    # Renders the main menu
    def update(self) -> bool:
        if mainGameState.isPaused is False:
            if self.nextScreen is not None:
                pygame.mixer.music.play(-1)
                return True

            self.checkEndgameConditions()

            # Endgame text timer
            if self.gameLost:
                if self.lostCount > gameSettings.FPS * 3:
                    mainGameState.reset()
                    playerUpgrades.reset()
                    pygame.mixer.music.stop()
                    saveScore(gameSettings.username, mainGameState.score)
                    self.nextScreen = ScreenType.MAIN_MENU
                    return True
                else:
                    return False

            self.updateEnemies()
            self.updatePlayer()
            self.updateAnimations()

        if self.upgradeMenu.isShown:
            self.upgradeMenu.update()
            self.player.updateUpgrades()

    def render(self) -> None:
        self.window.fill(self.waterColor)



        # Enemies and player's character
        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw(self.window)

        # Animations
        for animation in self.animations:
            animation.draw()

        if mainGameState.limitedVision is True:
            cover_surf = pygame.Surface((gameSettings.width, gameSettings.height))
            cover_surf.fill((80, 80, 80))
            cover_surf.set_colorkey((255, 255, 255))
            pygame.draw.ellipse(cover_surf, (255, 255, 255), (int(mainGameState.pX - gameSettings.blindCircleBaseRadius * gameSettings.w_scale_base),
                                                              int(mainGameState.pY - gameSettings.blindCircleBaseRadius * gameSettings.h_scale_base),
                                                              int(gameSettings.blindCircleBaseRadius * gameSettings.w_scale_base * 2),
                                                              int(gameSettings.blindCircleBaseRadius * gameSettings.h_scale_base * 2)))

            self.window.blit(cover_surf, (0, 0))

        # Lose screen
        if self.gameLost:
            lost_label: pygame.Surface = lost_font.render("GAME OVER", True, (255, 255, 255))
            self.window.blit(lost_label, (gameSettings.width / 2 - lost_label.get_width() / 2, gameSettings.height / 2 - lost_font.get_height() / 2))

        # Lives and level display
        lives_label: pygame.Surface = main_font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        level_label: pygame.Surface = main_font.render(f"Level: {mainGameState.level}", True, (255, 255, 255))
        score_label: pygame.Surface = main_font.render(f"Score: {mainGameState.score}", True, (255, 255, 255))
        money_label: pygame.Surface = main_font.render(f"Money: {mainGameState.money}", True, (255, 255, 255))



        # Pause text
        if mainGameState.isPaused:
            pause_label: pygame.Surface = main_font.render("GAME PAUSED", True, (255, 255, 255))
            self.window.blit(pause_label, (gameSettings.width / 2 - pause_label.get_width() / 2, gameSettings.height / 2 - main_font.get_height() / 2))

        if self.upgradeMenu.isShown:
            self.upgradeMenu.draw()

        self.window.blit(lives_label, (10, 10))
        self.window.blit(score_label, (10, main_font.get_height() + 10))
        self.window.blit(money_label, (10, main_font.get_height() * 2 + 10))
        self.window.blit(level_label, (gameSettings.width - level_label.get_width() - 10, 10))

        pygame.display.update()

    def keyboard_hold_button_handler(self, keys: tuple[bool, ...]) -> None:
        if mainGameState.isPaused is False:
            if not self.gameLost:
                if keys[gameSettings.moveLeftBinding] and self.player.x - self.player.velocity * gameSettings.w_scale_base > 0:  # left
                    self.player.x -= self.player.velocity * gameSettings.w_scale_base
                if keys[gameSettings.moveRightBinding] and self.player.x + self.player.velocity * gameSettings.w_scale_base + self.player.get_width() < gameSettings.width:  # right
                    self.player.x += self.player.velocity * gameSettings.w_scale_base
                if keys[gameSettings.moveUpBinding] and self.player.y - self.player.velocity * gameSettings.w_scale_base > 0:  # up
                    self.player.y -= self.player.velocity * gameSettings.h_scale_base
                if keys[gameSettings.moveDownBinding] and self.player.y + self.player.velocity * gameSettings.w_scale_base + self.player.get_height() + 15 < gameSettings.height:  # down
                    self.player.y += self.player.velocity * gameSettings.h_scale_base
                if keys[gameSettings.shootBinding]:
                    self.player.shoot()

    def keyboard_press_button_handler(self, event: pygame.event.Event) -> None:
        match event.key:
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
            if not self.gameLost:
                pygame.mixer.Sound.play(deathFX)
            self.gameLost = True
            self.lostCount += 1

    def updatePlayer(self) -> None:
        mainGameState.pX = self.player.x + self.player.get_width() / 2
        mainGameState.pY = self.player.y + self.player.get_height() / 2

        self.player.move_lasers(self.enemies, self.animations)
        self.player.updateEffects()
        self.player.updateHealthAndArmor()

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
                pygame.mixer.Sound.play(shipCollisionFX)
                self.player.health -= 10
                self.enemies.remove(enemy)
                self.animations.append(ExplosionAnimation(int(enemy.x + enemy.get_width() / 2), int(enemy.y + enemy.get_height() / 2), self.window))
                mainGameState.score += 10
                mainGameState.money += 10
            elif enemy.y + enemy.get_height() > gameSettings.height:
                # If enemy gets to the bottom of the screen we also lose lives
                self.lives -= 1
                self.enemies.remove(enemy)

    def updateAnimations(self):
        for animation in self.animations:
            animation.update()
            if animation.isDone:
                self.animations.remove(animation)


    def goToNextLevel(self) -> None:
        mainGameState.level += 1
        if mainGameState.level == 5:
            pygame.mixer.Sound.play(thunderStrikeFX)
            pygame.mixer.music.load('assets/audio/thunderAmbient.mp3')
            pygame.mixer.music.play(-1)
            self.waterColor = (11, 41, 46)
        if mainGameState.level > 1:
            pygame.mixer.Sound.play(newLevelFX)
        self.player.armor = self.player.max_armor
        self.waveLength += mainGameState.WAVE_SIZE
        for i in range(self.waveLength):
            enemySpawnTypePool = ["red", "blue", "green"]
            if mainGameState.level > 5:
                enemySpawnTypePool.append("ghost")
            enemy = Enemy(ShipType(ShipType.ENEMY),
                          random.randrange(math.ceil(scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2), math.ceil(gameSettings.width - scaleSurfaceBase(Textures.RED_SHIP1).get_width())),
                          random.randrange(math.ceil(-1500 * gameSettings.h_scale_base), math.ceil(-100 * gameSettings.h_scale_base)),
                          random.choice(enemySpawnTypePool),
                          gameSettings.ENEMY_BASE_VELOCITY * gameSettings.h_scale_base)
            self.enemies.append(enemy)
