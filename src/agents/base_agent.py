import logging
import time
import random
import os
from dataclasses import dataclass, field
from typing import List, Dict
from models.board import Board
from models.player import Player
from models.assets.index import Assets

@dataclass
class MatchPerformance:
    issue: str  # 'win', 'loss', 'draw'
    number_of_moves: int
    time: float
    opponent: str

@dataclass
class AgentStats:
    """Agent statistics"""
    total_games: int = 0
    performances: List[MatchPerformance] = field(default_factory=list)

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
        self.logger = logging.getLogger(__name__)
        self.profile_img = self._get_random_avatar()
        self.team_pseudo = f"Team {name}"  # Default team name
        self.agent_id = None  # Will be set when registered in store
        
    def set_agent_id(self, agent_id: int):
        """Set the unique ID for this agent instance"""
        self.agent_id = agent_id
    
    def _get_random_avatar(self) -> str:
        """Gets a random avatar path from assets"""
        avatar_dir = Assets.dir_avatar
        avatar_files = [f for f in os.listdir(avatar_dir) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if avatar_files:
            return os.path.join(avatar_dir, random.choice(avatar_files))
        return ""  # Return empty string if no avatar found
    
    def choose_action(self, board: Board, time_limit: float) -> Dict:
        """
        Abstract method to choose an action based on the current board state and player.
        
        Args:
            board: Current game board state
            time_limit: Time limit for the agent to choose an action
            
        Returns:
            The chosen action for the player
            
        Raises:
            NotImplementedError: This method must be implemented by subclasses
        """
        try:
            start_time = time.time()

            # Get valid actions
            valid_actions = board.get_valid_actions(player=self.player.id)
            if not valid_actions:
                self.logger.info(f"No valid moves available for {self.name}")
                return {'type': 'NO_OP', 'player_id': self.player.id}

            # Select action within time limit
            action = self._select_action(board, valid_actions, time_limit)

            elapsed_time = time.time() - start_time
            if (elapsed_time > time_limit):
                self.logger.error(f"{self.name} exceeded time limit of {time_limit} seconds")
                raise TimeoutError(f"Agent exceeded time limit of {time_limit} seconds")

            return action
            
        except Exception as e:
            self.logger.error(f"Error in {self.name}'s choose_action: {e}")
            raise

    def _select_action(self, board: Board, valid_actions: List[Dict], time_limit: float) -> Dict:
        # Should be implemented by subclasses
        raise NotImplementedError("This method must be implemented by subclasses")
    
    def reset_stats(self) -> None:
        """Reset the agent's statistics."""
        self.stats = AgentStats()

    def conclude_game(self, is_winner: bool, opponent_name: str, number_of_moves : int, time : float) -> None:
        """Updates agent statistics after game conclusion"""
        self.stats.total_games += 1
        issue = 'win' if is_winner else 'loss'
        if not is_winner and number_of_moves == 0:
            issue = 'draw'
        
        performance = MatchPerformance(
            issue=issue,
            number_of_moves= number_of_moves,
            time=   time,
            opponent=opponent_name
        )
        self.stats.performances.append(performance)
        

    def to_dict(self) -> Dict:
        """Convert the agent to a dictionary representation."""
        return {
            "id": self.agent_id,  # Added agent_id
            "name": self.name,
            "profile_img": self.profile_img,
            "team_pseudo": self.team_pseudo,
            "player_id": self.player.id,  # Added to link with player
            "stats": {
                "total_games": self.stats.total_games,
                "performances": [performance.__dict__ for performance in self.stats.performances]
            }
        }