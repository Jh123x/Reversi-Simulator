import enum

class State(enum.Enum):
    """
    Enum for the different states of the GUI.
    """
    TWO_PLAYER = 0
    MENU = 1
    AGAINST_AI = 2
    GAME_OVER = 3
    QUIT = -1