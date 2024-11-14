from dataclasses import dataclass, field
from typing import List,  Dict


@dataclass
class Stats:
    """Player statistics"""
    wins: int = 0
    losses: int = 0
    draws: int = 0
    total_games: int = 0
    total_moves: int = 0
    average_time_per_move: float = 0.0

@dataclass
class Player:
    """Represents a player in the Sixteen Soldiers game"""
    id: str
    color: str
    remaining_pieces: int = 16
    
    def __init__(self, id: str, color: str):
        """
        Initialize a player with the given parameters
        
        Args:
            id: Unique identifier for the player
            color: Player's color
        """
        self.id = id
        self.color = color
        self.remaining_pieces = 16

    def lose_piece(self) -> None:
        """Decrements the number of remaining pieces"""
        self.remaining_pieces = max(0, self.remaining_pieces - 1)

    def to_dict(self):
        """Convert Player object to dictionary"""
        return {
            "id": self.id,
            "color": self.color,
            "remaining_pieces": self.remaining_pieces,
        }




