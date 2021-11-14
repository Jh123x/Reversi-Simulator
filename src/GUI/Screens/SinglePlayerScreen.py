import pygame
from GUI.Screens.GameScreen import GameScreen
from GUI.State import State
from Game.Board import GameBoard
from Core.Exceptions.InvalidPositionException import InvalidPositionException
from Core.Index import Index


class SinglePlayerScreen(GameScreen):
    def __init__(self, screen: pygame.Surface, board: GameBoard):
        # AI will take white
        self.board = board
        return super().__init__(screen)

    def place_on_board(self, position: tuple) -> None:
        """Place piece at the position the player picked"""
        x, y = position
        x_ind = Index.from_zero_based(int((x - self.base_x) // self.x_sep))
        y_ind = Index.from_zero_based(int((y - self.base_y) // self.y_sep))
        self.board.place(x_ind, y_ind)

    def render(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                try:
                    self.place_on_board(pygame.mouse.get_pos())
                except InvalidPositionException as e:
                    self.notification = 3000
        return State.AGAINST_AI
