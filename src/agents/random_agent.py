import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    """AI agent that plays random valid moves"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Random Team"
        
    
    
    def choose_action(self, board: Board) -> Dict:
        """
        Choose a random action from valid moves.
        Args:
            board: Current game board state
        Returns:
            Randomly chosen valid action for the soldier_value
        """
        valid_actions = board.get_valid_actions()
        
        return random.choice(valid_actions)
        
    
