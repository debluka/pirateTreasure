import pygame
import os
import random

from Enemy import Enemy
from Player import Player
from util import WIDTH, HEIGHT, collide

pygame.font.init()

# Window config
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirate's Treasure")

# Background
BG = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "bg.png")), (WIDTH, HEIGHT))


# Main loop
def main():
    # Initialization
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 25)
    lost_font = pygame.font.SysFont("comicsans", 30)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.fill((14, 194, 249))
        # WIN.blit(BG, (0, 0))
        # Lives and level display
        lives_label = main_font.render(f"Lives: {lives}", True, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", True, (255, 255, 255))

        # Enemies and player's character
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        # Lose screen
        if lost:
            lost_label = lost_font.render("GAME OVER", True, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        # Loose condition
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        # Enemy spawning
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(
                    50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # Window close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Player Movement
        player.move_lasers(-laser_vel, enemies)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Enemy updating
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            # Shooting
            if random.randrange(0, 2 * 60) == 1:
                enemy.shoot()

            # Collision checking
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                # If enemy gets to the bottom of the screen we also lose lives
                lives -= 1
                enemies.remove(enemy)


# Renders the main menu
def main_menu():
    title_font = pygame.font.SysFont("comicsans", 50)
    run = True
    while run:
        WIN.fill((14, 194, 249))
        # WIN.blit(BG, (0, 0))
        title_label = title_font.render(
            "Click to start the game", True, (255, 255, 255))
        WIN.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()


# Start of the game
main_menu()
