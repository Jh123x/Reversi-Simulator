import pygame
from Core.Index import Index
from Game.Board import GameBoard
from GUI.Direction import DIRECTION
from Core.Exceptions import InvalidPositionException


class GUI(object):

    # Initialise pygame
    pygame.init()
    pygame.font.init()
    TURN_MESSAGE = "Current turn: {}"
    BLACK_SCORE_MSG = "Black score: {}"
    WHITE_SCORE_MSG = "White score: {}"

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
        self.title = pygame.font.Font('freesansbold.ttf', 32)

        # Calculate separation of grid
        self.base_x = 0
        self.base_y = self.font.get_height() * 3
        self.x_sep = (self.width - self.base_x) / 8
        self.y_sep = (self.height - self.base_y) / 8

        # Calculate radius of Pieces
        self.rad = min(self.x_sep, self.y_sep) // 3

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
                if pos == 1:
                    pygame.draw.circle(self.screen, (0, 0, 0), dim, self.rad)
                elif pos == 2:
                    pygame.draw.circle(
                        self.screen, (255, 255, 255), dim, self.rad)

    def place_on_board(self, position: tuple) -> None:
        """Place piece at the position the player picked"""
        x, y = position
        x_ind = Index.from_zero_based(int((x - self.base_x) // self.x_sep))
        y_ind = Index.from_zero_based(int((y - self.base_y) // self.y_sep))
        self.board.place(x_ind, y_ind)

    def write(
        self, x: int, y: int, message: str, background: tuple = (0, 0, 0),
        foreground: tuple = (255, 255, 255), direction: DIRECTION = DIRECTION.CENTER, title: bool = False
    ) -> None:
        """Write the message on the screen with (x, y) as center"""

        # Render the message
        if title:
            msg = self.title.render(message, True, foreground)
        else:
            msg = self.font.render(message, True, background, foreground)

        # Apply function in Enum to the rect
        rect = direction(msg.get_rect(), x, y)

        # Draw the rectangle
        self.screen.blit(msg, rect)

    def draw_ui(self) -> None:
        """Draw the UI to show the score and the current turn"""

        base_height = self.font.get_height() // 2

        # Draw the turn
        self.write(0, base_height,
                   GUI.TURN_MESSAGE.format(
                       'Black' if self.board.current_turn == 1 else 'White'),
                   direction=DIRECTION.LEFT)
        black, white = self.board.get_score()

        self.write(self.width, base_height, GUI.BLACK_SCORE_MSG.format(
            black), direction=DIRECTION.RIGHT)
        self.write(self.width, self.font.get_height() + base_height, GUI.WHITE_SCORE_MSG.format(white),
                   direction=DIRECTION.RIGHT)

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

    def mainloop(self) -> None:
        """Main loop to run the GUI"""

        running = True
        while running:

            # Check if the player wants to leave
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONUP:
                    try:
                        self.place_on_board(pygame.mouse.get_pos())
                    except InvalidPositionException as e:
                        print(e)

            # Draw the background
            self.screen.fill((0, 125, 0))

            if self.board.get_winner() is not None:
                self.draw_end_screen()
                pygame.display.flip()
                continue

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
