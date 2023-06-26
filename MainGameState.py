class MainGameState:
    def __init__(self):
        self.isPaused: bool = False
        self.level = 0
        self.WAVE_SIZE: int = 5
        self.score = 0
        self.money = 0

        self.HEALTH_PER_UPGRADE: int = 10
        self.VELOCITY_PER_UPGRADE: int = 1
        self.HEALTH_REGENERATION_PER_UPGRADE: float = 0.01
        self.ARMOR_PER_UPGRADE: int = 20
        self.PROJECTILE_SPEED_PER_UPGRADE: int = 2


mainGameState: MainGameState = MainGameState()
