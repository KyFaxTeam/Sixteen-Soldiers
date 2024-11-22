from typing import Dict
from dataclasses import dataclass
from utils.const import INITIAL_VALUES

@dataclass
class TimeControl:
    initial_time: float
    remaining_time: float
    
    def __init__(self, initial_time: float):
        self.initial_time = initial_time
        self.remaining_time = initial_time

    def update(self, elapsed_time: float) -> None:
        """Update remaining time and return if time is up"""
        self.remaining_time = max(0.0, self.remaining_time - elapsed_time)
    
    def is_time_up(self) -> bool:
        return self.remaining_time <= 0

class TimeManager:
    def __init__(self):
        self.time_controls: Dict[int, TimeControl] = {}  # Changed str to int for player_id
    
    def set_time_limits(self, time_limits: Dict[int, float]) -> None:
        """Initialize time controls for all players"""
        for player_id, time_limit in time_limits.items():
            self.time_controls[player_id] = TimeControl(time_limit)
    
    def update_player_time(self, player_id: int, elapsed: float) -> None:
        """Update time for a player and return if they ran out of time"""
        if player_id in self.time_controls:
            self.time_controls[player_id].update(elapsed)
    
    def is_time_up(self, player_id: int) -> bool:
        """Check if a player has run out of time"""
        return self.time_controls[player_id].is_time_up() if player_id in self.time_controls else True
    
    def get_remaining_time(self, player_id: int) -> float:
        """Get remaining time for a player"""
        return self.time_controls[player_id].remaining_time if player_id in self.time_controls else 0.0
