import pygame

from util import FPS
from ScreenController import ScreenController
from util import WIDTH, HEIGHT


def main_loop(clock: pygame.time.Clock) -> None:
    quit_game: bool = False
    while not quit_game:
        window.fill((0, 0, 0))
        quit_game = screenController.process_game_update()
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    print("Game ended")


pygame.display.set_caption("Pirate's Treasure")

# Main window config
window = pygame.display.set_mode((WIDTH, HEIGHT))
screenController: ScreenController = ScreenController(window)

main_loop(pygame.time.Clock())