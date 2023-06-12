import random

import pygame

from Enemy import Enemy
from GameScreen import GameScreen
from Player import Player
from ScreenType import ScreenType
from fonts import lost_font, main_font
from util import PLAYER_BASE_VELOCITY, WIDTH, FPS, LASER_BASE_VELOCITY, HEIGHT, ENEMY_BASE_VELOCITY, collide


class MainGame(GameScreen):
    def __init__(self, window: pygame.Surface):
        super().__init__(window)
        self.level: int = 0
        self.lives: int = 5
        self.enemies: [Enemy] = []
        self.waveLength: int = 5
        self.player = Player(300, 630, PLAYER_BASE_VELOCITY)
        self.gameLost = False
        self.lostCount = 0

    # Renders the main menu
    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

        # Loose condition
        # TODO: move to separate functions
        if self.lives <= 0 or self.player.health <= 0:
            self.gameLost = True
            self.lostCount += 1

        if self.gameLost:
            if self.lostCount > FPS * 3:
                self.nextScreen = ScreenType.MAIN_MENU
                return True
            else:
                return False

        # Enemy spawning
        if len(self.enemies) == 0:
            self.level += 1
            self.waveLength += 5
            for i in range(self.waveLength):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-1500, -100),
                              random.choice(["red", "blue", "green"]),
                              PLAYER_BASE_VELOCITY)
                self.enemies.append(enemy)

        # Player projectile update
        self.player.move_lasers(-LASER_BASE_VELOCITY, self.enemies)

        # Enemy updating
        for enemy in self.enemies[:]:
            enemy.updateEffects()
            enemy.move(ENEMY_BASE_VELOCITY)
            enemy.move_lasers(LASER_BASE_VELOCITY, self.player)

            # Shooting
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            # Collision checking
            if collide(enemy, self.player):
                self.player.health -= 10
                self.enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                # If enemy gets to the bottom of the screen we also lose lives
                self.lives -= 1
                self.enemies.remove(enemy)

        self.player.updateEffects()

    def render(self):
        self.window.fill((14, 194, 249))

        # Enemies and player's character
        for enemy in self.enemies:
            enemy.draw(self.window)

        self.player.draw(self.window)

        # Lose screen
        if self.gameLost:
            lost_label = lost_font.render("GAME OVER", True, (255, 255, 255))
            self.window.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        # Lives and level display
        lives_label = main_font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {self.level}", True, (255, 255, 255))

        self.window.blit(lives_label, (10, 10))
        self.window.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        pygame.display.update()

    def click_handler(self, button: int, position: tuple[int, int]):
        pass

    def mouse_move_handler(self, button: int, position: tuple[int, int]):
        pass

    def keyboard_button_handler(self, keys: tuple[bool, ...]):
        if keys[pygame.K_a] and self.player.x - self.player.velocity > 0:  # left
            self.player.x -= self.player.velocity
        if keys[pygame.K_d] and self.player.x + self.player.velocity + self.player.get_width() < WIDTH:  # right
            self.player.x += self.player.velocity
        if keys[pygame.K_w] and self.player.y - self.player.velocity > 0:  # up
            self.player.y -= self.player.velocity
        if keys[pygame.K_s] and self.player.y + self.player.velocity + self.player.get_height() + 15 < HEIGHT:  # down
            self.player.y += self.player.velocity
        if keys[pygame.K_SPACE]:
            self.player.shoot()
