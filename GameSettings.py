import pygame


class GameSettings:
    def __init__(self):
        self.FPS: int = 60
        self.PLAYER_BASE_VELOCITY: int = 5
        self.PLAYER_LASER_BASE_DAMAGE: int = 10
        self.ENEMY_LASER_BASE_DAMAGE: int = 10
        self.LASER_BASE_VELOCITY: int = 5
        self.ENEMY_BASE_VELOCITY: int = 1

        self.BASE_WIDTH: int = 750
        self.BASE_HEIGHT: int = 750
        self.prevWidth = 750
        self.prevHeight = 750

        self.width: int = 750
        self.height: int = 750

        self.w_scale: float = 1.0
        self.h_scale: float = 1.0
        self.w_scale_base: float = 1.0
        self.h_scale_base: float = 1.0
        self.username: str = ''

        self.blindCircleBaseRadius: int = 250
        self.resizableScreen: bool = True
        self.soundEnabled: bool = True
        self.fullScreen: bool = False

        self.moveUpBinding: int = pygame.K_w
        self.moveDownBinding: int = pygame.K_s
        self.moveLeftBinding: int = pygame.K_a
        self.moveRightBinding: int = pygame.K_d
        self.shootBinding: int = pygame.K_SPACE


gameSettings: GameSettings = GameSettings()
