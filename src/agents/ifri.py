from collections import deque
import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    """AI agent prioritizing multi-captures with loop and opponent move prediction"""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "IFRI"
        self.depth_limit = 3  # Max depth for Minimax
        self.move_history = deque(maxlen=3)  # Track the last 3 moves for loop detection

    def choose_action(self, board: Board) -> Dict:
        """
        Chooses the best move within the allotted time, prioritizing multi-captures.
        Args:
            board (Board): Current game board state.
        Returns:
            Dict: Best action to take.
        """
        valid_actions = board.get_valid_actions()
        if not valid_actions:
            return random.choice(valid_actions)

        # Prioritize capture actions
        capture_actions = [action for action in valid_actions if action["type"] == "CAPTURE_SOLDIER"]
        if capture_actions:
            return max(capture_actions, key=lambda action: self.evaluate_action(board, action))

        # Evaluate non-capture actions if no captures are available
        best_action = max(valid_actions, key=lambda action: self.evaluate_action(board, action))
        self.move_history.append(best_action)  # Track the chosen action
        return best_action

    def evaluate_action(self, board: Board, action: Dict) -> int:
        """
        Evaluates the score of a specific action.
        Args:
            board (Board): Current game board state.
            action (Dict): Action to evaluate.
        Returns:
            int: Score of the action.
        """
        # Simulate the action
        prev_state = self.simulate_action(board, action)

        # Evaluate the board after the action
        score = self.evaluate_board(board)

        # Predict and penalize for the opponent's best move
        opponent_action = self.predict_opponent_action(board)
        if opponent_action:
            opponent_score = self.simulate_opponent_response(board, opponent_action)
            score -= opponent_score  # Penalize based on predicted opponent advantage

        # Penalize repeated back-and-forth moves
        if self.is_repeating_back_and_forth(action):
            score -= 50  # Penalize heavily to avoid loops

        # Undo the action
        self.undo_action(board, action, prev_state)
        return score

    def predict_opponent_action(self, board: Board) -> Dict:
        """
        Predicts the opponent's best action.
        Args:
            board (Board): Current game board state.
        Returns:
            Dict: Predicted action for the opponent.
        """
        opponent = Soldier(not bool(self.soldier_value))
        opponent_actions = board.get_valid_actions()
        if not opponent_actions:
            return None

        # Assume the opponent will choose the action with the highest heuristic value
        return max(opponent_actions, key=lambda action: self.simulate_opponent_response(board, action))

    def simulate_opponent_response(self, board: Board, action: Dict) -> int:
        """
        Simulates the opponent's response and evaluates the resulting board state.
        Args:
            board (Board): Current game board state.
            action (Dict): Opponent's action to simulate.
        Returns:
            int: Heuristic evaluation of the board after the opponent's action.
        """
        prev_state = self.simulate_action(board, action)
        opponent_score = self.evaluate_board(board)
        self.undo_action(board, action, prev_state)
        return opponent_score

    def is_repeating_back_and_forth(self, action: Dict) -> bool:
        """
        Checks if the current action creates a back-and-forth loop.
        Args:
            action (Dict): The action to check.
        Returns:
            bool: True if the action is part of a back-and-forth loop.
        """
        if len(self.move_history) < 2:
            return False  # Not enough history for a back-and-forth pattern

        last_action = self.move_history[-1]
        return (
            last_action["from_pos"] == action["to_pos"]
            and last_action["to_pos"] == action["from_pos"]
        )

    def evaluate_board(self, board: Board) -> int:
        """
        Heuristic evaluation of the board state.
        """
        my_soldiers = board.count_soldiers(self.soldier_value)
        opponent = Soldier(not bool(self.soldier_value))
        opponent_soldiers = board.count_soldiers(opponent)

        # Emphasize soldier count as the primary metric
        return (my_soldiers - opponent_soldiers) * 10

    def simulate_action(self, board: Board, action: Dict) -> Dict:
        """
        Simulates an action on the board and returns the previous state for undoing.
        Args:
            board (Board): Current game board state.
            action (Dict): Action to simulate.
        Returns:
            Dict: Previous state of the board at affected positions.
        """
        prev_state = {
            "from_pos": board.get_soldier_value(action["from_pos"]),
            "to_pos": board.get_soldier_value(action["to_pos"]),
            "captured_pos": None,
        }

        # Move or capture
        if action["type"] == "CAPTURE_SOLDIER":
            prev_state["captured_pos"] = board.get_soldier_value(action["captured_soldier"])
            board.capture_soldier(action)
        else:
            board.move_soldier(action)

        return prev_state

    def undo_action(self, board: Board, action: Dict, prev_state: Dict):
        """
        Undoes a simulated action, restoring the previous state.
        Args:
            board (Board): Current game board state.
            action (Dict): Action to undo.
            prev_state (Dict): Previous state of the board at affected positions.
        """
        # Restore the positions
        board.soldiers[action["from_pos"]] = prev_state["from_pos"]
        board.soldiers[action["to_pos"]] = prev_state["to_pos"]

        if action["type"] == "CAPTURE_SOLDIER" and prev_state["captured_pos"] is not None:
            board.soldiers[action["captured_soldier"]] = prev_state["captured_pos"]
