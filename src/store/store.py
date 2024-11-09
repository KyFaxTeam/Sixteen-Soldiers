from models.board import Plateau
from models.time_manager import TimeManager

class Store:
    def __init__(self, reducer):
        self.state = {
            'plateau': Plateau(),
            'time_manager': TimeManager(),
            'joueurs': [], 
            'historique': [],  
            
        }
        self.reducer = reducer
        self.subscribers = []
    
    def get_state(self):
        return self.state
    
    def dispatch(self, action):
        self.state = self.reducer(self.state, action)
        for subscriber in self.subscribers:
            subscriber(self.state)
    
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)