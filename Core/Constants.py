from Game.PlayerEnum import PlayerTurn

WIDTH = 8
HEIGHT = 8
STARTING_POSITIONS = (
    (3, 3, PlayerTurn.WHITE),
    (3, 4, PlayerTurn.BLACK),
    (4, 3, PlayerTurn.BLACK),
    (4, 4, PlayerTurn.WHITE),
)
DIRECTIONS = (
    (-1, 1),
    (0, 1),
    (1, 1),
    (-1, 0),
    (1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
)

AI_MOVE_KEY = 'move'
