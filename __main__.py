import tkinter as tk
from CLI.UI import CLI
from GUI.UI import GUI
from Core.Index import Index

def run_cli():
    """Run the command line version of the game"""
    cli_ui = CLI()
    cli_ui.mainloop()

def run_gui():
    """Run the game in GUI mode TODO"""
    gui_ui = GUI()
    gui_ui.mainloop()

if __name__ == "__main__":
    run_cli()