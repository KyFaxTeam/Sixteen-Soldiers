
from typing import Dict
from agents.base_agent import BaseAgent
from models.board import Board
from utils.const import Soldier
import copy
import math

class Agent(BaseAgent):
    """AI agent that uses alpha-beta pruning to choose moves."""

    def __init__(self, soldier_value: Soldier, depth: int = 3):
        super().__init__(soldier_value)
        self.name = "AlphaBeta Agent"
        self.depth = depth

    def choose_action(self, board: Board):
        """
        Choose the best action using alpha-beta pruning.
        """
        _, best_action = self.alphabeta(board, self.depth, -math.inf, math.inf, True)
        return best_action

    def apply_action(board:Board, action: Dict):
        """Apply an action to the board."""
        action_type = action['type']
        if action_type == 'MOVE_SOLDIER':
            board.move_soldier(action)
        elif action_type == 'CAPTURE_SOLDIER':
            board.capture_soldier(action)

    def alphabeta(self, board: Board, depth: int, alpha: float, beta: float, maximizing_player: bool):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board), None

        soldier_value = self.soldier_value if maximizing_player else self.get_opponent_soldier()
        valid_actions = board.get_valid_actions(soldier_value)

        if not valid_actions:
            return self.evaluate(board), None

        best_action = None

        if maximizing_player:
            max_eval = -math.inf
            for action in valid_actions:
                new_board = copy.deepcopy(board)
                new_board.apply_action(action)
                eval_score, _ = self.alphabeta(new_board, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_action = action
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_action
        else:
            min_eval = math.inf
            for action in valid_actions:
                new_board = copy.deepcopy(board)
                self.apply_action(new_board, action)
                eval_score, _ = self.alphabeta(new_board, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_action = action
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_action

    def evaluate(self, board: Board):
        """
        Evaluate the board state from the perspective of this agent.
        """
        return board.count_pieces(self.soldier_value) - board.count_pieces(self.get_opponent_soldier())

    def get_opponent_soldier(self) -> Soldier:
        return Soldier.RED if self.soldier_value == Soldier.BLUE else Soldier.BLUE