
import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    """IA optimisée avec des stratégies d'attaque et de défense pour le jeu de stratégie"""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "blacknight01"  # Nom de l'IA ou de l'équipe

    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action parmi les actions valides disponibles en fonction de l'état du plateau.
        Args:
            board: L'état actuel du plateau
        Returns:
            L'action choisie sous forme de dictionnaire
        """
        valid_actions = board.get_valid_actions()  # Liste des actions valides
        best_move = self.choose_best_move(valid_actions, board)
        return best_move

    def choose_best_move(self, valid_actions: List[Dict], board: Board) -> Dict:
        """
        Choisit le meilleur mouvement parmi ceux valides en fonction de l'évaluation stratégique.
        Args:
            valid_actions: Liste des mouvements valides
            board: Plateau actuel du jeu
        Returns:
            Le meilleur mouvement sous forme de dictionnaire
        """
        best_move = None
        best_score = -float("inf")  # Score initial très bas pour la maximisation

        for move in valid_actions:
            score = self.evaluate_move(move, board)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def evaluate_move(self, move: Dict, board: Board) -> int:
        """
        Évalue un mouvement donné en fonction de critères stratégiques.
        Args:
            move: Mouvement à évaluer
            board: Plateau actuel du jeu
        Returns:
            Le score d'évaluation de ce mouvement
        """
        from_pos = move['from_pos']
        to_pos = move['to_pos']
        soldier_value = move['soldier_value']

        # Critères d'évaluation : chaque condition rajoute ou enlève des points
        score = 0

        # 1. Vérification de la capture
        if self.does_capture(move, board):
            score += 10  # Bonus pour capture

        # 2. Anticipation des captures successives
        if self.can_continue_capture(move, board):
            score += 20  # Bonus pour captures successives

        # 3. Sécurité du mouvement (évite les captures ennemies)
        if self.is_safe_move(move, board):
            score += 5  # Bonus de sécurité

        # 4. Proximité avec les pions ennemis (éloigner si trop proche)
        if self.is_too_close_to_enemy(move, board):
            score -= 3  # Pénalité pour proximité dangereuse

        # 5. Bloquer un ennemi
        if self.can_block_enemy(move, board):
            score += 8  # Bonus pour bloquer un ennemi

        # 6. Contrôle des cases centrales
        if self.is_center_position(to_pos):
            score += 6  # Bonus pour contrôler les cases centrales

        # 7. Protection des pièces stratégiques (protéger un allié)
        if self.can_protect_allied_piece(move, board):
            score += 4  # Bonus pour protéger un allié

        return score

    def does_capture(self, move: Dict, board: Board) -> bool:
        """
        Vérifie si un mouvement est une capture.
        Args:
            move: Mouvement à vérifier
            board: Plateau actuel du jeu
        Returns:
            True si c'est une capture, False sinon
        """
        from_pos = move['from_pos']
        to_pos = move['to_pos']
        soldier_value = move['soldier_value']

        # La capture se produit si l'ennemi est à côté et que la case est vide
        neighbors = board.get_neighbors(from_pos)
        captured_positions = set(neighbors[Soldier.RED.name] if soldier_value == Soldier.BLUE else neighbors[Soldier.BLUE.name])
        return to_pos in captured_positions

    def can_continue_capture(self, move: Dict, board: Board) -> bool:
        """
        Vérifie si un mouvement permet une capture successive (capture continue).
        Args:
            move: Mouvement à vérifier
            board: Plateau actuel du jeu
        Returns:
            True si une capture successive est possible
        """
        from_pos = move['from_pos']
        to_pos = move['to_pos']
        soldier_value = move['soldier_value']

        # Cherche à savoir si le mouvement mène à une capture successive
        return board.check_multi_capture(soldier_value, to_pos)

    def is_safe_move(self, move: Dict, board: Board) -> bool:
        """
        Vérifie si un mouvement place un pion dans une position sûre.
        Args:
            move: Mouvement à vérifier
            board: Plateau actuel du jeu
        Returns:
            True si le mouvement est sûr
        """
        from_pos = move['from_pos']
        to_pos = move['to_pos']

        # Un mouvement est considéré comme sûr si aucune case voisine n'est occupée par un ennemi
        neighbors = board.get_neighbors(to_pos)
        return all(board.get_soldier_value(neighbor) != Soldier.RED for neighbor in neighbors[Soldier.RED.name])

    def is_too_close_to_enemy(self, move: Dict, board: Board) -> bool:
        """
        Vérifie si le mouvement place un pion trop près d'un ennemi.
        Args:
            move: Mouvement à vérifier
            board: Plateau actuel du jeu
        Returns:
            True si trop proche d'un ennemi
        """
        from_pos = move['from_pos']
        to_pos = move['to_pos']

        # Si une case voisine appartient à l'adversaire, le mouvement est trop risqué
        neighbors = board.get_neighbors(to_pos)
        return any(board.get_soldier_value(neighbor) == Soldier.RED for neighbor in neighbors[Soldier.RED.name])

    def can_block_enemy(self, move: Dict, board: Board) -> bool:
        """
        Vérifie si le mouvement permet de bloquer un pion adverse.
        Args:
            move: Mouvement à vérifier
            board: Plateau actuel du jeu
        Returns:
            True si le mouvement bloque un pion ennemi
        """
        from_pos = move['from_pos']
        to_pos = move['to_pos']

        # Si un mouvement met un ennemi dans une position sans issue, il bloque cet ennemi
        return False  # Cette logique peut être affinée

    def is_center_position(self, position: str) -> bool:
        """
        Vérifie si une position est centrale sur le plateau.
        Args:
            position: Position à vérifier
        Returns:
            True si la position est centrale
        """
        center_positions = ['d3', 'd4', 'e3', 'e4', 'c3', 'c4']
        return position in center_positions

    def can_protect_allied_piece(self, move: Dict, board: Board) -> bool:
        """
        Vérifie si le mouvement protège une pièce alliée.
        Args:
            move: Mouvement à vérifier
            board: Plateau actuel du jeu
        Returns:
            True si le mouvement protège un allié
        """
        # Cette logique peut être affinée en fonction des stratégies de protection des pièces alliées
        return False  # Ajouter ici la logique pour détecter une protection stratégique

