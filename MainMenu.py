from pygame import Surface

from GameScreen import GameScreen
from ScreenType import ScreenType
from TextButton import TextButton


class MainMenu(GameScreen):
    def __init__(self, window: Surface):
        super().__init__(ScreenType(ScreenType.MAIN_MENU), window)
        TOP_OFFSET: int = 270
        BUTTON_SPACING: int = 60
        self.buttons: dict[str, TextButton] = {"Start game": TextButton(self. window, TOP_OFFSET, "Start game"),
                                               "Leaderboard": TextButton(self.window, TOP_OFFSET + BUTTON_SPACING, "Leaderboard"),
                                               "Options": TextButton(self.window, TOP_OFFSET + BUTTON_SPACING * 2, "Options"),
                                               "Exit": TextButton(self.window, TOP_OFFSET + BUTTON_SPACING * 3, "Exit")}

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
                    # case "Options":
                    #     self.nextScreen = ScreenType.OPTIONS_MENU
                    case "Exit":
                        return True

    def render(self) -> None:
        self.window.fill((14, 194, 249))
        for _, button in self.buttons.items():
            button.draw()

    def click_handler(self, button: int, position: tuple[int, int]) -> None:
        pass

    def mouse_move_handler(self, button: int, position: tuple[int, int]) -> None:
        pass

    def keyboard_hold_button_handler(self, keys: tuple[bool, ...]) -> None:
        pass

    def keyboard_press_button_handler(self, key: int) -> None:
        pass

    def window_resize_handler(self) -> None:
        for _, button in self.buttons.items():
            button.resize()
