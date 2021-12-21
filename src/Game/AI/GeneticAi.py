import numpy as np
from Game.Board import GameBoard
from Game.AI.AlphaBetaAi import AlphaBetaAi


class GeneticAI(AlphaBetaAi):
    def __init__(self, weights: np.ndarray = np.random.random((8, 8))):
        """A genetic ai based on weights"""
        self.board_weights = weights

    def _generate_move(self, board: GameBoard, result_dict: dict = None) -> None:
        """Make a move based on the weights"""
        scores = {}

        for move in board.get_valid_positions():
            test_board = GameBoard(board)
            x, y = self.to_index(*move)
            test_board.place(x, y)
            result = np.sum(np.dot(self.board_weights, test_board.board)) * \
                test_board.current_turn.value
            scores[move] = result

        return max(scores.items(), key=lambda x: x[1])[0]

    def get_weights(self) -> np.ndarray:
        """Get the weights of the AI"""
        return self.weights
