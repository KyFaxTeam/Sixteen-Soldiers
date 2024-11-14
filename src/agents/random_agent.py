import random
from typing import Dict, List
from agents.base_agent import BaseAgent
from models.board import Board
from models.player import Player

class RandomAgent(BaseAgent):
    """
    AI agent that plays random valid moves, inherits from BaseAgent.
    """
    
    def __init__(self, id: str, nom: str, couleur: str):
        """
        Initialize the random agent.
        
        Args:
            id: The ID of the player
            nom: The name of the player
            couleur: The color of the player
        """
        super().__init__(id, nom, couleur)
        self.rng = random.Random()
    
    def choose_action(self, board: Board, player: Player) -> Dict:
        """
        Choose a random action from valid moves and captures for the player.
        
        Args:
            board: Current game board state
            player: Player for whom to choose the action
            
        Returns:
            Randomly chosen valid action for the player
            
        Raises:
            ValueError: If no valid moves are available
        """
        valid_actions = self.get_valid_moves(board, player)
        
        if not valid_actions:
            raise ValueError("No valid moves available")
            
        return self.rng.choice(valid_actions)
    
    def set_seed(self, seed: int) -> None:
        """
        Set the random seed for reproducibility.
        
        Args:
            seed: Random seed value
        """
        self.rng.seed(seed)