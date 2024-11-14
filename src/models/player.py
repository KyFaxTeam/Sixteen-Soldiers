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
    color: str  # Renamed from couleur for consistency
    remaining_pieces: int = 16
    stats: Stats = field(default_factory=Stats)
    is_active: bool = False
    
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
        self.stats = Stats()
        self.is_active = False

    def lose_piece(self) -> None:
        """Decrements the number of remaining pieces"""
        self.remaining_pieces = max(0, self.remaining_pieces - 1)
    
    def conclude_game(self, is_winner: bool) -> None:
        """
        Updates player statistics after game conclusion
        
        Args:
            is_winner: Whether this player won the game
        """
        self.stats.total_games += 1
        if is_winner:
            self.stats.wins += 1
        else:
            self.stats.losses += 1
            
        if self.stats.total_moves > 0:
            self.stats.average_time_per_move = (
                self.time_control.allowing_time - self.time_control.remaining_time
            ) / self.stats.total_moves

    def to_dict(self):
        """Convert Player object to dictionary"""
        return {
            "id": self.id,
            "color": self.color,
            "remaining_pieces": self.remaining_pieces,
            "stats": self.stats.__dict__,
            "is_active": self.is_active,
        }




