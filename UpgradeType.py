from enum import IntEnum


class UpgradeType(IntEnum):
    HEALTH: int = 1
    HEALTH_REGENERATION: int = 2
    ARMOR: int = 3
    VELOCITY: int = 4
    SHOOTING_SPEED: int = 5
    NUMBER_OF_BULLETS: int = 6
    PROJECTILE_COLLISION: int = 7
    PROJECTILE_SPEED: int = 8
    PROJECTILE_DAMAGE: int = 9
