from random import choice

from Game.AI.Ai import AI
from Game.Board import GameBoard


class RandomAi(AI):

    def generate_move(self, board: GameBoard, result_dict: dict = None) -> tuple[int, int]:
        valid_positions = board.get_valid_positions(board.current_turn)
        return choice(tuple(valid_positions.keys()))
