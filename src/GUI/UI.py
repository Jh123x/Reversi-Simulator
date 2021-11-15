import pygame
from GUI.Screens.EndScreen import EndScreen
from GUI.Screens.GameScreen import GameScreen
from GUI.Screens.MenuScreen import MenuScreen
from Game.Board import GameBoard
from GUI.State import State
from GUI.Screens.SinglePlayerScreen import SinglePlayerScreen


class GUI(object):

    # Initialise pygame
    pygame.init()
    pygame.font.init()

    def __init__(self, width: int, height: int, window_name: str = "Reversi"):
        """GUI window to run the game"""
        super().__init__()

        # Store variables
        self.width = width
        self.height = height
        
        # Set window features
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(window_name)

        self.board = GameBoard()

        self.current_state = State.MENU

        # Complete Dict of States
        self.state_functions = {
            State.MENU: (MenuScreen(self.screen), (0, 125, 0)),
            State.TWO_PLAYER: (GameScreen(self.screen, self.board), (0, 125, 0)),
            State.GAME_OVER: (EndScreen(self.screen, self.board), (0, 0, 0)),
            State.AGAINST_AI: (SinglePlayerScreen(self.screen, self.board), (0, 125, 0)),
        }

    def mainloop(self) -> None:
        """Main loop to run the GUI"""

        running = True
        while running:

            # Call the function of the current state
            events = pygame.event.get()
            for event in events:

                # Leave event for all states.
                if event.type == pygame.QUIT:
                    return

            if self.current_state == State.QUIT:
                return

            # Get render function and background color
            curr_screen, bg_color = self.state_functions[self.current_state]

            # Draw the background
            self.screen.fill(bg_color)

            # Run the render function
            self.current_state = curr_screen.render(events)

            # Draw onto the screen
            pygame.display.flip()

        # Quit pygame
        pygame.quit()
