import pygame
from GUI.Screens.GameScreen import GameScreen
from GUI.State import State
from Game.Board import GameBoard
from Core.Exceptions.InvalidPositionException import InvalidPositionException


class SinglePlayerScreen(GameScreen):
    def __init__(self, screen: pygame.Surface, board: GameBoard):
        # AI will take white
        return super().__init__(screen, board)

    def render(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                try:
                    self.place_on_board(pygame.mouse.get_pos())
                except InvalidPositionException as e:
                    self.notification = 3000

        # Drawing logic
        self.draw_ui()
        self.update_board_pieces()
        self.draw_grid()

        # AI Logic

        return State.AGAINST_AI
