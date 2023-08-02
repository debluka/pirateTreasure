import pygame

from ScreenController import ScreenController
from GameSettings import gameSettings


def main_loop(clock: pygame.time.Clock) -> None:
    quit_game: bool = False
    while not quit_game:
        window.fill((0, 0, 0))
        quit_game = screenController.process_game_update()
        pygame.display.update()
        clock.tick(gameSettings.FPS)
    pygame.quit()
    print("Game ended")


pygame.display.set_caption("Pirate's Treasure")
pygame.mixer.init()
pygame.mixer.set_num_channels(64)
# Main window config
window: pygame.Surface = pygame.display.set_mode((gameSettings.width, gameSettings.height), pygame.RESIZABLE)
screenController: ScreenController = ScreenController(window)

main_loop(pygame.time.Clock())
