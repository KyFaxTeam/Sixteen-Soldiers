import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    """Agent IA avec une stratégie basique."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "JoLyCh"

    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action parmi les options valides selon la priorité suivante :
        1. Capture d'un soldat ennemi.
        2. Mouvement sûr (non capturable au tour suivant).
        3. Action aléatoire en dernier recours.
        """
        valid_actions = board.get_valid_actions()
        
        if not valid_actions:
            raise ValueError("Aucune action valide disponible, vérifiez l'état du jeu.")
        
        # Prioriser les captures
        capture_actions = [action for action in valid_actions if action.get("type") == "CAPTURE_SOLDIER"]
        if capture_actions:
            return random.choice(capture_actions)
        
        # Rechercher des actions sûres
        safe_actions = [action for action in valid_actions if self.is_safe(board, action)]
        if safe_actions:
            return random.choice(safe_actions)
        
        # Choisir une action aléatoire en dernier recours
        return random.choice(valid_actions)

    def is_safe(self, board: Board, action: Dict) -> bool:
        """
        Vérifie si une action de type MOVE_SOLDIER est sûre.
        Une action est sûre si elle ne conduit pas à une capture par l'adversaire.
        """
        if action["type"] != "MOVE_SOLDIER":
            return True  # Les autres types d'actions ne sont pas concernées par cette logique

        # Simuler le mouvement
        board.move_soldier(action)
        is_dangerous = any(
            adversary_action.get("type") == "CAPTURE_SOLDIER"
            for adversary_action in board.get_valid_actions()
        )
        # Annuler le mouvement simulé
        board.move_soldier({
            "type": "MOVE_SOLDIER",
            "soldier_value": action["soldier_value"],
            "from_pos": action["to_pos"],
            "to_pos": action["from_pos"]
        })
        return not is_dangerous