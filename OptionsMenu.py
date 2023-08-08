import pygame
from pygame import Surface

from Checkbox import Checkbox
from GameScreen import GameScreen
from GameSettings import gameSettings
from OptionsButton import OptionsButtonType
from RebindButton import RebindButton
from RebindButtonType import RebindButtonType
from ScreenType import ScreenType
from TextButton import TextButton
from fonts import main_font


class OptionsMenu(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(ScreenType(ScreenType.MAIN_MENU), window)
        TOP_OFFSET: int = 100
        BUTTON_SPACING: int = 60
        self.checboxButtons: dict[str, Checkbox] = {"Toggle music": Checkbox(self.window, OptionsButtonType.SOUND_ENABLED, gameSettings.soundEnabled, TOP_OFFSET, "Toggle music"),
                                                    "Resizable screen": Checkbox(self.window, OptionsButtonType.SCREEN_RESIZE, gameSettings.resizableScreen, TOP_OFFSET + BUTTON_SPACING, "Resizable screen"),
                                                    "Full-screen": Checkbox(self.window, OptionsButtonType.FULL_SCREEN, gameSettings.fullScreen, TOP_OFFSET + BUTTON_SPACING * 2, "Full-screen")}
        self.rebindButtons: dict[str, RebindButton] = {"moveUp": RebindButton(self.window, RebindButtonType.UP, TOP_OFFSET + BUTTON_SPACING * 4, "Move up"),
                                                       "moveDown": RebindButton(self.window, RebindButtonType.DOWN, TOP_OFFSET + BUTTON_SPACING * 5, "Move down"),
                                                       "moveLeft": RebindButton(self.window, RebindButtonType.LEFT, TOP_OFFSET + BUTTON_SPACING * 6, "Move left"),
                                                       "moveRight": RebindButton(self.window, RebindButtonType.RIGHT, TOP_OFFSET + BUTTON_SPACING * 7, "Move right"),
                                                       "shoot": RebindButton(self.window, RebindButtonType.SHOOT, TOP_OFFSET + BUTTON_SPACING * 8, "Shoot")}
        self.selectedRebindButtonType: RebindButtonType | None = None
        self.buttons: dict[str, TextButton] = {"Back": TextButton(self.window, gameSettings.height - main_font.get_height() - 20, "Back"),}

    # Renders the main menu
    def update(self) -> bool:
        if self.nextScreen is not None:
            return True

        for key, button in self.buttons.items():
            if button.clicked is True:
                match key:
                    case "Back":
                        self.nextScreen = ScreenType.MAIN_MENU

    def render(self) -> None:
        self.window.fill((14, 194, 249))
        for _, button in self.checboxButtons.items():
            button.draw()

        for _, button in self.rebindButtons.items():
            button.draw()

        for _, button in self.buttons.items():
            button.draw()

    def click_handler(self, event: pygame.event.Event) -> None:
        for key, button in self.checboxButtons.items():
            button.click_handler(event)

        self.selectedRebindButtonType = None
        for key, button in self.rebindButtons.items():
            if button.click_handler(event, self.selectedRebindButtonType) is True:
                self.selectedRebindButtonType = button.buttonType

    def window_resize_handler(self) -> None:
        for _, button in self.buttons.items():
            button.resize()

        for _, button in self.checboxButtons.items():
            button.resize()

        for _, button in self.rebindButtons.items():
            button.resize()

    def keyboard_press_button_handler(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            self.nextScreen = ScreenType.MAIN_MENU

        if ((pygame.K_a <= event.key <= pygame.K_z or
            pygame.K_1 <= event.key <= pygame.K_9 or
            event.key in (pygame.K_RETURN, pygame.K_SPACE)) and
            event.key not in (gameSettings.moveUpBinding,
                              gameSettings.moveDownBinding,
                              gameSettings.moveLeftBinding,
                              gameSettings.moveRightBinding,
                              gameSettings.shootBinding)):
            match self.selectedRebindButtonType:
                case RebindButtonType.UP:
                    gameSettings.moveUpBinding = event.key
                case RebindButtonType.DOWN:
                    gameSettings.moveDownBinding = event.key
                case RebindButtonType.LEFT:
                    gameSettings.moveLeftBinding = event.key
                case RebindButtonType.RIGHT:
                    gameSettings.moveRightBinding = event.key
                case RebindButtonType.SHOOT:
                    gameSettings.shootBinding = event.key
