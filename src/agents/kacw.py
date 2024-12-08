
import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "KACW"  # Will be replaced with actual team name
    
    def choose_action(self, board: Board) -> Dict:
        valid_actions = board.get_valid_actions()
        capture_actions = [action for action in valid_actions if action['type'] == 'CAPTURE_SOLDIER']
        if capture_actions:
            return random.choice(capture_actions)
        return random.choice(valid_actions)