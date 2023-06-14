import random

import pygame

from Enemy import Enemy
from GameScreen import GameScreen
from GameSettings import gameSettings
from Player import Player
from ScreenType import ScreenType
from ShipType import ShipType
from fonts import lost_font, main_font
from util import collide


class MainGame(GameScreen):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self.level: int = 0
        self.lives: int = 5
        self.enemies: [Enemy] = []
        self.waveLength: int = 5
        self.player = Player(ShipType.PLAYER, 300, 630, gameSettings.PLAYER_BASE_VELOCITY)
        self.gameLost = False
        self.lostCount = 0

    # Renders the main menu
    def update(self) -> bool:
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


    def render(self):
        self.window.fill((14, 194, 249))

        # Enemies and player's character
        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw(self.window)

        # Lose screen
        if self.gameLost:
            lost_label = lost_font.render("GAME OVER", True, (255, 255, 255))
            self.window.blit(lost_label, (gameSettings.width / 2 - lost_label.get_width() / 2, 350))

        # Lives and level display
        lives_label = main_font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {self.level}", True, (255, 255, 255))

        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (gameSettings.width - level_label.get_width() - 10, 10))

        pygame.display.update()

    def click_handler(self, button: int, position: tuple[int, int]):
        pass

    def mouse_move_handler(self, button: int, position: tuple[int, int]):
        pass

    def keyboard_button_handler(self, keys: tuple[bool, ...]):
        if not self.gameLost:
            if keys[pygame.K_a] and self.player.x - self.player.velocity > 0:  # left
                self.player.x -= self.player.velocity * gameSettings.w_scale_base
            if keys[pygame.K_d] and self.player.x + self.player.velocity + self.player.get_width() < gameSettings.width:  # right
                self.player.x += self.player.velocity * gameSettings.w_scale_base
            if keys[pygame.K_w] and self.player.y - self.player.velocity > 0:  # up
                self.player.y -= self.player.velocity * gameSettings.h_scale_base
            if keys[pygame.K_s] and self.player.y + self.player.velocity + self.player.get_height() + 15 < gameSettings.height:  # down
                self.player.y += self.player.velocity * gameSettings.h_scale_base
            if keys[pygame.K_SPACE]:
                self.player.shoot()

    def window_resize_handler(self):
        self.player.resize()
        for enemy in self.enemies:
            enemy.resize()

    def checkEndgameConditions(self) -> None:
        if self.lives <= 0 or self.player.health <= 0:
            self.gameLost = True
            self.lostCount += 1

    def updatePlayer(self):
        self.player.move_lasers(self.enemies)
        self.player.updateEffects()

    def updateEnemies(self):
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

    def goToNextLevel(self):
        self.level += 1
        self.waveLength += 5
        for i in range(self.waveLength):
            enemy = Enemy(ShipType.ENEMY,
                          random.randrange(50, gameSettings.width - 100),
                          random.randrange(-1500, -100),
                          random.choice(["red", "blue", "green"]),
                          gameSettings.ENEMY_BASE_VELOCITY)
            self.enemies.append(enemy)