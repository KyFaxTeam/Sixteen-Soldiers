from typing import List, Dict
from models.board import Board
from models.player import Player


class BaseAgent:
    """
    Base class for AI agents in the Sixteen Soldiers game.
    Provides an interface for agents to choose actions based on the current game state.
    """
    
    def __init__(self, name: str = "BaseAgent"):
        """
        Initialize the base agent.
        
        Args:
            name: The name of the agent
        """
        self.name = name
        self.total_moves = 0
        self.total_time = 0.0
    
    def choose_action(self, board: Board, player: Player) -> Dict:
        """
        Abstract method to choose an action based on the current board state and player.
        
        Args:
            board: Current game board state
            player: Player for whom to choose the action
            
        Returns:
            The chosen action for the player
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        raise NotImplementedError("This method must be implemented by subclasses")
    
    def get_valid_moves(self, board: Board, player: Player) -> List[Dict]:
        """
        Get all valid moves for the current player.
        
        Args:
            board: Current game board state
            player: Current player
            
        Returns:
            List of valid actions
        """
        return board.get_valid_actions(player)
    
    def reset_stats(self) -> None:
        """Reset the agent's statistics."""
        self.total_moves = 0
        self.total_time = 0.0