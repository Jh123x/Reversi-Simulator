import multiprocessing as mp
import os
from typing import List, Any

import numpy as np
import pygame

from GUI.Screens.GameScreen import GameScreen
from Game.AI.AlphaBetaAi import AlphaBetaAi
from Game.AI.GeneticAi import GeneticAI
from Game.Board import GameBoard
from Game.PlayerEnum import PlayerTurn


def render_gui(queue: mp.Queue, board: GameBoard = GameBoard()) -> None:
    """Render the GUI"""

    bg_color = (0, 125, 0)
    screen = pygame.display.set_mode((800, 600))
    game_screen = GameScreen(screen, board)
    pygame.display.set_caption("Training")
    clock = pygame.time.Clock()

    running = True
    while running:

        clock.tick(2)

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
            break

        # Otherwise, place for the move
        board.place(*move)

        # Update the screen
        game_screen.render(events)
        pygame.display.flip()

    # Quit pygame
    pygame.quit()


def play(agent: GeneticAI, agent2: GeneticAI = None, gui: bool = False) -> tuple[tuple, Any]:
    """
    Play agent against other agent
    Other agent is AlphaBetaAi by default
    Agent is always black
    Returns the score of the agent.
    """
    # Create the alpha beta AI to train the neural network
    ab_ai = AlphaBetaAi() if agent2 is None else agent2
    board = GameBoard()
    ai_turn = board.current_turn
    queue = mp.Manager().Queue(64)

    if gui:
        p = mp.Process(target=render_gui, args=(queue, board))
        p.start()

    # Play until the game is over
    while board.get_winner() is None:
        if len(board.get_valid_positions()) == 0:
            break

        if board.current_turn == PlayerTurn.WHITE:
            move = ab_ai.generate_move(board)
        elif board.current_turn == PlayerTurn.BLACK:
            move = agent.generate_move(board)
        else:
            break

        x, y = agent.to_index(*move)
        board.place(x, y)
        queue.put((x, y))

    if gui:
        queue.put(None)
        p.join()

    return board.get_score(), ai_turn


def mutate(weights: np.ndarray) -> np.ndarray:
    """Mutate weights randomly"""
    for r in weights:
        r += np.random.uniform(-0.5, 0.5)
    return weights


def breed(ai1: GeneticAI, ai2: GeneticAI) -> List[GeneticAI]:
    """Breed genetic AI to become 4 new AI"""

    # Get the weights of the two players
    weights1 = ai1.get_model()
    weights2 = ai2.get_model()

    # Create the new weights
    new_weights = []

    # New child
    for i in range(1, 7):
        child = np.zeros(weights1.shape)
        child[0:i] = weights1[0:i]
        child[i:] = weights2[i:]
        new_weights.append(child)
        new_weights.append(mutate(child))

    # Create the new AI
    t = []
    for weight in new_weights:
        t.append(GeneticAI(weight))
    return t


def start_training() -> None:
    """Start training for the ai"""

    # Constants for training
    saves: str = os.path.join("", "saves", "genetic_ai")
    if not os.path.exists(saves):
        os.makedirs(saves)

    # Hyper params
    population_size = 20
    num_generations = 500
    gui = True

    # Create the generations
    population = [GeneticAI() for _ in range(population_size)]

    # Check if the previous weights exists
    if os.path.exists(os.path.join(saves, f"1.npy")):
        weights: List = []
        for i in range(2):
            path = os.path.join(saves, f"{i + 1}.npy")
            weights.append(np.load(path))
        population = [GeneticAI(model=weight) for weight in weights]
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
            (score1, score2), turn = play(
                agent,
                agent2=AlphaBetaAi() if generation < 60 else population[(index + 1) % population_size],
                gui=gui,
            )
            assert PlayerTurn.BLACK == turn
            score = score1 if turn == PlayerTurn.BLACK else score2
            scores.append((score, agent))
            print(f"Agent {index + 1} score: {score}")

        # Pick the best players
        scores.sort(reverse=True, key=lambda x: x[0])
        print(scores)

        # Create the next generation (2 old + 4 mutated + 4 new)
        population: List = []

        # Save the top 2 players
        for i in range(min(2, len(scores))):
            ai: GeneticAI = scores[i][1]

            # Bring fwd to next generation
            population.append(ai)

            # Save the current version
            print(f"Saving {i + 1}")
            path = os.path.join(saves, f"{i + 1}.npy")
            np.save(path, ai.get_model())

        # Breed top 2 players
        print(f"Breeding top 2 players")
        mutated = breed(*population)
        population.extend(mutated)

        # Create new generation
        population += [GeneticAI() for _ in range(population_size - len(population))]
