from models.plateau import Plateau

class Store:
    def __init__(self, reducer):
        self.state = {
            'plateau': Plateau(),
            'joueurs': [],  # Initialiser avec une liste vide ou les joueurs initiaux
            'historique': []  # Liste de Coup
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