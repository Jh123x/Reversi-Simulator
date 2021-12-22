from Core.Constants import AI_MOVE_KEY
from Core.Index import Index
from Game.Board import GameBoard


class AI(object):

    def to_index(self, x: int, y: int) -> tuple[Index, Index]:
        """
        Converts the coordinates to Index
        """
        return Index.from_zero_based(x), Index.from_zero_based(y)

    def generate_move(self, board: GameBoard) -> None:
        """Generate moves for the AI"""
        raise NotImplementedError()

    def get_move(self, board: GameBoard, result_dict: dict = None) -> None:
        """Get the next move of the AI and place it to the dict"""
        move = self.generate_move(board)
        if move is None:
            return
        if result_dict is not None:
            result_dict[AI_MOVE_KEY] = move
