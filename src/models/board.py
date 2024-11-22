import logging
from typing import Dict, List,  Set

from actions.board_actions import BoardAction
from utils.const import Soldier

class Board:
    def __init__(self):
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
        

        self.soldiers: Dict[str, int] = {pos: Soldier.EMPTY for pos in self.battle_field.keys()}
        
        # Pions rouges (haut)
        for pos in ['a1', 'a3', 'a5', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'c5', 'd1', 'd2', 'd3', 'd4', 'd5']:
            self.soldiers[pos] = Soldier.RED
            
        # Pions bleus (bas)
        for pos in ['f1', 'f2', 'f3', 'f4', 'f5', 'g1', 'g2', 'g3', 'g4', 'g5', 'h2', 'h3', 'h4', 'i1', 'i3', 'i5']:
            self.soldiers[pos] = Soldier.BLUE

        self.logger = logging.getLogger(__name__)

    
       
        
    def get_valid_actions(self, soldier_value: Soldier) -> List[Dict]:

        valid_actions = []
        opponent = Soldier.BLUE if soldier_value == Soldier.RED else Soldier.RED
        
        # Trouver to_posutes les positions vides
        empty_positions = [
            pos for pos, occupant in self.soldiers.items() 
            if occupant == Soldier.EMPTY
        ]

        # Pour chaque position vide
        for empty_pos in empty_positions:
            for neighbor in self.battle_field[empty_pos]:
                current_piece = self.soldiers[neighbor]
                
                # Mouvement simple
                if current_piece == soldier_value:
                    valid_actions.append(BoardAction.move_soldier(
                        from_pos=neighbor,
                        to_pos=empty_pos,
                        soldier_value=soldier_value
                    ))
                # Capture possible
                elif current_piece == opponent:
                    # Vérifier les pièces qui peuvent capturer
                    capture_positions = [
                        pos for pos in self.battle_field[neighbor]
                        if self.soldiers[pos] == soldier_value
                    ]
                    
                    # Ajouter to_posutes les captures possibles
                    for from_pos_pos in capture_positions:
                        valid_actions.append(BoardAction.capture_soldier(
                            from_pos=from_pos_pos,
                            to_pos=empty_pos,
                            soldier_value=soldier_value,
                            captured_soldier=neighbor
                        ))

        return valid_actions

