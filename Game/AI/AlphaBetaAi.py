from Game.AI.Ai import AI
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


def get_next_turn(current_turn: PlayerTurn):
    return PlayerTurn.BLACK if current_turn == PlayerTurn.WHITE else PlayerTurn.WHITE


def base_prune(board: GameBoard) -> int:
    """Base case pruning"""
    black, white = board.get_score()
    num_moves = board.get_valid_positions()
    score = black - white
    if board.turns_taken < 30:
        return score
    return score - num_moves


class AlphaBetaAi(AI):

    def __init__(self, depth: int = 7):
        """The alpha beta pruning AI"""
        super().__init__()
        self.depth = depth

    def alphaBetaPrune(self, board: GameBoard, depth: float, alpha: float, beta: int) -> int:
        """
        Returns the best move for the AI.
        """
        # Valid moves
        valid_positions = board.get_valid_positions()
        current_turn = board.current_turn

        if depth == 0 or len(valid_positions) == 0:
            return base_prune(board)

        # Alpha for black
        if current_turn == PlayerTurn.BLACK:
            value = -float("inf")
            for position in valid_positions:
                cpy_board = GameBoard(board)
                x, y = self.to_index(*position)
                cpy_board.place(x, y)
                value = max(value, self.alphaBetaPrune(
                    cpy_board, depth - 1, alpha, beta))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value

        # Beta for white
        value = float("inf")
        for position in valid_positions:
            cpy_board = GameBoard(board)
            x, y = self.to_index(*position)
            cpy_board.place(x, y)
            value = max(value, self.alphaBetaPrune(
                cpy_board, depth - 1, alpha, beta))
            if value <= alpha:
                break
            alpha = min(alpha, value)
        return value

    def generate_move(self, board: GameBoard) -> tuple[int, int]:
        """
        Returns the position of the move that the AI will make.
        """

        current_turn = board.current_turn
        assert current_turn == PlayerTurn.WHITE
        curr_contender = None
        curr_score = None

        # Start the alpha beta search
        for position in board.get_valid_positions().keys():
            cpy = GameBoard(board)
            x, y = self.to_index(*position)
            cpy.place(x, y)
            score = self.alphaBetaPrune(
                cpy,
                depth=self.depth,
                alpha=-float("inf"),
                beta=float("inf")
            )

            if curr_contender is None or score < curr_score:
                curr_contender = position
                curr_score = score

        return curr_contender
