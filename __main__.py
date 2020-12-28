import tkinter as tk
from CLI.UI import CLI
from Core.Index import Index

def run_cli():
    cli_ui = CLI()
    cli_ui.mainloop()

if __name__ == "__main__":
    run_cli()