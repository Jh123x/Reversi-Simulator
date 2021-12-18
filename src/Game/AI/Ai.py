from Game.Board import GameBoard
from Core.Index import Index

class AI(object):

    def to_index(self, x: int, y: int) -> tuple[Index, Index]:
        """
        Converts the coordinates to Index
        """
        return Index.from_zero_based(x), Index.from_zero_based(y)

    def get_move(self, board: GameBoard, result_dict: dict = None) -> tuple[int, int]:
        raise NotImplementedError()
