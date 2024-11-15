from dataclasses import dataclass
from typing import List, Dict
from models.board import Board
from models.player import Player

@dataclass
class AgentStats:
    """Agent statistics"""
    wins: int = 0
    losses: int = 0
    draws: int = 0
    total_games: int = 0
    total_moves: int = 0
    average_time_per_move: float = 0.0

class BaseAgent:
    """
    Base class for AI agents in the Sixteen Soldiers game.
    Provides an interface for agents to choose actions based on the current game state.
    """
    
    def __init__(self, player: Player, name: str):
        """
        Initialize the base agent.
        
        Args:
            player: The player instance
            name: The agent's name
        """
        self.player = player  # Composition instead of inheritance
        self.name = name
        self.stats = AgentStats()
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
        self.stats = AgentStats()
        self.total_time = 0.0

    def conclude_game(self, is_winner: bool) -> None:
        """Updates agent statistics after game conclusion"""
        self.stats.total_games += 1
        if is_winner:
            self.stats.wins += 1
        else:
            self.stats.losses += 1
            
        if self.stats.total_moves > 0:
            self.stats.average_time_per_move = self.total_time / self.stats.total_moves