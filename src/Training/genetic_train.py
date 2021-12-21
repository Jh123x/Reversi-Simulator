import numpy as np

from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn
from Game.AI.AlphaBetaAi import AlphaBetaAi


def fitness_function(board: GameBoard, turn: PlayerTurn) -> int:
    """How good the board is for the player"""
    return 0


def create_nn():
    """Create a new neutral net with random weights"""
    return np.random.rand(8, 8)


def play(agent) -> int:
    """
    Play agent against alphabeta ai
    Returns the score of the agent
    """
    # Create the alpha beta AI to train the neural network
    ab_ai = AlphaBetaAi()
    board = GameBoard()

    # Play until the game is over
    while not board.is_game_over():
        # Get the best move for the agent
        move = agent.get_move(board)

        # Play the move
        board.play_move(move)

        # Get the best move for the alpha beta AI
        move = ab_ai.get_move(board)

        # Play the move
        board.play_move(move)


if __name__ == "__main__":

    # Hyper params
    population_size = 100
    num_generations = 100
    num_games_per_gen = 10
    num_games_to_win = 5

    # Create the generations
    population = [create_nn() for i in range(population_size)]
    score = []

    # Play each generation and get the score
    for generation in range(num_generations):
        print(f"Generation number: {generation}")
        for agent in population:
            score = play(agent)

            

        


