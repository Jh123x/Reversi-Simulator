from typing import Optional

import numpy as np
from collections import defaultdict

from Game.AI.Ai import AI
from Game.Board import GameBoard


def rollout_policy(possible_moves):

    return possible_moves[np.random.randint(len(possible_moves))]


def _get_winner(board: GameBoard) -> Optional[int]:
    if "White" in board.get_winner():
        return 1
    elif "Black" in board.get_winner():
        return -1
    else:
        return 0


class MonteCarloTreeSearchNode:
    def __init__(self, state: GameBoard, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def untried_actions(self):
        self._untried_actions = self.state.get_valid_positions()
        return list(self._untried_actions.keys())

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        new_board = GameBoard(self.state)
        new_board.place(*action, is_int=True)
        child_node = MonteCarloTreeSearchNode(
            new_board, parent=self, parent_action=action)

        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.get_winner() is not None

    def rollout(self):
        current_rollout_state = self.state

        while current_rollout_state.get_winner() is None:
            possible_moves = list(current_rollout_state.get_valid_positions().keys())

            action = rollout_policy(possible_moves)
            new_board = GameBoard(current_rollout_state)
            new_board.place(*action, is_int=True)
            current_rollout_state = new_board
        return _get_winner(current_rollout_state)

    def back_propagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.back_propagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):

        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self) -> 'MonteCarloTreeSearchNode':
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.back_propagate(reward)

        return self.best_child(c_param=0.)


class MonteAi(AI):

    def generate_move(self, board: GameBoard) -> tuple[int, int]:
        """Generate the next best move"""
        root = MonteCarloTreeSearchNode(board)
        return root.best_action().parent_action
