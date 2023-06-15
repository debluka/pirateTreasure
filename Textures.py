import pygame
import os

PLAYER_IMAGE = pygame.image.load(os.path.join("assets", "player_ship.png"))
RED_SHIP = pygame.image.load(os.path.join("assets", "enemy_red.png"))
GREEN_SHIP = pygame.image.load(os.path.join("assets", "enemy_green.png"))
BLUE_SHIP = pygame.image.load(os.path.join("assets", "enemy_blue.png"))

RED_LASER = pygame.image.load(os.path.join("assets", "red_projectile.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "green_projectile.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "blue_projectile.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "cannonBall.png"))