from typing import Dict, List
from models.player import Player
from models.move import Move
from utils.const import PLAYER_CONFIG

def initialize_players(state: Dict) -> Dict:
    """
    Initialise les joueurs avec leurs pions sur le plateau.
    """
    joueurs = [
        Player(id=PLAYER_CONFIG["PLAYER_1"], 
               
               color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_1"]]),
        Player(id=PLAYER_CONFIG["PLAYER_2"], 
               
               color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_2"]])
    ]
    state = state.copy()
    state["players"] = joueurs
    return state

def change_current_player(state: Dict) -> Dict:
    """
    Passe au joueur suivant en inversant le signe (-1 → 1 ou 1 → -1)
    """
    state = state.copy()
    current_player = state.get("current_player", PLAYER_CONFIG["PLAYER_1"])
    state["current_player"] = -current_player
    return state

def is_game_over(state: Dict) -> bool:
    """
    Vérifie si la partie est terminée.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        bool: True si la partie est terminée, False sinon.
    """
    return state.get("game_over", False)

def get_winner(state: Dict) -> Player:
    """
    Retourne le joueur gagnant.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        Player: Joueur gagnant.
    """
    return state.get("winner", None)

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

def player_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications liées aux joueurs.
    """
    match action['type']:
        case 'CHANGE_CURRENT_PLAYER':
            return change_current_player(state)
        case 'LOSE_PIECE':
            joueur = next(j for j in state["players"] if j.id == action["player_id"])  # Changé de joueur_id à player_id
            joueur.lose_piece()
            return state
        case _:
            return state