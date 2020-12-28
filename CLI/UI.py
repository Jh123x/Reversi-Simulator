from os import system
from Core.Index import Index
from Game.Board import GameBoard

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
        return input(f"{message}{self.prompt_msg}")

    def mainloop(self):
        #Create the gameboard
        player_input = ""
        err = None

        #Game loop
        while player_input != 'q':
            self.print_state()
            player_input = self.get_user_input(err)
            self.clear_screen()
            if player_input == 'q':
                break
            x,y = tuple(map(int, player_input.strip().split(",")))

            try:
                self.board.place(Index.from_one_based(x), Index.from_one_based(y))
                err = None
            except Exception as e:
                err = str(e)

    def __repr__(self):
        return str(self.board)