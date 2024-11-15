from typing import Dict, List, Tuple, Set

class Board:
    def __init__(self):
        # Définir la structure du plateau comme un graphe
        # Chaque position est identifiée par ses coordonnées algébriques
        # et stocke ses connexions avec les autres positions
        self.board_graph: Dict[str, Set[str]] = {
            'a1' : ['a3', 'b2'],
            'a3' : ['a1', 'a5', 'b3'],
            'a5' : ['a3', 'b4'],
            
            'b2' : ['a1', 'c3', 'b3'],
            'b3' : ['a3', 'b2', 'b4', 'c3'],
            'b4' : ['a5', 'b3', 'c3'],
            
            'c1' : ['c2', 'd1', 'd2'],
            'c2' : ['c1', 'd2', 'c3'],
            'c3' : ['c2', 'b2', 'b3', 'b4', 'c4', 'd4', 'd3', 'd2'],
            'c4' : ['c3', 'c5', 'd4'],
            'c5' : ['c4', 'd5', 'd4'],
            
            'd1' : ['c1', 'd2', 'e1'],
            'd2' : ['d1', 'c1', 'c2', 'c3', 'd3', 'e3', 'e2', 'e1'],
            'd3' : ['d2', 'c3', 'd4', 'e3'],
            'd4' : ['d3', 'c3', 'c4', 'c5', 'd5', 'e5', 'e4', 'e3'],
            'd5' : ['d4', 'c5', 'e5'],
            
            'e1' : ['d1', 'd2', 'e2', 'f2', 'f1'],
            'e2' : ['e1', 'd2', 'e3', 'f2'],
            'e3' : ['e2', 'd2', 'd3', 'd4', 'e4', 'f4', 'f3', 'f2'],
            'e4' : ['e3', 'd4', 'e5', 'f4'],
            'e5' : ['e4', 'd4', 'd5', 'f5', 'f4'],
            
            'f1' : ['e1', 'f2', 'g1'],
            'f2' : ['f1', 'e1', 'e2', 'e3', 'f3', 'g3', 'g2', 'g1'],
            'f3' : ['f2', 'e3', 'f4', 'g3'],
            'f4' : ['f3', 'e3', 'e4', 'e5', 'f4', 'g5', 'g4', 'g3'],
            'f5' : ['f4', 'e5', 'g5'],
            
            'g1' : ['f1', 'f2', 'g2'],
            'g2' : ['g1', 'f2', 'g3'],
            'g3' : ['g2', 'f2', 'f3', 'f4', 'g4', 'h4', 'h3', 'h2'],
            'g4' : ['g3', 'f4', 'g5'],
            'g5' : ['g4', 'f4', 'f5'],
            
            'h2' : ['g3', 'h3', 'i1'],
            'h3' : ['h2', 'g3', 'h4', 'i3'],
            'h4' : ['h3', 'g3', 'i5'],
            
            'i1' : ['h2', 'i3'],
            'i3' : ['i1', 'h3', 'i5'],
            'i5' : ['i3', 'h4']
        }
        
        # Stocker l'état des pions dans un dictionnaire
        # 0 = vide, 1 = rouge, 2 = vert
        # self.pieces: Dict[Tuple[int, int], int] = {pos: 0 for pos in self.positions}
        
        # # Placer les pions initiaux
        # # Pions rouges (haut)
        # for pos in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]:
        #     self.pieces[pos] = 1
            
        # # Pions verts (bas)
        # for pos in [(3, 2), (4, 0), (4, 1), (4, 2), (5, 0), (5, 1), (5, 2), (3, 1)]:
        #     self.pieces[pos] = 2
    
    def get_all_node(self):
        return self.board_graph.keys()
    
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
    
    def get_valid_actions(self, player: int) -> List[Dict]:
        """
        Renvoie les actions valides pour un joueur donné.

        Args:
            
            player (int): Joueur actuel (1 = rouge, 2 = vert).

        Returns:
            list: Liste des actions valides.
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