from typing import Optional

import numpy as np

from Core.Constants import WIDTH, HEIGHT, DIRECTIONS, STARTING_POSITIONS
from Core.Exceptions import InvalidPositionException
from Core.Index import Index
from Game.PlayerEnum import PlayerTurn


class GameBoard(object):
    DRAW_MESSAGE = "Its a draw"
    WINNER_MESSAGE = "{winner} wins!"

    @staticmethod
    def is_position_valid(x: int, y: int) -> bool:
        """Check if the position is valid"""
        return 0 <= x < WIDTH and 0 <= y < HEIGHT

    def __init__(self, board: 'GameBoard' = None, current_turn: PlayerTurn = PlayerTurn.BLACK):
        """Board object to keep track of game information"""
        self.init_curr_turn = current_turn
        self.init_board = board
        self.reset()

    def change_turn(self) -> None:
        """Change the current player turn"""
        self._current_turn = PlayerTurn.BLACK if self._current_turn == PlayerTurn.WHITE else PlayerTurn.WHITE

    def reset(self):
        """Reset to the start configuration"""
        # Store the current player turn
        self._current_turn = self.init_curr_turn
        self.turns_taken = 4

        # Store the board
        if self.init_board is None:
            self._init_board()
        else:
            self._board = np.copy(self.init_board.board)
            self._score = self.init_board._score.copy()
            self._current_turn = self.init_board.current_turn
            self.init_curr_turn = self.init_board.init_curr_turn
            self.init_board = self.init_board.init_board

        self.valid_positions = self.get_valid_positions()

        if len(self.valid_positions) == 0:
            self.change_turn()
            self.valid_positions = self.get_valid_positions()
            if len(self.valid_positions) == 0:
                self.turns_taken = 64

    @property
    def current_turn(self):
        """Get the current player's turn
            Either Black or White
        """
        return self._current_turn

    @property
    def board(self):
        """Get the current board"""
        return self._board

    def set_board(self, board: np.ndarray, current_turn: PlayerTurn = PlayerTurn.WHITE):
        """Set the current board to the input board for testing purposes"""
        self._board = board
        self.turns_taken = board[board != 0].size
        self._current_turn = current_turn

    def _set_position(self, x: int, y: int, piece: PlayerTurn):
        """Place the token at the x,y position of the board (0 based)"""
        self._board[x][y] = piece.value

    def get_position(self, x: int, y: int) -> int:
        """Get the current value at the position (x,y)"""
        assert self.is_position_valid(x, y)
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

        for x, y, player in STARTING_POSITIONS:
            self._set_position(x, y, player)

        # Starting Score is 2 each
        self._score = [2, 2]

    def get_valid_positions(self, piece: PlayerTurn = None) -> dict:
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

    def place(self, x: Index, y: Index, is_int: bool = False) -> bool:
        """Place the piece at the position
            Return if the move has been successfully executed
        """

        x_pos = x.zero_based_index if not is_int else x
        y_pos = y.zero_based_index if not is_int else y

        # Check if the move is valid
        changed = self.valid_positions.get(
            (x_pos, y_pos), [])
        if len(changed) == 0:
            raise InvalidPositionException(f"({x}, {y})")

        # Change the mutated pieces
        for mutate_x, mutated_y in changed:
            self._set_position(mutate_x, mutated_y, self.current_turn)

        # Place the piece on the board
        self._set_position(x_pos, y_pos, self.current_turn)

        # Update the score
        self._score[self.current_turn.to_index()] += len(changed) + 1

        # Toggle player turn
        self.change_turn()
        self._score[self.current_turn.to_index()] -= len(changed)

        # Increment the turn counter
        self.turns_taken += 1

        # Generate next set of valid moves
        self.valid_positions = self.get_valid_positions()

        # Check if other player has valid positions to move to
        if len(self.valid_positions) > 0:
            return True

        self.change_turn()
        self.valid_positions = self.get_valid_positions()
        if len(self.valid_positions) == 0:
            self.turns_taken = 64
        return False

    def get_winner(self) -> Optional[str]:
        if self.turns_taken < 64:
            return

        if self._score[0] > self._score[1]:
            return f"{self.WINNER_MESSAGE.format(winner='Black')}"

        if self._score[0] < self._score[1]:
            return self.WINNER_MESSAGE.format(winner='White')

        return self.DRAW_MESSAGE

    def is_valid(self, x_pos: int, y_pos: int, player: PlayerTurn) -> tuple:
        """Check if the move is valid
            x_pos and y_pos are zero based
        """

        player_value = player.value
        if self.get_position(x_pos, y_pos) != 0:
            return False, []

        applied = []

        # Check if any tile will change color
        for x, y in DIRECTIONS:

            mul = 1
            curr_x, curr_y = x_pos + mul * x, y_pos + mul * y

            # While position is valid look for next valid position
            while self.is_position_valid(curr_x, curr_y):

                # If the flip position is found
                if self.get_position(curr_x, curr_y) == player_value:
                    break

                # If the position is empty
                elif self.get_position(curr_x, curr_y) == 0:
                    curr_x = -1
                    break

                mul += 1
                curr_x, curr_y = x_pos + mul * x, y_pos + mul * y

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
