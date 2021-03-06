import unittest
import numpy as np
from random import randint
from src.Core.Index import Index
from src.Game.Board import GameBoard


class BoardTest(unittest.TestCase):

    # Constants to be used in the test
    STARTING_TURN = 1
    STARTING_MOVES = {(5, 3), (4, 2), (3, 5), (2, 4)}
    EMPTY_BOARD = np.zeros((8, 8))

    # Board with no valid moves
    BOARD_WITH_NO_VALID_MOVE = EMPTY_BOARD.copy()
    BOARD_WITH_NO_VALID_MOVE[0, 0] = 1
    BOARD_WITH_NO_VALID_MOVE[7, 7] = 0

    # Board that is completely filled
    FILLED_BOARD = EMPTY_BOARD.copy()
    for x in range(8):
        for y in range(8):
            FILLED_BOARD[x][y] = randint(1, 2)

    def setUp(self) -> None:
        """Create a new board for all the tests"""
        self.board = GameBoard()

    def test_initial_state(self):
        """Check the initial state of the board"""
        # Check the current player turn
        self.assertEqual(self.board.current_turn, BoardTest.STARTING_TURN)

        # Check if the starting player score is correct
        self.assertEqual(self.board.get_score(), (2, 2))

    def test_get_valid_positions(self):
        """Check if the valid positions reflected are correct"""

        # Get the valid positions at the start
        starting_valid_positions = self.board.get_valid_positions()
        self.assertEqual(set(starting_valid_positions.keys()), BoardTest.STARTING_MOVES)

        # Place 1 piece at 4,2
        self.board.place(Index.from_zero_based(4), Index.from_zero_based(2))
        valid_positions = self.board.get_valid_positions()
        self.assertEqual(set(valid_positions), {(3, 2), (5, 2), (5, 4)})

        # Set the board with no valid moves when the board is empty
        self.board.set_board(BoardTest.EMPTY_BOARD)
        valid_positions = self.board.get_valid_positions()
        self.assertEqual(len(valid_positions), 0)

        # Set the board with no valid moves when the board is partially filled
        self.board.set_board(BoardTest.BOARD_WITH_NO_VALID_MOVE)
        valid_positions = self.board.get_valid_positions()
        self.assertEqual(len(valid_positions), 0)

        # Set the board with no valid moves when the board is filled
        self.board.set_board(BoardTest.FILLED_BOARD)
        valid_positions = self.board.get_valid_positions()
        self.assertEqual(len(valid_positions), 0)

    def test_current_turn(self):
        """Check if the turn cycling is correct"""
        # First turn
        curr = False

        # For each iteration and turn change (Board is only 8x8 at starts with 4 pieces)
        for _ in range(60):

            # Check if the turn in the board is correct
            self.assertEqual(self.board.current_turn, int(curr) + 1)

            # Take the next possible move and execute it
            x, y = tuple(self.board.get_valid_positions().keys())[0]

            # If turn changed go to the next turn
            turn_changed = self.board.place(Index.from_zero_based(x), Index.from_zero_based(y))
            if turn_changed:
                curr = not curr

    def test_place(self):
        """Checks the placing of the pieces"""
        # For each iteration and turn change (Board is only 8x8 at starts with 4 pieces)
        for _ in range(60):
            # Take the next possible move and execute it
            x, y = tuple(self.board.get_valid_positions().keys())[0]
            self.assertEqual(0, self.board.get_position(x, y))

            # Check if the position is filled after playing
            current_turn = self.board.current_turn
            self.board.place(Index.from_zero_based(x), Index.from_zero_based(y))
            self.assertEqual(current_turn, self.board.get_position(x, y))


if __name__ == '__main__':
    unittest.main()
