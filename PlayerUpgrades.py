class PlayerUpgrades:
    def __init__(self):
        self.shootingSpeed: int = 0
        self.numberOfBullets: int = 1
        self.laserDamage: int = 10
        self.bulletCollision: int = 0
        self.maxHealth: int = 0
        self.velocity: int = 0
        self.healthRegeneration: int = 0
        self.armor: int = 0
        self.projectileSpeed: int = 0
        self.projectileDamage: int = 0

    def reset(self) -> None:
        self.shootingSpeed: int = 0
        self.numberOfBullets: int = 1
        self.laserDamage: int = 10
        self.bulletCollision: int = 0
        self.maxHealth: int = 0
        self.velocity: int = 0
        self.healthRegeneration: int = 0
        self.armor: int = 0
        self.projectileSpeed: int = 0
        self.projectileDamage: int = 0


playerUpgrades: PlayerUpgrades = PlayerUpgrades()
