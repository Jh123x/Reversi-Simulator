from os import system
from src.Core.Index import Index
from src.Game.Board import GameBoard
from src.Core.Exceptions import InvalidPositionException, AlreadyTakenException, OutOfBoundsException


class CLI(object):
    def __init__(self, board: GameBoard):
        """CLI runner for the game"""
        self.board = board
        self.prompt_msg = "'q' to quit\nWhat is the position to put the piece (x,y): "

    def print_state(self):
        """Print the current state of the block"""
        print(self)
        print(f"Current turn: Player {self.board.current_turn}")

    @staticmethod
    def clear_screen():
        """Clear the items in the console"""
        system('cls')

    def get_user_input(self, message: str = None):
        """Get the input from the user
            message: Message to show user for prompt
        """
        if message is None:
            message = ""
        else:
            message += "\n"

        # Prompt the user for the input
        return input(f"{message}Current Score (p1,p2): {self.board.get_score()}\n{self.prompt_msg}").strip()

    @staticmethod
    def convert_position(user_input: str) -> tuple:
        """Convert the player input into a position"""
        split_string = user_input.strip().split(",")

        # Check if the length is correct
        if len(split_string) != 2 or not "".join(split_string).isdigit():
            raise InvalidPositionException(f"{user_input}")
        
        # Convert the string to integer
        return tuple(map(int, split_string))

    def mainloop(self):
        """Main loop for the game"""
        # Create the Game board
        err = None

        # Game loop
        while True:
            self.print_state()
            player_input = self.get_user_input(err)
            self.clear_screen()
            if player_input == 'q':
                break
            
            try:
                x, y = self.convert_position(player_input)
                placed = self.board.place(Index.from_one_based(x), Index.from_one_based(y))
                err = None
                if not placed:
                    err = f"Player {self.board.current_turn} skipped as there are no spots"
            except (InvalidPositionException, AlreadyTakenException, OutOfBoundsException) as e:
                err = str(e)

    def __repr__(self):
        return str(self.board)
