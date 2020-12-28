from argparse import ArgumentParser
from CLI.UI import CLI
from GUI.UI import GUI

def run_cli():
    """Run the command line version of the game"""
    cli_ui = CLI()
    cli_ui.mainloop()

def run_gui():
    """Run the game in GUI mode"""
    gui_ui = GUI()
    gui_ui.mainloop()

if __name__ == "__main__":

    #Create parser
    parser = ArgumentParser()
    parser.add_argument('-gui', "--gui", action="store_true", help="Run the game in GUI mode")

    #Parse arguments
    args = parser.parse_args()

    #Run in either CLI or GUI mode
    if(args.gui):
        run_gui()
    else:
        run_cli()