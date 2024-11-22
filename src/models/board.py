import logging
from typing import Dict, List, Tuple, Set

from actions.board_actions import BoardAction
from utils.const import PLAYER_CONFIG

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
        # -1 = vide, 0 = rouge, 1 = bleu
        self.soldiers: Dict[str, int] = {pos: PLAYER_CONFIG["EMPTY"] for pos in self.battle_field.keys()}
        
        # Placer les pions initiaux
        # Pions rouges (haut)
        for pos in ['a1', 'a3', 'a5', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'c5', 'd1', 'd2', 'd3', 'd4', 'd5']:
            self.soldiers[pos] = PLAYER_CONFIG["PLAYER_1"]
            
        # Pions bleus (bas)
        for pos in ['f1', 'f2', 'f3', 'f4', 'f5', 'g1', 'g2', 'g3', 'g4', 'g5', 'h2', 'h3', 'h4', 'i1', 'i3', 'i5']:
            self.soldiers[pos] = PLAYER_CONFIG["PLAYER_2"]

        self.logger = logging.getLogger(__name__)
    
    def get_piece(self, pos: Tuple[int, int]) -> int:
        pass

    def is_valid_move(self, action) -> bool:
        # Ignore validation for non-move actions
        if action['type'] not in ['MOVE_SOLDIER', 'CAPTURE_SOLDIER']:
            return True

        # Validate that 'action' is a dictionary with required keys
        if not isinstance(action, dict):
            self.logger.error("Invalid action format")
            return False
            
        required_keys = ['type', 'from', 'to', 'soldier']
        for key in required_keys:
            if key not in action:
                self.logger.error(f"Action missing key: {key}")
                return False

        # Validate action type
        if action['type'] not in ['MOVE_SOLDIER', 'CAPTURE_SOLDIER']:
            self.logger.error(f"Invalid action type: {action['type']}")
            return False

        # Validate positions exist on board
        if action['from'] not in self.soldiers or action['to'] not in self.soldiers:
            self.logger.error("Invalid positions in action")
            return False

        # Validate soldier ownership
        if self.soldiers[action['from']] != action['soldier']:
            self.logger.error("Soldier not present at the from position")
            return False

        # Validate destination is empty
        if self.soldiers[action['to']] != PLAYER_CONFIG["EMPTY"]:
            self.logger.error("Destination position is not empty")
            return False

        return True

    def evaluate_position(self) -> float:
        pass
    
    def make_move(self, action):
        try:
            self.logger.info(f"Executing action: {action}")
            if not self.is_valid_move(action):
                raise ValueError("Invalid move attempted")

            match action['type']:
                case 'MOVE_SOLDIER':
                    self.__move_soldier(from_=action['from'], to=action['to'], soldier=action['soldier'])
                case 'CAPTURE_SOLDIER':
                    self.__capture_soldier(from_=action['from'], to=action['to'], captured_soldier=action['captured_soldier'])
        except Exception as e:
            self.logger.error(f"Error executing move: {e}")
            # Optionally, re-raise or handle the exception as needed

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
            player (int): Joueur actuel (0 = rouge, 1 = bleu).

        Returns:
            list: Liste des actions valides.
        """
        
        assert player == PLAYER_CONFIG["PLAYER_1"] or player == PLAYER_CONFIG["PLAYER_2"], "Invalid Player"

        valid_actions = []
        
        # Trouver toutes les positions vides
        empty_positions = [pos for pos, occupant in self.soldiers.items() if occupant == PLAYER_CONFIG["EMPTY"]]

        for empty_pos in empty_positions:
            # Trouver les voisins de la position vide
            neighbors = self.battle_field[empty_pos]
            
            for neighbor in neighbors:
                if self.soldiers[neighbor] == player:
                    # Le joueur peut déplacer un soldat vers une cellule vide
                    valid_actions.append(BoardAction.move_soldier(
                        from_=neighbor, 
                        to=empty_pos,
                        soldier=player
                    ))
                # L'adversaire est maintenant l'autre index (0 ou 1)
                elif self.soldiers[neighbor] == (0 if player == 1 else 1):
                    # Vérifier si un soldat peut capturer un ennemi
                    for next_neighbor in self.battle_field[neighbor]:
                        if self.soldiers[next_neighbor] == player:
                            valid_actions.append(BoardAction.capture_soldier(
                                captured_soldier=neighbor,
                                from_=next_neighbor,
                                to=empty_pos,
                                soldier=player
                            ))
        return valid_actions

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