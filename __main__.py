from Game import GameBoard
from Core.Index import Index

def print_board(board: GameBoard):
    for row in range(8):
        for col in range(8):
            print(int(board._get_position(col, row)), end = " ")
        print()

    print(f"Current turn: {board.current_turn}")

if __name__ == "__main__":

    #Create the gameboard
    board = GameBoard()
    player_input = ""

    #Game loop
    while player_input != 'q':

        print_board(board)
        player_input = input("What is the position to put the piece (x,y): ")

        if player_input == 'q':
            break

        x,y = tuple(map(int, player_input.strip().split(",")))
        board.place(Index.from_one_based(x), Index.from_one_based(y))