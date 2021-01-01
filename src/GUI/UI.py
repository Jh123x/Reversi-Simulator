import pygame
from Core.Index import Index
from Game.Board import GameBoard
from Core.Exceptions import InvalidPositionException, AlreadyTakenException, OutOfBoundsException


class GUI(object):
    def __init__(self, board: GameBoard, width: int, height: int, window_name: str = "Reversi"):
        """GUI window to run the game"""
        super().__init__()

        # Store variables
        self.screen = pygame.display.set_mode([width, height])
        self.window_name = window_name
        self.width = width
        self.height = height
        self.board = board
        self.x_sep = self.width / 8
        self.y_sep = self.height / 8
        self.rad = min(self.x_sep, self.y_sep) // 3
        self.initialise_windows()

    def initialise_windows(self):
        # Set window name
        pygame.display.set_caption(self.window_name)

    def draw_grid(self):
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen, (0, 0, 0),
                                 (int(y * self.y_sep),
                                  int(x * self.x_sep),
                                  int(self.x_sep),
                                  int(self.y_sep)),
                                 3)

    def update_board_pieces(self):
        for x in range(8):
            for y in range(8):
                pos = self.board.get_position(x, y)
                dim = (x * self.x_sep + self.x_sep / 2, y * self.y_sep + self.y_sep / 2)
                if pos == 1:
                    pygame.draw.circle(self.screen, (0, 0, 0), dim, self.rad)
                elif pos == 2:
                    pygame.draw.circle(self.screen, (255, 255, 255), dim, self.rad)

    def place_on_board(self, position: tuple):
        """Place piece at the position the player picked"""
        x, y = position
        x_ind = Index.from_zero_based(int(x // self.x_sep))
        y_ind = Index.from_zero_based(int(y // self.y_sep))
        self.board.place(x_ind, y_ind)

    def mainloop(self):
        """Main loop to run the GUI"""

        # Initialise pygame
        pygame.init()

        running = True
        while running:

            # Check if the player wants to leave
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    try:
                        self.place_on_board(pygame.mouse.get_pos())
                    except (InvalidPositionException, AlreadyTakenException, OutOfBoundsException) as e:
                        print(e)

            # Draw the background
            self.screen.fill((0, 125, 0))

            # Draw the grid
            self.draw_grid()

            # Update the grid with the board
            self.update_board_pieces()

            # Draw onto the screen
            pygame.display.flip()

        # Quit pygame
        pygame.quit()
