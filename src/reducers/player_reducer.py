from typing import Dict
from models.player import Player
from utils.const import PLAYER_CONFIG

# def initialize_players(state: Dict) -> Dict:
#     """
#     Initialise les joueurs avec leurs pions sur le plateau.
#     """
#     joueurs = [
#         Player(id=PLAYER_CONFIG["PLAYER_1"], 
               
#                color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_1"]]),
#         Player(id=PLAYER_CONFIG["PLAYER_2"], 
               
#                color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_2"]])
#     ]
#     state = state.copy()
#     state["players"] = joueurs
#     return state

def reset_players(state:Dict) -> Dict:
    """
    Réinitialise les joueurs avec 16 pions chacun.
    """
    state = state.copy()
    for joueur in state["players"]:
        joueur.remaining_pieces = 16
    return state

def change_current_player(state: Dict) -> Dict:
    """
    Passe au joueur suivant en inversant le signe (-1 → 1 ou 1 → -1)
    """
    state = state.copy()
    current_player = state.get("current_player", PLAYER_CONFIG["PLAYER_1"])
    state["current_player"] = -current_player
    return state


def player_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications liées aux joueurs.
    """
    match action['type']:
        case 'RESET_PLAYERS':
            return reset_players(state)
        case 'CHANGE_CURRENT_PLAYER':
            return change_current_player(state)
        case 'LOSE_PIECE':
            joueur = next(j for j in state["players"] if j.id == action["player_id"])  # Changé de joueur_id à player_id
            joueur.lose_piece()
            return state
        case _:
            return state