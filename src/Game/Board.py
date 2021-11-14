from typing import Optional
import numpy as np
from Core.Index import Index
from Core.Constants import WIDTH, HEIGHT, DIRECTIONS, STARTING_POSITIONS
from Core.Exceptions import InvalidPositionException


class GameBoard(object):

    DRAW_MESSAGE = "Its a draw"
    WINNER_MESSAGE = "{winner} wins!"

    @staticmethod
    def is_position_valid(x: int, y: int) -> bool:
        """Check if the position is valid"""
        return 0 <= x < WIDTH and 0 <= y < HEIGHT

    def __init__(self, board=None, current_turn: bool = False):
        """Board object to keep track of game information"""

        # Store the current player turn
        self._current_turn = current_turn
        self.turns_taken = 4

        # Store the board
        if board is None:
            self._init_board()
        else:
            self._board = np.copy(board.board)

        self.valid_positions = self.get_valid_positions()

        if len(self.valid_positions) == 0:
            self._current_turn = not self._current_turn
            self.valid_positions = self.get_valid_positions()
            if len(self.valid_positions) == 0:
                self.turns_taken = 64

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

    def get_score(self) -> tuple:
        """Get the score of the game so far
            (Player 1, Player 2)
        """
        return tuple(self._score)

    def _init_board(self):
        """Restore the board to the initial state"""
        # Create the board

        self._board = np.zeros((8, 8))
        # self._board = np.ones((8, 8))
        self._set_position(0, 0, 0)
        self._set_position(0, 1, 0)
        self._set_position(0, 2, 0)
        for x, y, player in STARTING_POSITIONS:
            self._set_position(x, y, player)

        # Starting Score is 2 each
        self._score = [2, 2]

    def get_valid_positions(self, piece: int = None) -> dict:
        """Get the possible positions for the player to move"""
        if piece is None:
            piece = self.current_turn
        valid = {}
        for x in range(WIDTH):
            for y in range(HEIGHT):
                is_valid, applied = self.is_valid(x, y, piece)
                if is_valid:
                    valid[(x, y)] = applied
        return valid

    def place(self, x: Index, y: Index) -> bool:
        """Place the piece at the position
            Return if the move has been successfully executed
        """

        # Check if the move is valid
        changed = self.valid_positions.get(
            (x.zero_based_index, y.zero_based_index), None)
        if not changed:
            raise InvalidPositionException(f"({x}, {y})")

        # Change the mutated pieces
        for mutate_x, mutated_y in changed:
            self._set_position(mutate_x, mutated_y, self.current_turn)

        # Update the score
        self._score[self.current_turn - 1] += len(changed) + 1
        self._score[self.current_turn % 2] -= len(changed)

        # Place the piece on the board
        self._set_position(x.zero_index, y.zero_index, self.current_turn)

        # Toggle player turn
        self._current_turn = not self._current_turn

        # Generate next set of valid moves
        self.valid_positions = self.get_valid_positions()

        # Increment the turn counter
        self.turns_taken += 1
        print(self.turns_taken)

        # Check if other player has valid positions to move to
        if len(self.valid_positions) == 0:
            self._current_turn = not self._current_turn
            self.valid_positions = self.get_valid_positions()
            if len(self.valid_positions) == 0:
                self.turns_taken = 64
            return False

        return True

    def get_winner(self) -> Optional[str]:
        if self.turns_taken < 64:
            return

        if self._score[0] > self._score[1]:
            return f"{self.WINNER_MESSAGE.format(winner='Black')}"

        if self._score[0] < self._score[1]:
            return self.WINNER_MESSAGE.format(winner='White')

        return self.DRAW_MESSAGE

    def is_valid(self, x_pos: int, y_pos: int, player: int):
        """Check if the move is valid
            x_pos and y_pos are zero based
        """

        if self.get_position(x_pos, y_pos) > 0:
            return False, []

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
