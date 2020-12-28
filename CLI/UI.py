from os import system
from Core.Index import Index
from Game.Board import GameBoard
from Core.Exceptions import InvalidPositionException, AlreadyTakenException, OutOfBoundsException

class CLI(object):
    def __init__(self):
        """CLI runner for the game"""
        self.board = GameBoard()
        self.prompt_msg = "'q' to quit\nWhat is the position to put the piece (x,y): "

    def print_state(self):
        """Print the current state of the block"""
        print(self)
        print(f"Current turn: Player {self.board.current_turn}")

    def clear_screen(self):
        """Clear the items in the console"""
        system('cls')

    def get_user_input(self, message:str = None):
        """Get the input from the user
            message: Message to show user for prompt
        """
        if message == None:
            message = ""
        else:
            message += "\n"

        #Prompt the user for the input
        return input(f"{message}{self.prompt_msg}").strip()

    def convert_position(self, user_input:str) -> tuple:
        """Convert the player input into a position"""
        split_string = user_input.strip().split(",")

        #Check if the length is correct
        if len(split_string) != 2 or not "".join(split_string).isdigit():
            raise InvalidPositionException(f"{user_input}")
        
        #Convert the string to integer
        return tuple(map(int, split_string))

    def mainloop(self):
        """Main loop for the game"""
        #Create the gameboard
        player_input = ""
        err = None

        #Game loop
        while True:
            self.print_state()
            player_input = self.get_user_input(err)
            self.clear_screen()
            if player_input == 'q':
                break
            
            try:
                x, y = self.convert_position(player_input)
                self.board.place(Index.from_one_based(x), Index.from_one_based(y))
                err = None
            except (InvalidPositionException, AlreadyTakenException, OutOfBoundsException) as e:
                err = str(e)

    def __repr__(self):
        return str(self.board)