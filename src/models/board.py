from typing import Dict, List, Tuple, Set

from actions.board_actions import BoardAction

class Board:
    def __init__(self):
        # Définir la structure du plateau comme un graphe
        # Chaque position est identifiée par ses coordonnées algébriques
        # et stocke ses connexions avec les autres positions
        self.battle_field: Dict[str, Set[str]] = {
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
        self.soldiers: Dict[str, int] = {pos: 0 for pos in self.battle_field.keys()}
        
        # # Placer les pions initiaux
        # # Pions rouges (haut)
        for pos in ['a1', 'a3', 'a5', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'c5', 'd1', 'd2', 'd3', 'd4', 'd5']:
            self.soldiers[pos] = 1
        #     self.pieces[pos] = 1
            
        # # Pions bleus (bas)
        for pos in ['f1', 'f2', 'f3', 'f4', 'f5', 'g1', 'g2', 'g3', 'g4', 'g5', 'h2', 'h3', 'h4', 'i1', 'i3', 'i5']:
            self.soldiers[pos] = -1
    
    def get_piece(self, pos: Tuple[int, int]) -> int:
        pass

    def is_valid_move(self, action) -> bool:
        
        # TODO : assertion
        # TODO : 
        if action['type'] == "MOVE_SOLDIER":
            ...
        
        if self.soldiers[action['from']] != action['soldier']:
            return False
        if self.soldiers[action['to']] != 0:
            return False
        
        return True

    def evaluate_position(self) -> float:
        pass
    
    def make_move(self, action):
        match action['type']:
            case 'MOVE_SOLDIER':
                if self.is_valid_move(action=action):
                    self.__move_soldier(from_=action['from'], to=action['to'], soldier=action['soldier'])
            
            case 'CAPTURE_SOLDIER':
                if self.is_valid_move(action=action):
                    self.__capture_soldier(from_=action['from'], to=action['to'], captured_soldier=action['captured_soldier'])

    def __move_soldier(self, from_: str, to: str, soldier: int):
        """
        Déplace un pion sur le plateau.
    
        Args:
            
            from_pos (tuple): Position de départ du pion (x, y).
            to_pos (tuple): Position d'arrivée du pion (x, y).
    
        Returns:
            dict: État mis à jour avec le pion déplacé.
        """
        self.soldiers[from_] = 0
        self.soldiers[to] = soldier
        

    def __capture_soldier(self, from_: str, to:str, captured_soldier=str) -> bool:
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
        
        assert player == -1 or player == 1 , "Invalid Player"

        valid_positions = []
        
        empty_positions = [node  for node, player in self.soldiers.items() if player == 0 ]

        for empty_position in empty_positions:
            empty_position_neighbors = self.battle_field[empty_position]
            
            for neighbor in empty_position_neighbors :
                if self.soldiers[neighbor] == player:
                    # Le joeur peut accéder à une cellule vide
                    valid_positions.append(BoardAction.move_soldier(
                        from_ = neighbor, 
                        to = empty_position,
                        soldier=player
                        ))
                    
                if self.soldiers[neighbor] == player * -1:
                    # On vérifie si un soldat à du vide derrière un ennemi
                    for neighbor_neighbor in self.battle_field[neighbor]:
                        if self.soldiers[neighbor_neighbor] ==  player :
                            valid_positions.append(BoardAction.capture_soldier(
                                captured_soldier = neighbor,
                                from_ = neighbor_neighbor,
                                to = empty_position,
                                soldier=player
                            ))
        return valid_positions


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