import random
import os
from dataclasses import dataclass, field
import sys
from typing import List, Dict, Literal
from models.assets.index import Assets
from utils.const import  Soldier

@dataclass
class MatchPerformance:
    issue : Literal["win", "loss", "draw"]
    number_of_moves: int
    time: float
    opponent: str

@dataclass
class AgentStats:
    total_games: int = 0
    performances: List[MatchPerformance] = field(default_factory=list)

class BaseAgent:
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        """
        Initialize the base agent.
        Args:
            soldier_value: The player configuration for the agent
        """
        self.soldier_value = soldier_value
        self.pseudo = os.path.basename(sys.modules[self.__module__].__file__).replace(".py", "")
        if data:
            self.profile_img = data.get("profile_img", "")
            self.stats = AgentStats(**data.get("stats", {}))
        else :
            self.stats = AgentStats()
            self.profile_img = self._get_random_avatar()

    
    def _get_random_avatar(self) -> str:
        """Gets a random avatar path from assets"""
        avatar_dir = Assets.dir_avatar
        avatar_files = [f for f in os.listdir(avatar_dir) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if avatar_files:
            return os.path.join(avatar_dir, random.choice(avatar_files))
        return ""  
    

    def conclude_game(self, issue : Literal['win', 'loss', 'draw'], opponent_name: str, number_of_moves : int, time : float) -> None:
        """Updates agent statistics after game conclusion"""

        self.stats.total_games += 1
        
        performance = MatchPerformance(
            issue=issue,
            number_of_moves= number_of_moves,
            time=   time,
            opponent=opponent_name
        )
        self.stats.performances.append(performance)
        

    def to_dict(self) -> Dict:
        """Convert agent to dictionary representation"""
        return {
            "pseudo": self.pseudo,
            "name": self.name,
            "soldier_value": self.soldier_value,
            "profile_img": self.profile_img,
            "stats": self.stats.__dict__
        }