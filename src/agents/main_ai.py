import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

# This file contains the main AI agent that you will use to play the game. It is a main class that we get if you finish your implementation of the game.
class Agent(BaseAgent):
    """AI agent that plays your choice"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Your Team" # You need to replace Your Team with your team name
        
    
    
    def choose_action(self, board: Board) -> Dict:

        """
        Choose an action from valid moves.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """

    
        valid_actions = board.get_valid_actions()
        

        return random.choice(valid_actions) # You need to replace random.choice(valid_actions) with your choice of action or method to choose an action
        
    
