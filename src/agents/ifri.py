"""best agent ai v3"""
import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

DEPTH = 1
HISTORY_SIZE = 4

class Agent(BaseAgent):
    """Enhanced AI agent implementing minimax with loop avoidance and evaluation function."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "IFRI"
        self.move_history: List[Dict] = []  # Track recent moves to detect loops

    def choose_action(self, board: Board) -> Dict:
        """
        Choose an action from valid moves using minimax algorithm with loop avoidance.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """
        valid_actions = board.get_valid_actions()

        # If no valid actions, return a random fallback (shouldn't happen in normal cases)
        if not valid_actions:
            return random.choice(valid_actions)

        # Run minimax with depth and avoid loops
        best_action = None
        best_score = float('-inf')  # Maximizing player starts with -infinity

        for action in valid_actions:
            if self.is_looping_action(action):
                continue  # Skip actions that lead to loops

            simulated_board = self.simulate_action(board, action)
            score = self.minimax(simulated_board, depth=DEPTH, maximizing=False)

            if score > best_score:
                best_score = score
                best_action = action

        # Update move history to prevent loops
        if best_action:
            self.update_move_history(best_action)

        return best_action if best_action else random.choice(valid_actions)

    def is_looping_action(self, action: Dict) -> bool:
        """
        Check if the given action creates a loop based on recent move history.
        Args:
            action: Action to check
        Returns:
            True if the action causes a loop, False otherwise
        """
        # Check if this move reverses the previous move
        if len(self.move_history) >= 2:
            last_action = self.move_history[-1]
            second_last_action = self.move_history[-2]
            if (action['from_pos'] == last_action['to_pos'] and
                action['to_pos'] == last_action['from_pos'] and
                last_action['from_pos'] == second_last_action['to_pos']):
                return True
        return False

    def update_move_history(self, action: Dict):
        """
        Update the move history to track recent moves and avoid loops.
        Args:
            action: The action to add to the history
        """
        self.move_history.append(action)
        # Limit history size to avoid unnecessary memory usage
        if len(self.move_history) > HISTORY_SIZE:
            self.move_history.pop(0)

    def minimax(self, board: Board, depth: int, maximizing: bool) -> float:
        """
        Minimax algorithm with fixed depth for decision-making.
        Args:
            board: Current game board state
            depth: Depth of search
            maximizing: Boolean, True if maximizing player, False if minimizing
        Returns:
            Score of the board state
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        valid_actions = board.get_valid_actions()
        if not valid_actions:
            return self.evaluate_board(board)

        if maximizing:
            max_eval = float('-inf')
            for action in valid_actions:
                simulated_board = self.simulate_action(board, action)
                v_eval = self.minimax(simulated_board, depth - 1, False)
                max_eval = max(max_eval, v_eval)
            return max_eval
        else:
            min_eval = float('inf')
            for action in valid_actions:
                simulated_board = self.simulate_action(board, action)
                v_eval = self.minimax(simulated_board, depth - 1, True)
                min_eval = min(min_eval, v_eval)
            return min_eval

    def evaluate_board(self, board: Board) -> float:
        """
        Evaluate the desirability of a board state for the agent.
        Args:
            board: Current game board state
        Returns:
            Evaluation score
        """
        my_soldiers = board.count_soldiers(self.soldier_value)
        opponent_soldiers = board.count_soldiers(
            Soldier.RED if self.soldier_value == Soldier.BLUE else Soldier.BLUE
        )

        # Simple heuristic: piece count difference
        return my_soldiers - opponent_soldiers

    def simulate_action(self, board: Board, action: Dict) -> Board:
        """
        Simulate the result of an action on the board.
        Args:
            board: Current game board state
            action: Action to simulate
        Returns:
            A new board object representing the state after the action
        """
        simulated_board = Board()
        simulated_board.battle_field = board.battle_field
        simulated_board.soldiers = board.soldiers.copy()
        simulated_board.last_action = board.last_action
        simulated_board.is_multiple_capture = board.is_multiple_capture

        if action['type'] == 'CAPTURE_SOLDIER':
            simulated_board.capture_soldier(action)
        elif action['type'] == 'MOVE_SOLDIER':
            simulated_board.move_soldier(action)

        return simulated_board
