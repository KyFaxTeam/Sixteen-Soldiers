
from typing import  Callable, Dict, List

# STATE_STRUCTURE: TypedDict = {
#         "board": Board,          # Plateau de jeu
#         "time_manager": TimeManager,  # Gestionnaire de temps
#         "game_over": bool,       # True si partie terminée
#         "current_player_index": int,  # Index du joueur courant (0 ou 1)
#         "winner": Optional[str], # ID du gagnant ou None
#         "players": List[Player], # Liste des 2 joueurs
#         "history": List[dict]    # Historique des coups
#     }


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