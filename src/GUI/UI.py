import pygame
from src.Core.Index import Index
from src.Game.Board import GameBoard
from src.GUI.Direction import DIRECTION
from src.Core.Exceptions import InvalidPositionException


class GUI(object):

    # Initialise pygame
    pygame.init()
    pygame.font.init()

    def __init__(self, board: GameBoard, width: int, height: int, window_name: str = "Reversi"):
        """GUI window to run the game"""
        super().__init__()

        # Set window features
        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption(window_name)

        # Store variables
        self.width = width
        self.height = height
        self.board = board
        self.font = pygame.font.Font('freesansbold.ttf', 16)

        # Calculate separation of grid
        self.x_sep = self.width / 8
        self.y_sep = self.height / 8

        # Calculate radius of Pieces
        self.rad = min(self.x_sep, self.y_sep) // 3

    def draw_grid(self):
        for x in range(8):
            for y in range(8):
                pygame.draw.rect(self.screen,
                                 (0, 0, 0),
                                 (int(x * self.x_sep), int(y * self.y_sep), int(self.x_sep), int(self.y_sep)),
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

    def write(self, x: int, y: int, message: str, background: tuple = (0, 0, 0),
              foreground: tuple = (255, 255, 255), direction: DIRECTION = DIRECTION.CENTER):
        """Write the message on the screen with (x, y) as center"""

        # Render the message
        msg = self.font.render(message, True, background, foreground)

        # Apply function in Enum to the rect
        rect = direction(msg.get_rect(), x, y)

        # Draw the rectangle
        self.screen.blit(msg, rect)

    def draw_ui(self):
        """Draw the UI to show the score and the current turn"""

        base_height = self.font.get_height() // 2
        # Draw the turn
        self.write(0, base_height, f"Current turn: {'Black' if self.board.current_turn == 1 else 'White'}",
                   direction=DIRECTION.LEFT)
        black, white = self.board.get_score()

        self.write(self.width, base_height, f"Black score: {black}", direction=DIRECTION.RIGHT)
        self.write(self.width, self.font.get_height() + base_height, f"White Score: {white}", direction=DIRECTION.RIGHT)

    def mainloop(self):
        """Main loop to run the GUI"""

        running = True
        while running:

            # Check if the player wants to leave
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONUP:
                    try:
                        self.place_on_board(pygame.mouse.get_pos())
                    except InvalidPositionException as e:
                        print(e)

            # Draw the background
            self.screen.fill((0, 125, 0))

            # Draw the grid
            self.draw_grid()

            # Update the grid with the board
            self.update_board_pieces()

            # Draw UI to the screen
            self.draw_ui()

            # Draw onto the screen
            pygame.display.flip()

        # Quit pygame
        pygame.quit()
