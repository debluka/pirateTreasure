class MainGameState:
    def __init__(self):
        self.isPaused: bool = False
        self.level = 0
        self.WAVE_SIZE: int = 5
        self.score = 0
        self.money = 0


mainGameState: MainGameState = MainGameState()
