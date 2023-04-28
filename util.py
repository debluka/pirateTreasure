WIDTH, HEIGHT = 750, 750
FPS = 60
PLAYER_BASE_VELOCITY = 5
LASER_BASE_VELOCITY = 5
ENEMY_BASE_VELOCITY = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None
