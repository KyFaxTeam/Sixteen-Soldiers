import time
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    """AI agent with Alpha-Beta pruning and time optimization"""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "AIVerse Agent"
        self.max_depth = 12#3  # Profondeur maximale initiale
        self.time_budget = 500  # Temps total alloué en millisecondes
        self.time_used = 0  # Temps utilisé par l'agent

    def choose_action(self, board: Board) -> Dict:
        """
        Choose the best action using Alpha-Beta pruning.
        Args:
            board: Current game board state
        Returns:
            The best action for the soldier_value
        """
        start_time = time.time()
        best_action = None
        alpha = float("-inf")
        beta = float("inf")

        # Adjust max_depth dynamically based on remaining time budget
        if self.time_used < self.time_budget * 0.5:
            self.max_depth = 3  # Explore deeper in early game
        elif self.time_used < self.time_budget * 0.8:
            self.max_depth = 2  # Reduce depth in mid-game
        else:
            self.max_depth = 1  # Prioritize speed in late-game

        # Run Alpha-Beta pruning to find the best move
        valid_actions = board.get_valid_actions()
        valid_actions = self.prioritize_actions(valid_actions, board)

        for action in valid_actions:
            board_copy = self.copy_board(board)
            self.apply_action(board_copy, action)
            score = self.alpha_beta(board_copy, self.max_depth - 1, alpha, beta, False)
            if score > alpha:
                alpha = score
                best_action = action

            # Check time elapsed
            elapsed_time = (time.time() - start_time) * 1000
            if self.time_used + elapsed_time >= self.time_budget:
                break

        self.time_used += (time.time() - start_time) * 1000
        return best_action

    def alpha_beta(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """
        Alpha-Beta pruning algorithm.
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        valid_actions = board.get_valid_actions()
        valid_actions = self.prioritize_actions(valid_actions, board)

        if maximizing:
            max_eval = float("-inf")
            for action in valid_actions:
                board_copy = self.copy_board(board)
                self.apply_action(board_copy, action)
                eval = self.alpha_beta(board_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for action in valid_actions:
                board_copy = self.copy_board(board)
                self.apply_action(board_copy, action)
                eval = self.alpha_beta(board_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, board: Board) -> float:
        """
        Evaluate the board state.
        """
        red_count = board.count_soldiers(Soldier.RED)
        blue_count = board.count_soldiers(Soldier.BLUE)

        if self.soldier_value == Soldier.RED:
            return red_count - blue_count
        else:
            return blue_count - red_count

    def prioritize_actions(self, actions: list, board: Board) -> list:
        """
        Prioritize actions to explore better moves first.
        """
        return sorted(actions, key=lambda action: self.heuristic_action_value(action, board), reverse=True)

    def heuristic_action_value(self, action: Dict, board: Board) -> int:
        """
        Assign a heuristic value to an action.
        """
        from_pos = action['from_pos']
        to_pos = action['to_pos']
        captured = action.get('captured_soldier', None)

        value = 0
        if captured:
            value += 10  # Capture actions are prioritized
        if to_pos in board.get_neighbors(from_pos)[Soldier.EMPTY.name]:
            value += 1  # Prefer advancing

        return value

    def apply_action(self, board: Board, action: Dict):
        """
        Apply an action to a board.
        """
        if action['type'] == 'MOVE_SOLDIER':
            board.move_soldier(action)
        elif action['type'] == 'CAPTURE_SOLDIER':
            board.capture_soldier(action)

    def copy_board(self, board: Board) -> Board:
        """
        Create a deep copy of the board for simulations.
        """
        new_board = Board()
        new_board.soldiers = board.soldiers.copy()
        new_board.last_action = board.last_action
        new_board.is_multiple_capture = board.is_multiple_capture
        return new_board