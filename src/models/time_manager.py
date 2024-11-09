from dataclasses import dataclass
from typing import Dict

from dataclasses import dataclass
from typing import Optional

@dataclass
class TimeControl:
    """Manages time control for a player"""
    allowing_time: float
    remaining_time: float = 0.0
    last_move_time: Optional[float] = None
    
    def __init__(self, allowing_time: float):
        """
        Initialize time control
        
        Args:
            allowing_time: Total time allowed in seconds
            increment: Time increment after each move in seconds
        """
        self.allowing_time = allowing_time
        self.remaining_time = allowing_time
        
        self.last_move_time = None
    
    def update_time(self, elapsed_time: float) -> None:
        """
        Updates remaining time after a move
        
        Args:
            elapsed_time: Time spent on the move in seconds
        """
        self.remaining_time = max(0.0, self.remaining_time - elapsed_time)
        self.remaining_time += self.increment
        self.last_move_time = elapsed_time
    
    def is_timeout(self) -> bool:
        """Returns whether time has run out"""
        return self.remaining_time <= 0


class TimeManager:
    def __init__(self):
        self.time_controls: Dict[str, TimeControl] = {}
        
    def add_player(self, player_id: str, allowing_time: float):
        self.time_controls[player_id] = TimeControl(
            allowing_time=allowing_time,
            remaining_time=allowing_time
        )
    
    def update_player_time(self, player_id: str, elapsed: float):
        if player_id in self.time_controls:
            self.time_controls[player_id].update_time(elapsed)
    
    def get_remaining_time(self, player_id: str) -> float:
        return self.time_controls[player_id].remaining_time if player_id in self.time_controls else 0.0
