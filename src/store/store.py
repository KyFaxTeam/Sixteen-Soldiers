from typing import Callable, Dict, List
from agents.base_agent import BaseAgent
from models.board import Board
from models.time_manager import TimeManager
from utils.const import  Soldier
from utils.speed import GameSpeed


initial_state = {
    "board": Board(),
    "time_manager": TimeManager(),
    "is_game_over": False,
    "is_game_paused": False,
    "is_game_started": False,
    "current_soldier_value": Soldier.RED,
    "winner": None,
    "history": [],
    "agents": {},
    "agents_info_index": {
        Soldier.RED: None,
        Soldier.BLUE: None
    }
}
class Store:
    def __init__(self, reducer: Callable[[Dict, Dict], Dict]):
        self.state = initial_state
        self.reducer = reducer
        self.subscribers: List[Callable[[Dict], None]] = []
        self.game_speed = GameSpeed()
    
    def register_agents(self, agent1: BaseAgent, agent2: BaseAgent):
        """Register a new agent in the state using its unique ID if not already registered"""
        
        payload_1 = agent1.to_dict()
        payload_2 = agent2.to_dict()

        self.dispatch({
            "type": "REGISTER_AGENTS",
            "payload1": payload_1,
            "payload2": payload_2,
        })

    def get_state(self) -> Dict:
        return self.state
    
    def dispatch(self, action: Dict):
        state = self.reducer(self.state, action)
        
        if state is None:
            self.dispatch({"type": "PAUSE_GAME"})
        else :
            self.state = state   
            for subscriber in self.subscribers:
                subscriber(self.state)


    def subscribe(self, subscriber: Callable[[Dict], None]):
        self.subscribers.append(subscriber)
    
    def get_agent_info(self, soldier_value: Soldier) -> Dict:
        """Get agent information based on the soldier_value"""
        info_index = self.state["agents_info_index"].get(soldier_value)
        if info_index:
            return self.state["agents"].get(info_index, {})
        return {}