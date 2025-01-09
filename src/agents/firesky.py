import random
from typing import Dict, List, Optional
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier
from src.actions.board_actions import BoardAction

class Agent(BaseAgent):
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        """
        Initialise l'agent stratégique.
        Args:
            soldier_value (Soldier): Couleur des soldats de l'agent (RED ou BLUE).
            data (Dict, optional): Données de configuration pour l'agent. Par défaut, None.
        """
        super().__init__(soldier_value, data)
        self.name = "TeamFiresky"
        self.safe_zones = []  # Zones sécurisées

    def choose_action(self, board) -> Dict:
        """
        Choisit la meilleure action basée sur l'état actuel du plateau.
        Privilégie les captures sûres et évite les déplacements risqués.

        Args:
            board (Board): Instance du plateau de jeu.

        Returns:
            Dict: Action choisie dans le format attendu par `BoardAction`.
        """
        # Récupérer les actions valides
        valid_actions = board.get_valid_actions()
        
        # Filtrer les actions de capture
        capture_actions = [action for action in valid_actions if action["type"] == "CAPTURE_SOLDIER"]
        
        # Actions sûres (déplacement ou capture sans risque)
        safe_actions = [action for action in valid_actions if self.is_action_safe(board, action)]
        
        # Captures sûres
        safe_capture_actions = [action for action in capture_actions if action in safe_actions]
        
        # Priorisation des captures sûres
        if safe_capture_actions:
            return safe_capture_actions[0]
        
        # Si aucune capture sûre, prioriser les mouvements sûrs
        if safe_actions:
            return safe_actions[0]
        
        # Si aucune action sûre n'est disponible, choisir une action valide au hasard
        return valid_actions[0] if valid_actions else None

    def is_action_safe(self, board, action: Dict) -> bool:
        """
        Vérifie si une action est sûre (n'expose pas le soldat à une capture immédiate).

        Args:
            board (Board): Instance du plateau de jeu.
            action (Dict): Action à évaluer.

        Returns:
            bool: True si l'action est sûre, False sinon.
        """
        from_pos = action["from_pos"]
        to_pos = action["to_pos"]
        soldier_value = action["soldier_value"]
        
        # Simuler le déplacement
        board.soldiers[from_pos] = Soldier.EMPTY
        board.soldiers[to_pos] = soldier_value
        
        # Vérifier les voisins de la position cible
        neighbors = board.get_neighbors(to_pos)
        opponent_soldier = self.get_opponent_soldier()
        enemy_neighbors = neighbors[opponent_soldier.name]
        
        # Restaurer l'état initial du plateau
        board.soldiers[to_pos] = Soldier.EMPTY
        board.soldiers[from_pos] = soldier_value
        
        # Vérifier si un voisin ennemi peut capturer le soldat après ce déplacement
        for enemy_pos in enemy_neighbors:
            potential_captures = board.get_valid_actions_for_position(enemy_pos)
            if any(cap_action["to_pos"] == to_pos for cap_action in potential_captures):
                return False
        
        return True

    def attract_opponent_to_safe_zone(self, board, action: Dict) -> bool:
        """
        Attire l'adversaire vers une zone sécurisée (leurre). Cette fonction peut simuler une fuite ou
        faire en sorte que l'adversaire se dirige vers une zone où l'IA peut le capturer.
        
        Args:
            board (Board): Instance du plateau de jeu.
            action (Dict): Action à évaluer.

        Returns:
            bool: True si l'action attire l'adversaire vers une zone sécurisée.
        """
        from_pos = action["from_pos"]
        to_pos = action["to_pos"]
        
        # Vérifier si la destination se trouve dans une zone sécurisée
        if to_pos in self.safe_zones:
            return True  # L'IA a attiré l'adversaire vers une zone sécurisée.
        
        return False

    def get_opponent_soldier(self) -> Soldier:
        """
        Retourne la valeur du soldat adverse.

        Returns:
            Soldier: RED si l'agent joue BLUE, sinon BLUE.
        """
        return Soldier.RED if self.soldier_value == Soldier.BLUE else Soldier.BLUE

    def define_safe_zones(self, board: Board) -> None:
        """
        Définir des zones sécurisées sur le plateau (zones proches des alliés ou avec couverture).
        
        Args:
            board (Board): Instance du plateau de jeu.
        """
        # Exemple de zones sécurisées proches des alliés
        safe_positions = []
        for position, soldier in board.soldiers.items():
            if soldier == self.soldier_value:  # Si c'est un soldat allié
                # Ajouter des positions adjacentes comme sécurisées
                neighbors = board.get_neighbors(position)
                safe_positions.extend(neighbors)
        
        self.safe_zones = list(set(safe_positions))  # Enlever les doublons
