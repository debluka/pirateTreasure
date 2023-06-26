import pygame
import os

PLAYER_IMAGE3: pygame.Surface = pygame.image.load(os.path.join("assets", "player_ship3.png"))
PLAYER_IMAGE2: pygame.Surface = pygame.image.load(os.path.join("assets", "player_ship2.png"))
PLAYER_IMAGE1: pygame.Surface = pygame.image.load(os.path.join("assets", "player_ship1.png"))

RED_SHIP3: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_red3.png"))
RED_SHIP2: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_red2.png"))
RED_SHIP1: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_red1.png"))

GREEN_SHIP3: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_green3.png"))
GREEN_SHIP2: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_green2.png"))
GREEN_SHIP1: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_green1.png"))

BLUE_SHIP3: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_blue3.png"))
BLUE_SHIP2: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_blue2.png"))
BLUE_SHIP1: pygame.Surface = pygame.image.load(os.path.join("assets", "enemy_blue1.png"))

RED_LASER: pygame.Surface = pygame.image.load(os.path.join("assets", "red_projectile.png"))
GREEN_LASER: pygame.Surface = pygame.image.load(os.path.join("assets", "green_projectile.png"))
BLUE_LASER: pygame.Surface = pygame.image.load(os.path.join("assets", "blue_projectile.png"))
CANNONBALL: pygame.Surface = pygame.image.load(os.path.join("assets", "cannonBall.png"))