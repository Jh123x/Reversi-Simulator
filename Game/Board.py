import numpy as np
from Core.Index import Index
from Core.Constants import WIDTH, HEIGHT, DIRECTIONS, STARTING_POSITIONS
from Core.Exceptions import OutOfBoundsException, AlreadyTakenException, InvalidPositionException

class GameBoard(object):

    def __init__(self, board = None, current_turn:int = False):
        """Board object to keep track of game information"""

        #Store the current player turn
        self._current_turn = current_turn

        #Store the board
        if board == None:
            self._init_board()
        else:
            self._board = np.copy(board.board)

    @property
    def current_turn(self):
        """Get the current player's turn
            Either Player 1 or 2
        """
        return int(self._current_turn) + 1

    @property
    def board(self):
        """Get the current board"""
        return self._board

    def _set_position(self, x:int, y:int, piece:int):
        """Place the token at the x,y position of the board (0 based)"""
        self._board[x][y] = piece

    def _get_position(self, x:int, y:int) -> int:
        return int(self._board[x][y])

    def _init_board(self):
        """Restore the board to the initial state"""
        self._board = np.zeros((8,8))
        for x, y, player in STARTING_POSITIONS:
            self._set_position(x,y,player)

    def is_position_valid(self, x:int, y:int) -> bool:
        return 0 <= x < WIDTH and 0 <= y < HEIGHT

    def place(self, x:Index, y:Index):
        """Place the piece at the position"""

        #Check if the values within range
        if not self.is_position_valid(x.zero_based_index, y.zero_based_index):
            raise OutOfBoundsException(f"({x},{y})")

        #Check if the position is already taken
        if self._get_position(x.zero_index, y.zero_index) != 0:
            raise AlreadyTakenException(f"({x},{y})", self.current_turn)

        #Check if the move is valid
        is_valid, pieces_shifted = self.is_valid(x.zero_based_index, y.zero_based_index, self.current_turn)
        if not is_valid:
            raise InvalidPositionException(f"({x}, {y})")

        #Change the mutated pieces
        for mutate_x, mutated_y in pieces_shifted:
            self._set_position(mutate_x, mutated_y, self.current_turn)
        
        #Place the piece on the board
        self._set_position(x.zero_index, y.zero_index, self.current_turn)

        #Toggle player turn
        self._current_turn = not self._current_turn


    def is_valid(self, x_pos:int, y_pos:int, player:int):
        """Check if the move is valid
            x_pos and y_pos are zero based
        """

        applied = []

        #Check if any tile will change color
        for x, y in DIRECTIONS:

            mul = 1
            curr_x, curr_y = x_pos + mul * x,  y_pos + mul * y
            
            #While position is valid look for next valid position
            while self.is_position_valid(curr_x, curr_y):

                #If the flip position is found
                if self._get_position(curr_x, curr_y) == player:
                    break

                #If the position is empty
                elif self._get_position(curr_x, curr_y) == 0:
                    curr_x = -1
                    break

                mul += 1
                curr_x, curr_y = x_pos + mul * x,  y_pos + mul * y

            # Check if final position after end of loop is valid
            if self.is_position_valid(curr_x, curr_y):

                # Add positions between into the applied section
                for m in range(1, mul):
                    applied.append((x_pos + m * x, y_pos + m * y))

        return len(applied) > 0, applied

    def __repr__(self):
        """String representation of the current board"""
        acc = []
        for row in range(8):
            ac2 = []
            for col in range(8):
                pos = int(self._get_position(col, row))
                ac2.append(str(pos))

            res = " ".join(ac2)
            acc.append(res)

        return "\n".join(acc)



        
        
