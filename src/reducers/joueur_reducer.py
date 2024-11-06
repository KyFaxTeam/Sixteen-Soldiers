from typing import Dict, List
from models.joueur import Joueur
from models.coup import Coup

def initialize_players(state: Dict) -> Dict:
    """
    Initialise les joueurs avec leurs pions sur le plateau.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        dict: État mis à jour avec les joueurs initialisés.
    """
    joueurs = [
        Joueur(id="red", nom="Joueur Rouge", couleur="red"),
        Joueur(id="green", nom="Joueur Vert", couleur="green")
    ]
    pass
def change_current_player(state: Dict) -> Dict:
    """
    Passe au joueur suivant.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        dict: État mis à jour avec le joueur courant changé.
    """
    joueurs = state["joueurs"]
    pass
def is_game_over(state: Dict) -> bool:
    """
    Vérifie si la partie est terminée.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        bool: True si la partie est terminée, False sinon.
    """
    joueurs = state["joueurs"]
    pass
def get_winner(state: Dict) -> Joueur:
    """
    Retourne le joueur gagnant.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        Joueur: Joueur gagnant.
    """
    joueurs = state["joueurs"]
    pass
def get_current_player(state: Dict) -> Joueur:
    """
    Retourne le joueur courant.
   
    Args:
        state (dict): État actuel du jeu.
   
    Returns:
        Joueur: Joueur courant.
    """
    joueurs = state["joueurs"]
    pass

def joueur_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications liées aux joueurs.
    """
    match action['type']:
        case 'INITIALIZE_PLAYERS':
            return initialize_players(state)
        case 'CHANGE_CURRENT_PLAYER':
            return change_current_player(state)
        case 'CAPTURE_PIECE':
            joueur = next(j for j in state["joueurs"] if j.id == action["joueur_id"])
            joueur.capturer_piece()
            return state
        case 'LOSE_PIECE':
            joueur = next(j for j in state["joueurs"] if j.id == action["joueur_id"])
            joueur.perdre_piece()
            return state
        case 'FINISH_GAME':
            for joueur in state["joueurs"]:
                joueur.conclure_partie()
            return state
        case 'PLAY_MOVE':
            joueur = next(j for j in state["joueurs"] if j.id == action["joueur_id"])
            coup = Coup(action["from_pos"], action["to_pos"], joueur.id, action["timestamp"])
            joueur.jouer_coup(coup)
            return state
        case _:
            return state