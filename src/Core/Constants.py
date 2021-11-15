from Game.PlayerEnum import PlayerTurn


WIDTH = 8
HEIGHT = 8
STARTING_POSITIONS = (
            (3, 3, PlayerTurn.BLACK),
            (3, 4, PlayerTurn.WHITE),
            (4, 3, PlayerTurn.WHITE),
            (4, 4, PlayerTurn.BLACK),
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