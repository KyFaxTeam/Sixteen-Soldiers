import random
import os
from dataclasses import dataclass, field
import sys
from typing import List, Dict, Literal
from src.models.assets.index import Assets
from src.utils.const import Soldier
from src.utils.const import AGENT_DIR

@dataclass
class MatchPerformance:
    issue: Literal["win", "loss", "draw"]
    number_of_moves: int
    time: float
    opponent: str
    reason: str  # Added 'reason' attribute


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
            self.performances = [MatchPerformance(**performance) for performance in data.get("performances", [])]
            self.profile_img = data.get("profile_img", "")
        else:
            self.performances = []       
            # verify if an image name like the pseudo exists in the folder of agents
            # if not, get a random image
            
            if os.path.exists(os.path.join(AGENT_DIR, self.pseudo + ".png")):
                self.profile_img = os.path.join(AGENT_DIR, self.pseudo + ".png")
            else:  
                self.profile_img = self._get_random_avatar()

    
    def _get_random_avatar(self) -> str:
        """Gets a random avatar path from assets"""
        avatar_dir = Assets.dir_avatar
        
        avatar_files = [f for f in os.listdir(avatar_dir) 
                       if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if avatar_files:
            return os.path.join(avatar_dir, random.choice(avatar_files))
        return ""  
    

    def conclude_game(self, issue : Literal['win', 'loss', 'draw'], opponent_name: str, number_of_moves : int, time : float, reason: str) -> None:
        """Updates agent statistics after game conclusion"""

        performance = MatchPerformance(
            issue=issue,
            number_of_moves= number_of_moves,
            time=   time,
            opponent=opponent_name,
            reason=reason  # Include 'reason' when creating MatchPerformance
        )
        self.performances.append(performance)
        

    def to_dict(self) -> Dict:
        """Convert agent to dictionary representation"""
        return {
            "pseudo": self.pseudo,
            "name": self.name,
            "soldier_value": self.soldier_value,
            "profile_img": self.profile_img,
            "performances": [performance.__dict__ for performance in self.performances]
        }