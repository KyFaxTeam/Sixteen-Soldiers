from typing import Dict, List
from models.player import Player
from models.move import Move

def initialize_players(state: Dict) -> Dict:
    """
    Initialise les joueurs avec leurs pions sur le plateau.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        dict: État mis à jour avec les joueurs initialisés.
    """
    joueurs = [
        Player(id="red", nom="Joueur Rouge", couleur="red"),
        Player(id="green", nom="Joueur Vert", couleur="green")
    ]
    state = state.copy()
    state["players"] = joueurs
    return state

def change_current_player(state: Dict) -> Dict:
    """
    Passe au joueur suivant.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        dict: État mis à jour avec le joueur courant changé.
    """
    nouveaux_joueurs = state["players"]
    index = state.get("current_player_index", 0)
    index = (index + 1) % len(nouveaux_joueurs)
    state = state.copy()
    state["current_player_index"] = index
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
        case 'INITIALIZE_PLAYERS':
            return initialize_players(state)
        case 'CHANGE_CURRENT_PLAYER':
            return change_current_player(state)
        case 'CAPTURE_PIECE':
            joueur = next(j for j in state["players"] if j.id == action["joueur_id"])
            joueur.capturer_piece()
            return state
        case 'LOSE_PIECE':
            joueur = next(j for j in state["players"] if j.id == action["joueur_id"])
            joueur.perdre_piece()
            return state
        case 'FINISH_GAME':
            for joueur in state["players"]:
                joueur.conclure_partie()
            return state
        case 'PLAY_MOVE':
            joueur = next(j for j in state["players"] if j.id == action["joueur_id"])
            coup = Move(action["from_pos"], action["to_pos"], joueur.id, action["timestamp"])
            joueur.jouer_coup(coup)
            return state
        case _:
            return state