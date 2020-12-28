from Game.Board import GameBoard
from CLI.UI import CLI
from GUI.UI import GUI
from argparse import ArgumentParser


if __name__ == "__main__":

    #Create parser
    parser = ArgumentParser()
    parser.add_argument('-gui', "--gui", action="store_true", help="Run the game in GUI mode")

    #Parse arguments
    args = parser.parse_args()

    #Create the board
    board = GameBoard()

    runner = CLI(board)
    if(args.gui):
        runner = GUI(board, 800, 600)
        
    runner.mainloop()