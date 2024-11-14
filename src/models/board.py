from typing import Dict, List, Tuple, Set
from utils.const import PLAYER_CONFIG

class Board:
    def __init__(self):
        # Définir la structure du plateau comme un graphe
        # Chaque position est identifiée par ses coordonnées (x, y)
        # et stocke ses connexions avec les autres positions
        self.positions: Dict[Tuple[int, int], Set[Tuple[int, int]]] = {
            # Triangle supérieur
            (0, 0): {(0, 1), (1, 0), (1, 1)},
            (0, 1): {(0, 0), (0, 2), (1, 1)},
            (0, 2): {(0, 1), (1, 2), (1, 1)},
            (1, 0): {(0, 0), (2, 0), (1, 1)},
            (1, 1): {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)},
            (1, 2): {(0, 2), (2, 2), (1, 1)},
            (2, 0): {(1, 0), (3, 0), (2, 1), (1, 1)},
            (2, 1): {(2, 0), (2, 2), (3, 1), (1, 1)},
            (2, 2): {(1, 2), (3, 2), (2, 1), (1, 1)},
            
            # Zone centrale
            (3, 0): {(2, 0), (4, 0), (3, 1)},
            (3, 1): {(3, 0), (3, 2), (2, 1), (4, 1)},
            (3, 2): {(2, 2), (4, 2), (3, 1)},
            
            # Triangle inférieur
            (4, 0): {(3, 0), (5, 0), (4, 1), (5, 1)},
            (4, 1): {(4, 0), (4, 2), (3, 1), (5, 1)},
            (4, 2): {(3, 2), (5, 2), (4, 1), (5, 1)},
            (5, 0): {(4, 0), (5, 1)},
            (5, 1): {(5, 0), (5, 2), (4, 0), (4, 1), (4, 2)},
            (5, 2): {(4, 2), (5, 1)}
        }
        
        # Stocker l'état des pions dans un dictionnaire
        # 0 = vide, 1 = joueur 1, -1 = joueur 2
        self.pieces: Dict[Tuple[int, int], int] = {pos: PLAYER_CONFIG["EMPTY"] for pos in self.positions}
        
        # Placer les pions initiaux
        # Pions du joueur 1 (haut)
        for pos in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]:
            self.pieces[pos] = PLAYER_CONFIG["PLAYER_1"]
            
        # Pions du joueur 2 (bas)
        for pos in [(3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2), (3, 1)]:
            self.pieces[pos] = PLAYER_CONFIG["PLAYER_2"]
    
    

    def get_piece(self, pos: Tuple[int, int]) -> int:
        pass

    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        pass

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        pass

    
    def evaluate_position(self) -> float:
        pass

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """
        Déplace un pion sur le plateau.
    
        Args:
            
            from_pos (tuple): Position de départ du pion (x, y).
            to_pos (tuple): Position d'arrivée du pion (x, y).
    
        Returns:
            dict: État mis à jour avec le pion déplacé.
        """
   
        pass

    def capture_piece(self, pos: Tuple[int, int]) -> bool:
        """
        Capture un pion sur le plateau.
    
        Args:
            
            pos (tuple): Position du pion à capturer (x, y).
    
        Returns:
            dict: État mis à jour avec le pion capturé.
        """
        pass

    def get_available_moves(self, player: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """                             
        Renvoie les mouvements valides pour un joueur donné.

        Args:
            
            player (int): Joueur actuel (1 = rouge, 2 = vert).

        Returns:

        """
        pass
    
    def get_valid_actions(self, player_id: int) -> List[Dict]:
        """
        Renvoie les actions valides pour un joueur donné.

        Args:
            player_id (int): ID du joueur (1 ou -1)
        """
        pass


    def to_dict(self):
        """Convert Board object to dictionary"""
        return {
            "positions": self.positions,
            "pieces": self.pieces,
            # Add other necessary fields
        }
    
    def from_dict(cls, data: dict):
        """Create Board object from dictionary"""
        board = cls()
        board.positions = data["positions"]
        board.pieces = data["pieces"]
        # Initialize other fields
        return board
