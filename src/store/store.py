from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional

from agents.base_agent import BaseAgent
from models.board import Board
from models.player import Player
from models.time_manager import TimeManager
from utils.const import PLAYER_CONFIG

@dataclass
class StateModel:
    board: Board = field(default_factory=Board)
    time_manager: TimeManager = field(default_factory=TimeManager)  # Remove custom initialization
    game_over: bool = False
    is_game_paused: bool = False
    current_player_index: int = 0
    winner: Dict = field(default_factory=dict)
    history: List = field(default_factory=list)
    players: List[Player] = field(default_factory=lambda: [
        Player(id=PLAYER_CONFIG["PLAYER_1"], 
              color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_1"]]),
        Player(id=PLAYER_CONFIG["PLAYER_2"], 
              color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_2"]])
    ])

class Store:
    def __init__(self, reducer: Callable[[Dict, Dict], Dict]):
        self.state = StateModel().__dict__
        self.reducer = reducer
        self.subscribers: List[Callable[[Dict], None]] = []
        self.agents: Dict[str, Dict] = {}  # Stocker les agents sous forme de dictionnaires
    
    def register_agent(self, agent: BaseAgent):
        """Enregistre un nouvel agent sous forme de dictionnaire"""
        self.agents[agent.name] = agent.to_dict()
        
    def get_agent_info(self, agent_name: str) -> Dict:
        """Récupère les informations d'un agent par son nom"""
        return self.agents.get(agent_name)
    
    def get_all_agents_info(self) -> Dict[str, Dict]:
        """Récupère les informations de tous les agents"""
        return self.agents

    def get_state(self) -> Dict:
        return self.state
    
    def dispatch(self, action: Dict):
        self.state = self.reducer(self.state, action)
        for subscriber in self.subscribers:
            subscriber(self.state)
    
    def subscribe(self, subscriber: Callable[[Dict], None]):
        self.subscribers.append(subscriber)