import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    """
    AI agent for the game, implementing advanced strategies for attack and defense.
    """

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "blacknight01"
        self.opponent = Soldier.RED if soldier_value == Soldier.BLUE else Soldier.BLUE

    def evaluate_action(self, action: Dict, board: Board) -> int:
        """
        Evaluate the desirability of a given action.
        Higher scores represent better moves.
        """
        from_pos = action['from_pos']
        to_pos = action['to_pos']
        action_type = action.get('type', 'MOVE_SOLDIER')
        score = 0

        # 1. Offensive strategy: prioritize captures
        if action_type == 'CAPTURE_SOLDIER':
            score += 50  # High reward for capturing an opponent soldier
            captured_pos = action['captured_soldier']

            # Check if the capture leads to another possible capture (multi-capture)
            if board.check_multi_capture(self.soldier_value, to_pos):
                score += 30  # Bonus for setting up a multi-capture

            # Evaluate the safety of the capturing position
            neighbors = board.get_neighbors(to_pos)
            if neighbors[self.opponent.name]:
                score -= 20  # Penalty if the position is exposed to opponent capture

        # 2. Defensive strategy: avoid risky moves
        neighbors = board.get_neighbors(to_pos)
        if neighbors[self.opponent.name]:
            score -= 10 * len(neighbors[self.opponent.name])  # Penalty for moving into a risky area

        # 3. Positional strategy: prioritize control of the center
        center_positions = ['c3', 'd3', 'd4', 'e3', 'e4', 'f3']
        if to_pos in center_positions:
            score += 20  # Reward for moving to a strategic position

        # 4. Formation strategy: encourage grouping of soldiers
        friendly_neighbors = len(neighbors[self.soldier_value.name])
        score += 5 * friendly_neighbors  # Reward for staying close to friendly soldiers

        # 5. Mobility: prioritize moves that increase options
        future_moves = board.get_valid_actions_for_position(to_pos)
        score += len(future_moves) * 2  # Reward for maintaining mobility

        return score

    def choose_action(self, board: Board) -> Dict:
        """
        Choose the best action based on an evaluation of all valid actions.
        """
        valid_actions = board.get_valid_actions()
        if not valid_actions:
            return None

        # Evaluate all valid actions
        action_scores = [
            (action, self.evaluate_action(action, board)) for action in valid_actions
        ]

        # Select the action with the highest score
        best_action = max(action_scores, key=lambda x: x[1])[0]

        return best_action
