import pygame.mixer

pygame.mixer.init()
cannonFireFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/cannonFire.mp3")
deathFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/death.mp3")
hitFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/hitEffect.mp3")
newLevelFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/newLevel.mp3")
shipCollisionFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/shipCollision.mp3")
freezeFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/freeze.mp3")
poisonFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/poison.mp3")
blindFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/blind.mp3")
thunderStrikeFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/thunderStrike.mp3")
vulnerableFX: pygame.mixer.Sound = pygame.mixer.Sound("assets/audio/vulnerable.mp3")