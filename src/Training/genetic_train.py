import multiprocessing as mp
from typing import List
import pygame
import numpy as np
import os
import time

from GUI.Screens.GameScreen import GameScreen
from GUI.State import State
from Game.AI.AlphaBetaAi import AlphaBetaAi
from Game.AI.GeneticAi import GeneticAI
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


def render_gui(queue: mp.Queue, board: GameBoard = GameBoard(), delay: int = 10) -> None:
    """Render the GUI"""

    bg_color = (0, 125, 0)
    screen = pygame.display.set_mode((800, 600))
    game_screen = GameScreen(screen, board)
    pygame.display.set_caption("Training")

    running = True
    while running:

        # Call the function of the current state
        events = pygame.event.get()
        for event in events:

            # Leave event for all states.
            if event.type == pygame.QUIT:
                return

        # Draw the background
        screen.fill(bg_color)
        move = queue.get(block=True)

        # After the last move
        if move is None:
            time.sleep(delay)
            break

        # Otherwise place for the move
        board.place(*move)

        # Update the screen
        game_screen.render(events)
        pygame.display.flip()

    # Quit pygame
    pygame.quit()


def play(agent: GeneticAI, agent2: GeneticAI = None, gui: bool = False,) -> int:
    """
    Play agent against alphabeta ai
    Returns the score of the agent
    """
    # Create the alpha beta AI to train the neural network
    ab_ai = AlphaBetaAi() if agent2 is None else agent2
    board = GameBoard()
    ai_turn = board.current_turn

    if gui:
        queue = mp.Manager().Queue(64)
        p = mp.Process(target=render_gui, args=(queue, board))
        p.start()

    # Play until the game is over
    while board.get_winner() is None:
        if len(board.get_valid_positions()) == 0:
            break

        if board.current_turn == PlayerTurn.WHITE:
            move = ab_ai._generate_move(board)
        elif board.current_turn == PlayerTurn.BLACK:
            move = agent._generate_move(board)
        else:
            break

        x, y = agent.to_index(*move)
        valid = board.place(x, y)

        if not valid:
            print(
                f"Invalid Move (0 based): {move}. Valid Moves: {board.get_valid_positions()}")
            queue.put(None)
            if gui:
                p.join()
            raise ValueError(
                f"Invalid Move (0 based): {move}. Valid Moves: {board.get_valid_positions()}")

        queue.put((x, y))

    if gui:
        p.join()

    return board.get_score(), ai_turn


def breed(ai1: GeneticAI, ai2: GeneticAI) -> List[GeneticAI]:
    """Breed genetic AI to become 4 new AI"""

    # Get the weights of the two players
    weights1 = ai1.get_weights()
    weights2 = ai2.get_weights()

    # Create the new weights
    new_weights = []

    # Breed the weights (Choose parent or child)
    for _ in range(3):
        for i in range(len(weights1)):
            new_weights.append(np.random.choice([weights1[i], weights2[i]]))

    # Average the parent and child
    new_weights.append(np.average(weights1 + weights2, axis=0))

    # Create the new AI
    return [GeneticAI(weights=weights) for weights in new_weights]


def start_training():
    """Start training for the ai"""

    # Constants for training
    saves: str = os.path.join(".", "saves", "genetic_ai")
    if not os.path.exists(saves):
        os.makedirs(saves)

    # Hyper params
    population_size = 2
    num_generations = 2
    gui = True

    # Create the generations
    population = [GeneticAI() for _ in range(population_size)]

    # Check if the previous weights exists
    if os.path.exists(os.path.join(saves, f"1.npy")):
        weights: List = []
        for i in range(2):
            # Save the current version
            path = os.path.join(saves, f"{i+1}.npy")
            with open(path, "wb") as f:
                weights.append(np.load(f))
        population = [GeneticAI(weights=weight) for weight in weights]
        population.extend(breed(*population))
        population += [GeneticAI()
                       for _ in range(population_size - len(population))]

    # Play each generation and get the score
    for generation in range(num_generations):

        # Generation Training
        print(f"Generation number: {generation + 1}")

        # Store the scores
        scores: List = []

        # Allow each agent to play
        for index, agent in enumerate(population):
            score1, score2, turn = play(
                agent,
                agent2=population[(index + 1) % len(population)],
                gui=gui)
            scores.append(
                (score1 if turn == PlayerTurn.WHITE else score2, agent))
            print(f"Agent {index + 1} score: {score1}")

        # Pick the best players
        scores.sort(reverse=True, key=lambda x: x[0])
        print(scores)

        # Create the next generation (2 old + 4 mutated + 4 new)
        population: List = []

        # Save the top 3 players
        for i in range(min(2, len(scores))):
            ai: GeneticAI = scores[i][1]

            # Bring fwd to next generation
            population.append(ai)

            # Save the current version
            print(f"Saving {i+1}")
            path = os.path.join(saves, f"{i+1}.npy")
            with open(path, 'wb') as f:
                np.save(f, ai.get_weights())

        # Breed top 2 players
        print(f"Breeding top 2 players")
        mutated = breed(*population)
        population.extend(mutated)

        # Create new generation
        population += [GeneticAI()
                       for _ in range(population_size - len(population))]
