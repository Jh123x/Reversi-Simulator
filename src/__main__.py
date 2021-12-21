from Test import test_all

from CLI.UI import CLI
from GUI.UI import GUI
from argparse import ArgumentParser


def run_test():
    test_all()


def run_cli():
    runner = CLI()
    runner.mainloop()


def run_gui():
    runner = GUI(800, 600)
    runner.mainloop()


if __name__ == "__main__":
    # Create parser
    parser = ArgumentParser()
    parser.add_argument('-g', "--gui", action="store_true",
                        help="Run the game in GUI mode")
    parser.add_argument('-t', "--test", help="Run tests")

    # Parse arguments
    args = parser.parse_args()

    # Run the modes
    if args.gui:
        run_gui()
    elif args.test:
        run_test()
    else:
        run_cli()
