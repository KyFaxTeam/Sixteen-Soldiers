
from typing import Dict, Optional
from models.player import Player

def get_current_player(state: Dict) -> Player:
    """
    Retourne le joueur courant.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        Player: Joueur courant.
    """
    index = state.get("current_player_index", 0)
    return state["players"][index]

def get_winner(state: Dict) -> Optional[Player]:
    """
    Retourne le joueur gagnant.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        Optional[Player]: Joueur gagnant ou None.
    """
    return state.get("winner", None)

def is_game_over(state: Dict) -> bool:
    """
    Vérifie si la partie est terminée.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        bool: True si la partie est terminée, False sinon.
    """
    return state.get("game_over", False)