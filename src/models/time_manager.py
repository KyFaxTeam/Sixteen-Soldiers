from typing import Dict, Optional
from dataclasses import dataclass
from utils.const import INITIAL_VALUES

@dataclass
class TimeControl:
    allowing_time: float
    remaining_time: float = 0.0
    last_move_time: Optional[float] = None

    def __init__(self, allowing_time: float):
        self.allowing_time = allowing_time
        self.remaining_time = allowing_time
        self.last_move_time = None

    def update_time(self, elapsed_time: float) -> None:
        self.remaining_time = max(0.0, self.remaining_time - elapsed_time)
        self.last_move_time = elapsed_time

    def is_timeout(self) -> bool:
        """Returns whether time has run out"""
        return self.remaining_time <= 0

    def to_dict(self) -> dict:
        """Convert TimeControl object to dictionary"""
        return {
            "allowing_time": self.allowing_time,
            "remaining_time": self.remaining_time,
            "last_move_time": self.last_move_time
        }
    
class TimeManager:
    def __init__(self):
        self.time_controls: Dict[str, TimeControl] = {}
        
    def add_player(self, player_id: str, allowing_time: float = INITIAL_VALUES['TIMER']):
        self.time_controls[player_id] = TimeControl(allowing_time=allowing_time)
    
    def update_player_time(self, player_id: str, elapsed: float):
        if player_id in self.time_controls:
            self.time_controls[player_id].update_time(elapsed)
    
    def get_remaining_time(self, player_id: str) -> float:
        return self.time_controls[player_id].remaining_time if player_id in self.time_controls else 0.0

    def set_time_limits(self, time_limits: Dict[str, float]):
        """
        Initialise les limites de temps pour chaque joueur.

        Args:
            time_limits (dict): Dictionnaire avec player_id comme clé et temps en secondes comme valeur.
        """
        for player_id, allowing_time in time_limits.items():
            self.add_player(player_id, allowing_time)
    
    def to_dict(self) -> dict:
        """Convert TimeManager object to dictionary"""
        return {
            "time_controls": {player_id: tc.to_dict() for player_id, tc in self.time_controls.items()}
        }
