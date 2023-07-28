import pygame
from pygame import Surface

from Checkbox import Checkbox
from GameScreen import GameScreen
from OptionsButton import OptionsButtonType
from ScreenType import ScreenType
from TextButton import TextButton


class OptionsMenu(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(ScreenType(ScreenType.MAIN_MENU), window)
        TOP_OFFSET: int = 270
        BUTTON_SPACING: int = 60
        self.buttons: dict[str, Checkbox] = {"Toggle sound": Checkbox(self. window, OptionsButtonType.SOUND_ENABLED, True, TOP_OFFSET, "Toggle sound"),
                                             "Resizable screen": Checkbox(self. window, OptionsButtonType.SCREEN_RESIZE, True, TOP_OFFSET + BUTTON_SPACING, "Resizable screen")}

    # Renders the main menu
    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

        for key, button in self.buttons.items():
            if button.clicked is True:
                match key:
                    case "Start game":
                        self.nextScreen = ScreenType.MAIN_GAME
                    case "Leaderboard":
                        self.nextScreen = ScreenType.LEADERBOARD
                    case "Options":
                        print("asdf")
                    case "Exit":
                        return True

    def render(self) -> None:
        self.window.fill((14, 194, 249))
        for _, button in self.buttons.items():
            button.draw()

    def click_handler(self, event: pygame.event.Event) -> None:
        for key, button in self.buttons.items():
            button.click_handler(event)

    def window_resize_handler(self) -> None:
        for _, button in self.buttons.items():
            button.resize()
