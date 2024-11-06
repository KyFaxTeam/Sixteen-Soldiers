import pickle
from models.joueur import Joueur
from typing import Dict


def save_game(state: Dict) -> Dict:
    """
    Enregistre l'état actuel des joueurs et de l'historique.
   
    Args:
        state (dict): État global du jeu (joueurs, historique).
   
    Returns:
        dict: Représentation sérialisée de l'état des joueurs et de l'historique.
    """
    players = state['players']
    history = state['history']
    
    with open('save.pkl', 'wb') as f:
        pickle.dump({'players': players, 'history': history}, f)
    
    return {'players': players, 'history': history}

def load_game(save_file: str = 'save.pkl') -> Dict:
    """
    Charge l'état des joueurs et de l'historique à partir d'une sauvegarde.
   
    Args:
        save_file (str): Chemin du fichier de sauvegarde (par défaut 'save.pkl').
   
    Returns:
        dict: Nouvel état des joueurs et de l'historique.
    """
    try:
        with open(save_file, 'rb') as f:
            saved_state = pickle.load(f)
    except FileNotFoundError:
        print("No saved game found.")
        return None
    
    players = saved_state['players']
    history = saved_state['history']
    
    return {
        'players': players,
        'history': history
    }

def save_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les actions liées à la sauvegarde de la partie.
    """
    match action['type']:
        case 'SAVE_GAME':
            return save_game(state)
        case 'LOAD_GAME':
            loaded_state = load_game()
            # Mise à jour de l'état seulement si un chargement a réussi
            return loaded_state if loaded_state else state
        
        case _:
            return state