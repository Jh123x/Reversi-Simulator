import unittest
from random import randint

import numpy as np

from Core.Index import Index
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


class BoardTest(unittest.TestCase):
    # Constants to be used in the test
    STARTING_TURN = PlayerTurn.BLACK
    STARTING_MOVES = {(5, 3), (4, 2), (3, 5), (2, 4)}
    EMPTY_BOARD = np.zeros((8, 8))

    # Board with no valid moves
    BOARD_WITH_NO_VALID_MOVE = EMPTY_BOARD.copy()
    BOARD_WITH_NO_VALID_MOVE[0, 0] = 1
    BOARD_WITH_NO_VALID_MOVE[7, 7] = 0

    # Board that is completely filled
    FILLED_BOARD = np.full((8, 8), 1)

    # Board with 1 valid move
    BOARD_WITH_VALID_MOVE = FILLED_BOARD.copy()
    BOARD_WITH_VALID_MOVE[0, 0] = -1
    BOARD_WITH_VALID_MOVE[7, 7] = 0

    # Board with 1 valid move part 2
    ONE_VALID_BOARD_2 = np.full((8, 8), 1)
    ONE_VALID_BOARD_2[0][0] = 0
    coords = [
        (0, 2), (0, 6), (0, 7),
        (1, 0), (1, 1), (1, 2), [1, 3], [1, 4], [1, 5], [1, 6], [1, 7],
        (2, 5), (2, 7),
        (3, 2), (3, 4), (3, 6), (3, 7),
        (4, 2), (4, 3), (4, 6), (4, 7),
        (5, 0), (5, 1), (5, 2), (5, 4),
        (6, 0), (6, 1), (6, 2), (6, 3), (6, 5),
        (7, 0)
    ]
    for x, y in coords:
        ONE_VALID_BOARD_2[x][y] = -1

    for x in range(8):
        for y in range(8):
            FILLED_BOARD[x][y] = randint(1, 2)

    def setUp(self) -> None:
        """Create a new board for all the tests"""
        self.board = GameBoard()

    def test_change_turn(self):
        """Check the turn changing logic is correct"""
        self.assertEqual(self.board.current_turn, PlayerTurn.BLACK)
        self.board.change_turn()
        self.assertEqual(self.board.current_turn, PlayerTurn.WHITE)

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
        curr = PlayerTurn.BLACK

        # For each iteration and turn change (Board is only 8x8 at starts with 4 pieces)
        for _ in range(60):

            # Check if the turn in the board is correct
            self.assertEqual(self.board.current_turn, curr)

            # Take the next possible move and execute it
            positions = self.board.get_valid_positions()
            assert len(positions) > 0
            x, y = tuple(positions.keys())[0]

            # If turn changed go to the next turn
            turn_changed = self.board.place(Index.from_zero_based(x), Index.from_zero_based(y))
            if turn_changed:
                curr = PlayerTurn.WHITE if curr == PlayerTurn.BLACK else PlayerTurn.BLACK

    def test_place(self):
        """Checks the placing of the pieces"""
        # For each iteration and turn change (Board is only 8x8 at starts with 4 pieces)
        for _ in range(60):
            # Take the next possible move and execute it
            pos = tuple(self.board.get_valid_positions().keys())
            assert (len(pos) > 0), self.board.get_valid_positions()
            x, y = pos[0]
            self.assertEqual(0, self.board.get_position(x, y))

            # Check if the position is filled after playing
            current_turn = self.board.current_turn
            self.board.place(Index.from_zero_based(x), Index.from_zero_based(y))
            self.assertEqual(current_turn.value, self.board.get_position(x, y))

    def test_almost_full_place_is_valid(self):
        """Check if the last piece can be placed correctly"""
        # Set the board with no valid moves when the board is partially filled
        self.board.set_board(BoardTest.BOARD_WITH_VALID_MOVE)

        # Place the last piece
        self.assertTrue(self.board.is_valid(7, 7, PlayerTurn.WHITE))

        # 2nd Board
        self.board.set_board(BoardTest.ONE_VALID_BOARD_2)
        self.assertTrue(self.board.is_valid(0, 0, PlayerTurn.WHITE))
        self.assertTrue(self.board.is_valid(0, 0, PlayerTurn.BLACK))


if __name__ == '__main__':
    unittest.main()
