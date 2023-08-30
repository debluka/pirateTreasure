import math
import random

import pygame

import Textures
from Ally import Ally
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
from WaterParticles import ParticlePrinciple
from dbModifyScores import saveScore
from fonts import lost_font, main_font
from util import collide, scaleSurfaceBase, line_rect_collision, rotate_point


class Tutorial(GameScreen):
    def __init__(self, window: pygame.Surface):
        super().__init__(ScreenType(ScreenType.MAIN_GAME), window)
        self.player = Player(self.window, ShipType(ShipType.PLAYER), gameSettings.width / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE3).get_width() / 2, gameSettings.height / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE3).get_height() / 2, gameSettings.PLAYER_BASE_VELOCITY)
        self.animations: list[ExplosionAnimation] = []

        self.upgradeMenu: UpgradeMenu = UpgradeMenu(self.window)
        self.waterColor: (int, int, int) = (14, 194, 249)

        self.base_water_color = '#3D897B'
        self.high_light_color = '#FFFFFF'
        self.points: [[pygame.Vector2, int]] = []
        self.populate()
        self.playerParticles = ParticlePrinciple(self.window)
        self.enemies: [Enemy] = []
        self.allies: [Ally] = []
        self.shootCounter: int = 0
        mainGameState.money = 10000


        self.step = 0
        self.steps = [["Welcome to the Pirate's Game tutorial!",
                       "Press ENTER to go to the next step"],
                      ["Move with W, A, S, D or",
                       "rotate your ship with Q or E.",
                       "Press SPACE to shoot!"],
                      ["Main goal of the game is to sink",
                       "enemy ships which come in waves",
                       "and earn money to buy upgrades to sink",
                       "even more ships!",
                       "(press U to open the upgrade menu)"],
                      ["Each enemy ship also fires special bullets,",
                       "which apply certain effects."],
                      ["Allies will also spawn each wave. Their",
                       "projectiles will heal you and smashing your",
                       "boat into them will deal significantly more",
                       "damage to your ship."],
                      ["Press ENTER again to return to the main menu!"]]


        pygame.mixer.music.load('assets/audio/ambient.mp3')
        pygame.mixer.music.play(-1)

    def populate(self) -> None:
        random.seed(None)
        # first_sin_input = random.randint(1,90)
        for x in range(int(gameSettings.width / (30 * gameSettings.w_scale_base))):
            for y in range(int((gameSettings.height - gameSettings.minY + gameSettings.maxY) / (90* gameSettings.w_scale_base))):
                point_xy = pygame.Vector2(random.randint(0, 23) + (gameSettings.width / 24) * x,
                                          random.randint(0, 200) + ((gameSettings.height - gameSettings.minY + gameSettings.maxY) / 25) * y - gameSettings.maxY)
                self.points.append([point_xy, random.randint(1, 359)])

    def wave(self, point: pygame.Vector2, sin_input: int) -> int:

        speed: int = random.randint(1, 2)
        sin_input += speed
        if sin_input >= 360:
            sin_input = 0

        point.y += (math.sin(math.radians(sin_input))) / random.randint(20, 25)

        return sin_input

    # Renders the main menu
    def update(self) -> bool:
        mainGameState.cameraRect = pygame.Rect(0, 0, gameSettings.width, gameSettings.height)
        if mainGameState.isPaused is False:
            self.playerParticles.update()
            for point in self.points:
                point[1] = self.wave(point[0], point[1])
            if self.nextScreen is not None:
                pygame.mixer.music.play(-1)
                return True

            self.updateEnemies()
            self.updateAllies()
            self.updatePlayer()
            self.updateAnimations()

        if self.upgradeMenu.isShown:
            self.upgradeMenu.update()
            self.player.updateUpgrades()

    def render(self) -> None:
        # Background and sea effects
        self.window.fill(self.waterColor)
        self.playerParticles.draw()
        for point in self.points:
            random_width = point[1] // 100
            vector_width = pygame.Vector2(random_width, 0)
            startPos = [point[0][0] - vector_width[0], point[0][1] - vector_width[1] + mainGameState.yOffset]
            endPos = [point[0][0] + vector_width[0], point[0][1] + vector_width[1] + mainGameState.yOffset]
            if line_rect_collision(startPos, endPos, mainGameState.cameraRect):
                pygame.draw.line(self.window, (255, 255, 255), startPos, endPos)

        # Reference lines
        enemySurface = pygame.Surface((gameSettings.width, gameSettings.baseHeight * gameSettings.w_scale_base))
        enemySurface.set_alpha(99)
        enemySurface.fill((255, 0, 0))
        self.window.blit(enemySurface, (0, -gameSettings.maxY + mainGameState.yOffset))

        midSurface = pygame.Surface((gameSettings.width, 10 * gameSettings.w_scale_base))
        midSurface.set_alpha(99)
        midSurface.fill((50, 160, 250))
        self.window.blit(midSurface, (0, gameSettings.height / 2 - 5 + mainGameState.yOffset))

        homeSurface = pygame.Surface((gameSettings.width, gameSettings.baseHeight * gameSettings.w_scale_base))
        homeSurface.set_alpha(99)
        homeSurface.fill((0, 255, 0))
        self.window.blit(homeSurface, (0, -gameSettings.minY + gameSettings.height + mainGameState.yOffset - gameSettings.baseHeight))

        # Tutorial text
        lineCount: int = 0
        for line in self.steps[self.step]:
            tutorialText = main_font.render(line, True, (255, 255, 255))
            self.window.blit(tutorialText, (int(gameSettings.width / 2 - main_font.size(line)[0] / 2),
                                                 int(gameSettings.height * 0.2 + (main_font.get_height() + 3) * lineCount) + mainGameState.yOffset,
                                                 tutorialText.get_width(),
                                                 tutorialText.get_height()))
            lineCount += 1

        for enemy in self.enemies:
            enemy.draw(self.window)

        for ally in self.allies:
            ally.draw(self.window)

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

        # Pause text
        if mainGameState.isPaused:
            pause_label: pygame.Surface = main_font.render("GAME PAUSED", True, (255, 255, 255))
            self.window.blit(pause_label, (gameSettings.width / 2 - pause_label.get_width() / 2, gameSettings.height / 2 - main_font.get_height() / 2))

        if self.upgradeMenu.isShown:
            self.upgradeMenu.draw()

        pygame.display.update()

    def keyboard_hold_button_handler(self, keys: tuple[bool, ...]) -> None:
        if mainGameState.isPaused is False:
            origin = pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() / 2)
            if keys[gameSettings.moveLeftBinding] and self.player.x - self.player.velocity * gameSettings.w_scale_base > 15 * gameSettings.w_scale_base:
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.7), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.4), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.1), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                self.player.x -= self.player.velocity * gameSettings.w_scale_base
            # right
            if keys[gameSettings.moveRightBinding] and self.player.x + self.player.velocity * gameSettings.w_scale_base + self.player.get_width() < gameSettings.width:
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.7), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.4), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.1), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                self.player.x += self.player.velocity * gameSettings.w_scale_base
            # up
            if keys[gameSettings.moveUpBinding] and self.player.y - self.player.velocity * gameSettings.w_scale_base > 0:
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.7), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.4), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.1), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, 1)
                if gameSettings.maxY > mainGameState.yOffset >= gameSettings.minY and self.player.y <= gameSettings.height / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE3).get_height() / 2:
                    mainGameState.yOffset += self.player.velocity * gameSettings.h_scale_base
                    if mainGameState.yOffset > gameSettings.maxY:
                        mainGameState.yOffset = gameSettings.maxY
                else:
                    self.player.y -= self.player.velocity * gameSettings.h_scale_base
            # down
            if keys[gameSettings.moveDownBinding] and self.player.y + self.player.velocity * gameSettings.w_scale_base + self.player.get_height() + 15 < gameSettings.height:
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.7), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, -1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.4), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, -1)
                point = rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.1), -self.player.rotate, origin)
                self.playerParticles.add_particles(point.x, point.y, -1)
                if gameSettings.minY < mainGameState.yOffset <= gameSettings.maxY and self.player.y >= gameSettings.height / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE3).get_height() / 2:
                    mainGameState.yOffset -= self.player.velocity * gameSettings.h_scale_base
                    if mainGameState.yOffset < gameSettings.minY:
                        mainGameState.yOffset = gameSettings.minY
                else:
                    self.player.y += self.player.velocity * gameSettings.h_scale_base
            # rotate left
            if keys[pygame.K_e]:
                self.player.rotate -= 2
            # rotate right
            if keys[pygame.K_q]:
                self.player.rotate += 2
            # shoot
            if keys[gameSettings.shootBinding]:
                self.player.shoot()
            if keys[pygame.K_BACKSPACE]:
                pygame.mixer.music.stop()
                mainGameState.reset()
                playerUpgrades.reset()
                self.nextScreen = ScreenType.MAIN_MENU

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
            case pygame.K_RETURN:
                self.step += 1
                if self.step == 2:
                    self.spawnOneEnemy()
                if self.step == 3:
                    mainGameState.level = 11
                    self.enemies = []
                    self.spawnAllEnemyTypes()
                if self.step == 4:
                    mainGameState.level = 11
                    self.enemies = []
                    self.spawnOneAlly()
                if self.step >= len(self.steps):
                    pygame.mixer.music.stop()
                    mainGameState.reset()
                    playerUpgrades.reset()
                    self.nextScreen = ScreenType.MAIN_MENU


    def window_resize_handler(self) -> None:
        self.player.resize()
        self.upgradeMenu.resize()

        for enemy in self.enemies:
            enemy.resize()
        for ally in self.allies:
            ally.resize()

        self.points = []
        self.populate()

    def updateEnemies(self) -> None:
        for enemy in self.enemies[:]:
            enemy.updateParticles()
            enemy.updateEffects()
            enemy.move(self.player.lasers)
            enemy.move_lasers(self.player)

            # Shooting
            if self.shootCounter % 60 == 0:
                enemy.shoot()

            # Collision checking
            if collide(enemy, self.player):
                pygame.mixer.Sound.play(shipCollisionFX)
                self.player.health -= 10
                self.enemies.remove(enemy)
                self.animations.append(ExplosionAnimation(int(enemy.x + enemy.get_width() / 2), int(enemy.y + enemy.get_height() / 2), self.window))
            elif enemy.y + enemy.get_height() > gameSettings.height - gameSettings.minY - gameSettings.baseHeight:
                # If enemy gets to the bottom of the screen we also lose lives
                self.enemies.remove(enemy)

    def updateAllies(self) -> None:
        for ally in self.allies[:]:
            ally.updateParticles()
            ally.updateEffects()
            ally.move()
            ally.move_lasers(self.player)

            # Shooting
            if self.shootCounter % 60 == 0:
                ally.shoot()

            # Collision checking
            if collide(ally, self.player):
                pygame.mixer.Sound.play(shipCollisionFX)
                self.player.health -= 50
                self.allies.remove(ally)
                self.animations.append(ExplosionAnimation(int(ally.x + ally.get_width() / 2), int(ally.y + ally.get_height() / 2), self.window))
            elif ally.y + ally.get_height() > gameSettings.height - gameSettings.minY - gameSettings.baseHeight:
                self.allies.remove(ally)

    def updatePlayer(self) -> None:
        mainGameState.pX = self.player.x + self.player.get_width() / 2
        mainGameState.pY = self.player.y + self.player.get_height() / 2

        self.player.move_lasers(self.allies, self.enemies, self.animations)
        self.player.updateEffects()
        self.player.updateHealthAndArmor()

    def updateAnimations(self):
        for animation in self.animations:
            animation.update()
            if animation.isDone:
                self.animations.remove(animation)

    def spawnOneEnemy(self):
        self.enemies.append(Enemy(False,
                                   False,
                                   ShipType(ShipType.ENEMY),
                                   int(gameSettings.width / 2 - scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2),
                                   int(30 * gameSettings.h_scale_base),
                                   "red",
                                   0,
                                   self.window,
                                   100))

    def spawnAllEnemyTypes(self):
        self.enemies.append(Enemy(False,
                                  False,
                                  ShipType(ShipType.ENEMY),
                                  int(gameSettings.width * 0.2 - scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2),
                                  int(30 * gameSettings.h_scale_base),
                                  "red",
                                  0,
                                  self.window,
                                  100))

        self.enemies.append(Enemy(False,
                                  False,
                                  ShipType(ShipType.ENEMY),
                                  int(gameSettings.width * 0.4 - scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2),
                                  int(30 * gameSettings.h_scale_base),
                                  "green",
                                  0,
                                  self.window,
                                  100))

        self.enemies.append(Enemy(False,
                                  False,
                                  ShipType(ShipType.ENEMY),
                                  int(gameSettings.width * 0.6 - scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2),
                                  int(30 * gameSettings.h_scale_base),
                                  "blue",
                                  0,
                                  self.window,
                                  100))

        self.enemies.append(Enemy(False,
                                  False,
                                  ShipType(ShipType.ENEMY),
                                  int(gameSettings.width * 0.8 - scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2),
                                  int(30 * gameSettings.h_scale_base),
                                  "ghost",
                                  0,
                                  self.window,
                                  100))

    def spawnOneAlly(self):
        self.allies.append(Ally(ShipType(ShipType.ENEMY),
                                int(gameSettings.width / 2 - scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2),
                                int(30 * gameSettings.h_scale_base),
                                "yellow",
                                0,
                                self.window,
                                100,
                                False))


