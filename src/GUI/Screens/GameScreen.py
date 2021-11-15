import pygame
import GUI

from GUI.Screens.Screen import Screen
from GUI.State import State
from GUI.Direction import DIRECTION
from Core.Index import Index
from Core.Exceptions import InvalidPositionException
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


class GameScreen(Screen):
    TURN_MESSAGE = "Current turn: {}"
    BLACK_SCORE_MSG = "Black score: {}"
    WHITE_SCORE_MSG = "White score: {}"
    INVALID_POSITION_MSG = "Invalid Position"

    def __init__(self, screen: pygame.Surface, board: GameBoard):
        super().__init__(screen)

        # Calculate separation of grid
        self.base_x = 0
        self.base_y = self.font.get_height() * 3
        self.x_sep = (self.width - self.base_x) / 8
        self.y_sep = (self.height - self.base_y) / 8
        self.notification = 0

        # Calculate radius of Pieces
        self.rad = min(self.x_sep, self.y_sep) // 3

        # Create the board
        self.board = board

    def update_board_pieces(self) -> None:
        winner_msg = self.board.get_winner()
        if winner_msg is not None:
            return
        for x in range(8):
            for y in range(8):
                pos = self.board.get_position(x, y)
                x_pos = x * self.x_sep + self.x_sep / 2 + self.base_x
                y_pos = y * self.y_sep + self.y_sep / 2 + self.base_y
                dim = (x_pos, y_pos)
                if pos == PlayerTurn.BLACK.value:
                    pygame.draw.circle(self.screen, (0, 0, 0), dim, self.rad)
                elif pos == PlayerTurn.WHITE.value:
                    pygame.draw.circle(
                        self.screen, (255, 255, 255), dim, self.rad)

    def draw_grid(self) -> None:
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    (int(x * self.x_sep + self.base_x),
                     int(y * self.y_sep + self.base_y),
                     int(self.x_sep),
                     int(self.y_sep)),
                    3
                )

    def place_on_board(self, position: tuple) -> None:
        """Place piece at the position the player picked"""
        x, y = position
        x_ind = Index.from_zero_based(int((x - self.base_x) // self.x_sep))
        y_ind = Index.from_zero_based(int((y - self.base_y) // self.y_sep))
        self.board.place(x_ind, y_ind)

    def draw_ui(self) -> None:
        """Draw the UI to show the score and the current turn"""

        base_height = self.font.get_height() // 2

        # Draw the turn
        self.write(0, base_height,
                   self.TURN_MESSAGE.format(
                       'Black' if self.board.current_turn == PlayerTurn.BLACK else 'White'),
                   direction=DIRECTION.LEFT)
        black, white = self.board.get_score()

        self.write(self.width, base_height, self.BLACK_SCORE_MSG.format(
            black), direction=DIRECTION.RIGHT)
        self.write(self.width, self.font.get_height() + base_height, self.WHITE_SCORE_MSG.format(white),
                   direction=DIRECTION.RIGHT)

    
    def render(self, events):
        # Check if the player wants to leave
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                try:
                    self.place_on_board(pygame.mouse.get_pos())
                except InvalidPositionException as e:
                    self.notification = 3000
                    
        if self.notification > 0:
            self.write_title(self.width // 2, 16, self.INVALID_POSITION_MSG)
            self.notification -= 1

        if self.board.get_winner() is not None:
            return State.GAME_OVER

        # Draw the grid
        self.draw_grid()

        # Update the grid with the board
        self.update_board_pieces()

        # Draw UI to the screen
        self.draw_ui()

        return State.TWO_PLAYER