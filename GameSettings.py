class GameSettings():    
    def __init__(self):
        self.FPS = 60
        self.PLAYER_BASE_VELOCITY = 5
        self.LASER_BASE_VELOCITY = 5
        self.ENEMY_BASE_VELOCITY = 1

        self.BASE_WIDTH = 750
        self.BASE_HEIGHT = 750

        self.width = 750
        self.height = 750

        self.w_scale = 1.0
        self.h_scale = 1.0
        self.w_scale_base = 1.0
        self.h_scale_base = 1.0


gameSettings = GameSettings()
