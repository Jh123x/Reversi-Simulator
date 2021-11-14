import pygame

from GUI.Screens.Screen import Screen
from GUI.State import State
from Game.Board import GameBoard


class EndScreen(Screen):
    def __init__(self, screen: pygame.Surface, board: GameBoard):
        super().__init__(screen)

        self.board = board
        self.width = screen.get_width()
        self.height = screen.get_height()

    def draw_end_screen(self):
        self.write(
            self.width // 2, self.height // 2 + 32, self.board.get_winner(), title=True
        )
        black, white = self.board.get_score()
        self.write(
            self.width // 2, self.height // 2, f"Black: {black}", title=True
        )
        self.write(
            self.width // 2, self.height // 2 - 32, f"White: {white}", title=True
        )
    
    def render(self, events) -> State:
        self.draw_end_screen()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.board.reset()
                return State.MENU

        return State.GAME_OVER