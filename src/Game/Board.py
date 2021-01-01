import numpy as np
from src.Core.Index import Index
from src.Core.Constants import WIDTH, HEIGHT, DIRECTIONS, STARTING_POSITIONS
from src.Core.Exceptions import OutOfBoundsException, AlreadyTakenException, InvalidPositionException


class GameBoard(object):

    def __init__(self, board=None, current_turn: bool = False):
        """Board object to keep track of game information"""

        # Store the current player turn
        self._current_turn = current_turn

        # Store the board
        if board is None:
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

    def set_board(self, board):
        """Set the current board to the input board for testing purposes"""
        self._board = board

    def _set_position(self, x: int, y: int, piece: int):
        """Place the token at the x,y position of the board (0 based)"""
        self._board[x][y] = piece

    def get_position(self, x: int, y: int) -> int:
        """Get the current value at the position (x,y)"""
        return int(self._board[x][y])

    def _init_board(self):
        """Restore the board to the initial state"""
        self._board = np.zeros((8, 8))
        for x, y, player in STARTING_POSITIONS:
            self._set_position(x, y, player)

    @staticmethod
    def is_position_valid(x: int, y: int) -> bool:
        """Check if the position is valid"""
        return 0 <= x < WIDTH and 0 <= y < HEIGHT

    def get_valid_positions(self) -> dict:
        """Get the possible positions for the player to move"""
        valid = {}
        for x in range(8):
            for y in range(8):
                is_valid, applied = self.is_valid(x, y, self.current_turn)
                if is_valid:
                    valid[(x, y)] = applied
        return valid

    def place(self, x: Index, y: Index) -> bool:
        """Place the piece at the position
            Return if the move has been successfully executed
        """

        # Check if the values within range
        if not self.is_position_valid(x.zero_based_index, y.zero_based_index):
            raise OutOfBoundsException(f"({x},{y})")

        # Check if the position is already taken
        if self.get_position(x.zero_index, y.zero_index) != 0:
            raise AlreadyTakenException(f"({x},{y})", self.current_turn)

        # Get valid positions
        valid_pos = self.get_valid_positions()

        # Check if other player has valid positions to move to
        if len(valid_pos) == 0:
            self._current_turn = not self._current_turn
            return False

        # Check if the move is valid
        changed = valid_pos.get((x.zero_based_index, y.zero_based_index), None)
        if not changed:
            raise InvalidPositionException(f"({x}, {y})")

        # Change the mutated pieces
        for mutate_x, mutated_y in changed:
            self._set_position(mutate_x, mutated_y, self.current_turn)
        
        # Place the piece on the board
        self._set_position(x.zero_index, y.zero_index, self.current_turn)

        # Toggle player turn
        self._current_turn = not self._current_turn

        return True

    def is_valid(self, x_pos: int, y_pos: int, player: int):
        """Check if the move is valid
            x_pos and y_pos are zero based
        """

        applied = []

        # Check if any tile will change color
        for x, y in DIRECTIONS:

            mul = 1
            curr_x, curr_y = x_pos + mul * x,  y_pos + mul * y
            
            # While position is valid look for next valid position
            while self.is_position_valid(curr_x, curr_y):

                # If the flip position is found
                if self.get_position(curr_x, curr_y) == player:
                    break

                # If the position is empty
                elif self.get_position(curr_x, curr_y) == 0:
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
                pos = int(self.get_position(col, row))
                ac2.append(str(pos))

            res = " ".join(ac2)
            acc.append(res)

        return "\n".join(acc)
