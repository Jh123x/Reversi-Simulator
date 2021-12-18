from Core.Constants import AI_MOVE_KEY
from Core.Index import Index
from Game.AI.Ai import AI
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


class AlphaBetaAi(AI):
    def get_next_turn(self, current_turn: PlayerTurn):
        PlayerTurn.BLACK if current_turn == PlayerTurn.WHITE else PlayerTurn.WHITE

    def alphaBetaPrune(self, board: GameBoard, depth: int, alpha: int, beta: int) -> int:
        """
        Returns the best move for the AI.
        """

        # Valid moves
        valid_positions = board.get_valid_positions()
        current_turn = board.current_turn

        if depth == 0 or len(valid_positions) == 0:
            black, white = board.get_score()
            return black - white

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

    def to_index(self, x: int, y: int) -> tuple[Index, Index]:
        """
        Converts the coordinates to Index
        """
        return Index.from_zero_based(x), Index.from_zero_based(y)

    def get_move(self, board: GameBoard, result_dict: dict = None) -> tuple[int, int]:
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
                cpy, depth=6, alpha=-float("inf"), beta=float("inf"))

            if curr_contender is None or score < curr_score:
                curr_contender = position
                curr_score = score

        if result_dict is not None:
            result_dict[AI_MOVE_KEY] = curr_contender

        return curr_contender