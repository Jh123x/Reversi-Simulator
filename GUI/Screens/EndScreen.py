import pygame

from GUI.Screens.Screen import Screen
from GUI.State import State
from Game.Board import GameBoard


class EndScreen(Screen):
    def __init__(self, screen: pygame.Surface, board: GameBoard):
        super().__init__(screen)
        self.board = board

    def draw_end_screen(self):
        center = self.width // 2
        self.write_title(
            center, self.height // 2 + 32, self.board.get_winner()
        )
        black, white = self.board.get_score()
        self.write_title(
            center, self.height // 2, f"Black: {black}"
        )
        self.write_title(
            center, self.height // 2 - 32, f"White: {white}"
        )
        self.write_title(
            center, self.height // 2 + 128, f"Press click anywhere to continue...."
        )

    def render(self, events) -> State:
        self.draw_end_screen()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.board.reset()
                return State.MENU

        return State.GAME_OVER
