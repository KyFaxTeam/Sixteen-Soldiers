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
    is_game_over: bool = False  # Renommé de game_over à is_game_over
    is_game_paused: bool = False
    current_player: int = 0  # Renommé de current_player_index à current_player
    winner: Dict = field(default_factory=dict)
    history: List = field(default_factory=list)
    players: List[Player] = field(default_factory=lambda: [
        Player(id=PLAYER_CONFIG["PLAYER_1"], 
              color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_1"]]),
        Player(id=PLAYER_CONFIG["PLAYER_2"], 
              color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_2"]])
    ])
    agents: Dict[str, Dict] = field(default_factory=dict)

class Store:
    def __init__(self, reducer: Callable[[Dict, Dict], Dict]):
        self.state = StateModel().__dict__
        self.reducer = reducer
        self.subscribers: List[Callable[[Dict], None]] = []
    
    def register_agent(self, agent: BaseAgent):
        """Enregistre un nouvel agent dans le state avec un ID unique"""
        current_agents = self.state.get("agents", {})
        new_agent_id = len(current_agents)
        agent.set_agent_id(new_agent_id)
        
        self.dispatch({
            "type": "REGISTER_AGENT",
            "agent": agent.to_dict()
        })
        
    def get_state(self) -> Dict:
        return self.state
    
    def dispatch(self, action: Dict):
        self.state = self.reducer(self.state, action)
        for subscriber in self.subscribers:
            subscriber(self.state)
    
    def subscribe(self, subscriber: Callable[[Dict], None]):
        self.subscribers.append(subscriber)