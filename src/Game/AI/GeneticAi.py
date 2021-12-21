import numpy as np
from Game.Board import GameBoard
from Game.AI.AlphaBetaAi import AlphaBetaAi


class GeneticAI(AlphaBetaAi):
    def __init__(self, weights: np.ndarray = None):
        """A genetic ai based on weights"""
        if weights is None:
            weights = np.random.random((8, 8))
        self.board_weights = weights

    def _generate_move(self, board: GameBoard) -> tuple[int, int]:
        """Make a move based on the weights"""
        scores = {}
        valid_positions = board.get_valid_positions()

        if len(valid_positions) == 1:
            return list(valid_positions.keys())[0]

        for move in valid_positions.keys():
            test_board = GameBoard(board)
            x, y = self.to_index(*move)
            test_board.place(x, y)
            result = np.sum(np.dot(self.board_weights,
                            test_board.board * -test_board.current_turn.value))
            scores[move] = result

        if len(scores) == 0:
            return None

        move = max(scores.items(), key=lambda x: x[1])[0]
        return move

    def get_weights(self) -> np.ndarray:
        """Get the weights of the AI"""
        return self.board_weights
