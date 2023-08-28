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


class MainGame(GameScreen):
    def __init__(self, window: pygame.Surface):
        super().__init__(ScreenType(ScreenType.MAIN_GAME), window)
        self.lives: int = 5
        self.enemies: [Enemy] = []
        self.allies: [Ally] = []
        self.waveLength: int = 0
        self.player = Player(self.window, ShipType(ShipType.PLAYER), gameSettings.width / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE3).get_width() / 2, gameSettings.height / 2 - scaleSurfaceBase(Textures.PLAYER_IMAGE3).get_height() / 2, gameSettings.PLAYER_BASE_VELOCITY)
        self.gameLost: bool = False
        self.lostCount: int = 0
        self.animations: list[ExplosionAnimation] = []

        self.upgradeMenu: UpgradeMenu = UpgradeMenu(self.window)
        self.waterColor: (int, int, int) = (14, 194, 249)

        self.base_water_color = '#3D897B'
        self.high_light_color = '#FFFFFF'
        self.points: [[pygame.Vector2, int]] = []
        self.populate()
        self.playerParticles = ParticlePrinciple(self.window)


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

            self.checkEndgameConditions()

            # Endgame text timer
            if self.gameLost:
                if self.lostCount > gameSettings.FPS * 3:
                    saveScore(gameSettings.username, mainGameState.score)
                    mainGameState.reset()
                    playerUpgrades.reset()
                    pygame.mixer.music.stop()
                    self.nextScreen = ScreenType.MAIN_MENU
                    return True
                else:
                    return False

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


        # Enemies and player's character
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
                origin = pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() / 2)
                # originalPoint = pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.7)
                # point = pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.7)
                # point = rotate_point(point, self.player.rotate, origin)
                # rotate_point(pygame.Vector2(self.player.x + self.player.get_width() / 2, self.player.y + self.player.get_height() * 0.7), self.player.rotate, origin)
                # left
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
        for ally in self.allies:
            ally.resize()

        self.points = []
        self.populate()


    def checkEndgameConditions(self) -> None:
        if self.lives <= 0 or self.player.health <= 0:
            if not self.gameLost:
                pygame.mixer.Sound.play(deathFX)
            self.gameLost = True
            self.lostCount += 1

    def updatePlayer(self) -> None:
        mainGameState.pX = self.player.x + self.player.get_width() / 2
        mainGameState.pY = self.player.y + self.player.get_height() / 2

        self.player.move_lasers(self.allies, self.enemies, self.animations)
        self.player.updateEffects()
        self.player.updateHealthAndArmor()

    def updateEnemies(self) -> None:
        if len(self.enemies) == 0:
            self.goToNextLevel()

        for enemy in self.enemies[:]:
            enemy.updateParticles()
            enemy.updateEffects()
            enemy.move(self.player.lasers)
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
                mainGameState.score += int(10 + mainGameState.level * 0.3)
                mainGameState.money += 5
            elif enemy.y + enemy.get_height() > gameSettings.height - gameSettings.minY - gameSettings.baseHeight:
                # If enemy gets to the bottom of the screen we also lose lives
                self.lives -= 1
                self.enemies.remove(enemy)

    def updateAllies(self) -> None:
        for ally in self.allies[:]:
            ally.updateParticles()
            ally.updateEffects()
            ally.move()
            ally.move_lasers(self.player)

            # Shooting
            if random.randrange(0, 2 * 60) == 1:
                ally.shoot()

            # Collision checking
            if collide(ally, self.player):
                pygame.mixer.Sound.play(shipCollisionFX)
                self.player.health -= 50
                self.allies.remove(ally)
                self.animations.append(ExplosionAnimation(int(ally.x + ally.get_width() / 2), int(ally.y + ally.get_height() / 2), self.window))
            elif ally.y + ally.get_height() > gameSettings.height - gameSettings.minY - gameSettings.baseHeight:
                self.allies.remove(ally)

    def updateAnimations(self):
        for animation in self.animations:
            animation.update()
            if animation.isDone:
                self.animations.remove(animation)


    def goToNextLevel(self) -> None:
        mainGameState.level += 1
        if mainGameState.level % 5 == 0 and mainGameState.level > 1:
            pygame.mixer.Sound.play(thunderStrikeFX)
            pygame.mixer.music.load('assets/audio/thunderAmbient.mp3')
            pygame.mixer.music.play(-1)
            self.waterColor = (11, 41, 46)
        elif mainGameState.level % 5 == 1 and mainGameState.level > 5:
            self.waterColor = (14, 194, 249)
            pygame.mixer.music.load('assets/audio/ambient.mp3')
        if mainGameState.level > 1:
            pygame.mixer.Sound.play(newLevelFX)
        self.player.armor = self.player.max_armor
        self.waveLength += mainGameState.WAVE_SIZE
        for i in range(self.waveLength):
            enemySpawnTypePool = ["red", "blue", "green"]
            if mainGameState.level % 5 == 0 and mainGameState.level > 1:
                enemySpawnTypePool.append("ghost")
            elif mainGameState.level % 5 == 1 and mainGameState.level > 5:
                enemySpawnTypePool.remove("ghost")

            base_probability = 0.10
            increase_factor = 0.05
            probability = min(base_probability + (increase_factor * (mainGameState.level)), 0.3)
            isTracker: bool = True if random.random() < probability else False
            isDodger: bool = True if random.random() < probability else False

            if isTracker is True:
                isDodger = False

            enemy = Enemy(isTracker,
                          isDodger,
                          ShipType(ShipType.ENEMY),
                          random.randrange(math.ceil(scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2), math.ceil(gameSettings.width - scaleSurfaceBase(Textures.RED_SHIP1).get_width())),
                          random.randrange(math.ceil(-2500 * gameSettings.h_scale_base), math.ceil(-1500 * gameSettings.h_scale_base)),
                          random.choice(enemySpawnTypePool),
                          gameSettings.ENEMY_BASE_VELOCITY * gameSettings.h_scale_base,
                          self.window,
                          10 * mainGameState.level)
            self.enemies.append(enemy)

        for i in range(math.ceil(mainGameState.level / 5)):
            ally = Ally(ShipType(ShipType.ENEMY),
                        random.randrange(math.ceil(scaleSurfaceBase(Textures.RED_SHIP1).get_width() / 2), math.ceil(gameSettings.width - scaleSurfaceBase(Textures.RED_SHIP1).get_width())),
                        random.randrange(math.ceil(-2500 * gameSettings.h_scale_base), math.ceil(-1500 * gameSettings.h_scale_base)),
                        "yellow",
                        gameSettings.ENEMY_BASE_VELOCITY * gameSettings.h_scale_base,
                        self.window,
                        10)
            self.allies.append(ally)
