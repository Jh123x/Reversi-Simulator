from Game.Board import GameBoard

class AI(object):
    def get_move(self, board: GameBoard, result_dict: dict = None):
        raise NotImplementedError()