from models.board import Board
from models.time_manager import TimeManager
from typing import Any, Callable, Dict, List

class Store:
    def __init__(self, initial_state: Dict, reducer: Callable[[Dict, Dict], Dict]):
        self.state = initial_state if initial_state is not None else {}
        self.reducer = reducer
        self.subscribers: List[Callable[[Dict], None]] = []
    
    def get_state(self) -> Dict:
        return self.state
    
    def dispatch(self, action: Dict):
        self.state = self.reducer(self.state, action)
        for subscriber in self.subscribers:
            subscriber(self.state)
    
    def subscribe(self, subscriber: Callable[[Dict], None]):
        self.subscribers.append(subscriber)