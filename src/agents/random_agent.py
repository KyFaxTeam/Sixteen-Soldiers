import random
from typing import Dict, List
from agents.base_agent import BaseAgent
from models.board import Board
from models.player import Player

class RandomAgent(BaseAgent):
    """
    AI agent that plays random valid moves, inherits from BaseAgent.
    """
    
    def __init__(self, player: Player, name: str = "Random Agent"):
        """
        Initialize the random agent.
        
        Args:
            player: The player instance
            name: The agent's name
        """
        super().__init__(player, name)
        self.rng = random.Random()
    
    def choose_action(self, board: Board) -> Dict:
        """
        Choose a random action from valid moves.
        
        Args:
            board: Current game board state
            
        Returns:
            Randomly chosen valid action for the player
            
        Raises:
            ValueError: If no valid moves are available
        """
        try:
            valid_actions = board.get_valid_actions(player=self.player.id)
            if not valid_actions:
                self.logger.info(f"No valid moves available for {self.name}")
                return {'type': 'NO_OP', 'player_id': self.player.id}
            return self.rng.choice(valid_actions)
        except Exception as e:
            self.logger.error(f"Error choosing action: {e}")
            raise
    
    def _select_action(self, board: Board, valid_actions: List[Dict], time_limit: float) -> Dict:
        """
        Randomly choose an action from valid actions.
        
        Args:
            board: Current game board state
            valid_actions: List of valid actions
            time_limit: Time limit for choosing an action
            
        Returns:
            Randomly chosen valid action
        """
        action = self.rng.choice(valid_actions)
        return action

    def set_seed(self, seed: int) -> None:
        """
        Set the random seed for reproducibility.
        
        Args:
            seed: Random seed value
        """
        self.rng.seed(seed)