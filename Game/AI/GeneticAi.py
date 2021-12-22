from typing import Optional

import numpy as np

from Game.AI.AlphaBetaAi import AlphaBetaAi
from Game.Board import GameBoard


class GeneticAI(AlphaBetaAi):
    def __init__(self, weights: np.ndarray = None):
        """A genetic ai based on weights"""
        super().__init__()
        if weights is None:
            weights = np.random.random((8, 8))

        self.weights = weights

    def generate_move(self, board: GameBoard) -> Optional[tuple[int, int]]:
        """Make a move based on the weights"""
        scores = {}
        valid_positions = board.get_valid_positions()

        if len(valid_positions) == 1:
            return list(valid_positions.keys())[0]

        for move in valid_positions.keys():
            test_board = GameBoard(board)
            x, y = self.to_index(*move)
            test_board.place(x, y)
            result = np.sum(
                np.dot(
                    self.weights,
                    test_board.board * -test_board.current_turn.value
                )
            )
            scores[move] = result

        if len(scores) == 0:
            return None

        move = max(scores.items(), key=lambda i: i[1])[0]
        return move

    def get_model(self) -> np.ndarray:
        """Get the weights of the AI"""
        return self.weights
