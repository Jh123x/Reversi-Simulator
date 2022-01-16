import multiprocessing as mp
import pygame

from Core.Constants import AI_MOVE_KEY
from Core.Exceptions.InvalidPositionException import InvalidPositionException
from GUI.Screens.GameScreen import GameScreen
from GUI.State import State
from Game.AI.Ai import AI
from Game.AI.AlphaBetaAi import AlphaBetaAi
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


class SinglePlayerScreen(GameScreen):
    def __init__(self, screen: pygame.Surface, board: GameBoard, ai_type: AI = AlphaBetaAi()) -> None:
        """The single player screen"""
        super().__init__(screen, board)

        # AI will take white
        self.ai = ai_type
        self.is_ai_executing = False

        # Multiprocess manager
        self.process_manager = mp.Manager()
        self.return_dict = self.process_manager.dict()
        self.process = None

    def draw_loading(self):
        """
        Draws the ai waiting screen
        """
        self.write_title(self.width // 2, 32, "Ai is thinking...")

    def render(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and not self.is_ai_executing:
                try:
                    self.place_on_board(pygame.mouse.get_pos())
                except InvalidPositionException as _:
                    self.notification = 3000

        if self.board.get_winner() is not None:
            return State.GAME_OVER

        # AI Logic execute in parallel
        if self.board.current_turn == PlayerTurn.WHITE and not self.is_ai_executing:
            self.is_ai_executing = True
            args = (self.board, self.return_dict)
            self.process = mp.Process(target=self.ai.get_move, args=args)
            self.process.start()

        if self.is_ai_executing:
            # Tries to get result
            if AI_MOVE_KEY in self.return_dict:
                self.is_ai_executing = False
                pos = self.return_dict[AI_MOVE_KEY]

                self.board.place(*self.ai.to_index(*pos))
                self.process.join()
                self.process = None
                del self.return_dict[AI_MOVE_KEY]
            else:
                self.draw_loading()

        # Drawing logic
        self.draw_ui()
        self.update_board_pieces()
        self.draw_grid()

        return State.AGAINST_AI
