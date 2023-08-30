import pygame

from GameSettings import gameSettings


class MainGameState:
    def __init__(self):
        self.isPaused: bool = False
        self.isBonusLevel: bool = False
        self.level = 0
        self.WAVE_SIZE: int = 4
        self.score: int = 0
        self.money: int = 0

        self.limitedVision: bool = False
        self.pX: int = 0
        self.pY: int = 0

        self.yOffset: int = 0

        self.HEALTH_PER_UPGRADE: int = 10
        self.VELOCITY_PER_UPGRADE: int = 1
        self.HEALTH_REGENERATION_PER_UPGRADE: float = 0.01
        self.ARMOR_PER_UPGRADE: int = 20
        self.PROJECTILE_SPEED_PER_UPGRADE: int = 1
        self.PROJECTILE_DAMAGE_PER_UPGRADE: int = 5
        self.cameraRect: pygame.Rect = pygame.Rect(0, 0, gameSettings.width, gameSettings.height)

    def reset(self) -> None:
        self.isPaused: bool = False
        self.level = 0
        self.score = 0
        self.money = 0

        self.limitedVision: bool = False
        self.pX: int = 0
        self.pY: int = 0
        self.yOffset = 0


mainGameState: MainGameState = MainGameState()
