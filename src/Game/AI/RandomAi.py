from Core.Constants import AI_MOVE_KEY
from Game.AI.Ai import AI
from Game.Board import GameBoard
from random import choice


class RandomAi(AI):

    def get_move(self, board: GameBoard, result_dict: dict = None) -> tuple[int, int]:
        valid_positions = board.get_valid_positions(board.current_turn)
        result_dict[AI_MOVE_KEY] = choice(tuple(valid_positions.keys()))
