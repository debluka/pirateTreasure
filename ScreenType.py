from enum import IntEnum


class ScreenType(IntEnum):
    MAIN_MENU: int = 1
    MAIN_GAME: int = 2
    OPTIONS_MENU: int = 3
    LEADERBOARD: int = 4
    WELCOME_SCREEN: int = 5
    CREDITS_SCREEN: int = 6
    HOW_TO_PLAY_SCREEN: int = 7
    TUTORIAL: int = 8
