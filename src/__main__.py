from Game.Board import GameBoard
from CLI.UI import CLI
from GUI.UI import GUI
from argparse import ArgumentParser


if __name__ == "__main__":

    # Create parser
    parser = ArgumentParser()
    parser.add_argument('-gui', "--gui", action="store_true", help="Run the game in GUI mode")

    # Parse arguments
    args = parser.parse_args()

    runner = CLI()
    if args.gui:
        runner = GUI(800, 600)
        
    runner.mainloop()
