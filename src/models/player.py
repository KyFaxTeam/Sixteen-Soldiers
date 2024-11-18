from dataclasses import dataclass
from typing import List, Dict



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

    def count_pieces(self, board) -> int:
        """Count remaining pieces for this player on the board"""
        return sum(1 for value in board.soldiers.values() if value == self.id)




