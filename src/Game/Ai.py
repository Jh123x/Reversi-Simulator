from Game.Board import GameBoard

class AI(object):
    def __init__(self):
        super().__init__()


    def alphaBetaPrune(self, board: GameBoard, depth: int, alpha: int, beta: int, current_turn: int) -> int:
        """
        Returns the best move for the AI.
        """

        # Valid moves
        valid_positions = board.get_valid_positions()

        if depth == 0 or len(valid_positions) == 0:
            return alpha if current_turn == 1 else beta

        
        
        if current_turn == 1:
            value = -float("inf")
            for position in valid_positions:
                cpy_board = GameBoard(board)
                cpy_board.place(position)
                value = max(value, self.alphaBetaPrune(cpy_board, depth - 1, alpha, beta, 2))
                

        

        # Start the alpha beta search

    
    def getMove(self, board: GameBoard, current_turn: int) -> tuple[int, int]:
        """
        Returns the position of the move that the AI will make.
        """
        
        # Start the alpha beta search
        pass
        