from typing import Dict
from dataclasses import dataclass
from src.utils.const import TIMINGS, Soldier

@dataclass
class TimeControl:
    initial_time: float
    remaining_time: float
    
    def __init__(self, initial_time: float):
        self.initial_time = initial_time
        self.remaining_time = initial_time

    def update(self, elapsed_time: float) -> None:
        self.remaining_time = max(0.0, self.remaining_time - elapsed_time)
    
    def is_time_up(self) -> bool:
        return self.remaining_time <= 0

class TimeManager:
    def __init__(self):
        self.time_controls: Dict[Soldier, TimeControl] = {
            Soldier.RED: TimeControl(TIMINGS["AI_TIMEOUT"]),
            Soldier.BLUE: TimeControl(TIMINGS["AI_TIMEOUT"])
        } 
    
    def set_time_limits(self, time_limits: Dict[int, float]) -> None:
        for soldier_value, time_limit in time_limits.items():
            self.time_controls[soldier_value] = TimeControl(time_limit)
    
    def update_player_time(self, soldier_value: Soldier, elapsed: float) -> None:
        if soldier_value in self.time_controls:
            return self.time_controls[soldier_value].update(elapsed)
    
    def is_time_up(self, soldier_value: Soldier) -> bool:
        return self.time_controls[soldier_value].is_time_up()
    
    def get_remaining_time(self, soldier_value: Soldier) -> float:
        return self.time_controls[soldier_value].remaining_time
