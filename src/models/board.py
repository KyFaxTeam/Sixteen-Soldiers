import logging
from typing import Dict, List,  Set

from src.actions.board_actions import BoardAction
from src.utils.board_utils import BoardUtils
from src.utils.const import Soldier


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
        
        # Red soldiers (top)
        for pos in ['a1', 'a3', 'a5', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'c5', 'd1', 'd2', 'd3', 'd4', 'd5']:
            self.soldiers[pos] = Soldier.RED
            
        # Blue soldiers (bottom)
        for pos in ['f1', 'f2', 'f3', 'f4', 'f5', 'g1', 'g2', 'g3', 'g4', 'g5', 'h2', 'h3', 'h4', 'i1', 'i3', 'i5']:
            self.soldiers[pos] = Soldier.BLUE

        self.last_action = None

        self.is_multiple_capture = False

        # self.logger = logging.getLogger(__name__)


    
    def get_neighbors(self, position: str) -> Dict[str, List[str]]:
        """Returns neighboring positions of a given position, classified by value."""
        neighbors = self.battle_field.get(position, [])
        result = {
            Soldier.RED.name: [],
            Soldier.BLUE.name: [],
            Soldier.EMPTY.name: []
        }
        for neighbor in neighbors:
            soldier = self.soldiers.get(neighbor, Soldier.EMPTY)
            result[soldier.name].append(neighbor)
        return result
    
    def get_empty_positions(self) -> List[str]:
        """
        Returns a list of empty positions
        """
        return [pos for pos, soldier in self.soldiers.items() if soldier == Soldier.EMPTY]
    

    def get_soldier_positions(self, soldier_value: Soldier) -> List[str]:
        """Returns positions occupied by soldiers of a specific value."""
        return [pos for pos, value in self.soldiers.items() if value == soldier_value]


    def get_soldier_value(self, position: str) -> Soldier:
        """Returns the soldier value at a given position."""
        return self.soldiers.get(position, Soldier.EMPTY)

    
    def count_soldiers(self, soldier_value: Soldier) -> int:
        """Count the number of pieces for the given soldier value."""
        return sum(1 for s in self.soldiers.values() if s == soldier_value)

    def move_soldier(self, action: Dict):
        """Move a soldier based on the action dictionary."""
        from_pos = action['from_pos']
        to_pos = action['to_pos']
        soldier_value = action['soldier_value']
        self.soldiers[from_pos] = Soldier.EMPTY
        self.soldiers[to_pos] = soldier_value
        
        # Store the last move
        self.last_action = action

    def capture_soldier(self, action: Dict):
        """Capture a soldier based on the action dictionary."""
        from_pos = action['from_pos']
        to_pos = action['to_pos']
        captured_pos = action['captured_soldier']
        soldier_value = action['soldier_value']
        self.soldiers[from_pos] = Soldier.EMPTY
        self.soldiers[to_pos] = soldier_value
        self.soldiers[captured_pos] = Soldier.EMPTY
        
        # Store the last move
        self.last_action = action

        self.is_multiple_capture = self.check_multi_capture(soldier_value, to_pos)

    def get_last_action(self) -> Dict:
        """
        Returns the last move made
        """
        return getattr(self, 'last_action', None)

    def check_multi_capture(self, soldier_value: Soldier, current_position: str) -> bool:
        """Check if a multi-capture is possible."""
        return BoardUtils.find_continued_captures(battle_field= self.battle_field, soldiers= self.soldiers, soldier_value=soldier_value, last_position=current_position, just_know=True)
    
    def get_valid_actions(self) -> List[Dict]:

        if self.last_action is None:
            
            return BoardUtils.get_actions_soldier(self.battle_field, self.soldiers, soldier_value=Soldier.RED, last_position=None)
        
        last_soldier = self.last_action.get('soldier_value') if self.last_action else None
        

        if self.last_action['type'] == 'CAPTURE_SOLDIER' and self.is_multiple_capture:
            return BoardUtils.find_continued_captures(self.battle_field, self.soldiers, last_soldier, self.last_action['to_pos'])
        
        next_soldier = Soldier.RED if last_soldier == Soldier.BLUE else Soldier.BLUE
        return BoardUtils.get_actions_soldier(self.battle_field, self.soldiers, next_soldier, last_position=None)
             

    def get_valid_actions_for_position(self, position: str) -> List[Dict]:
        """
        Returns valid actions for a specific position
        """
        soldier_value = self.soldiers[position]
        if soldier_value == Soldier.EMPTY:
            return []
        
        return [action for action in self.get_valid_actions() 
                if action['from_pos'] == position]

    def is_valid_move(self, from_pos: str, to_pos: str, soldier_value: Soldier) -> bool:
        """
        Checks if a specific move is valid
        """
        valid_actions = self.get_valid_actions()
        return any(
            action['from_pos'] == from_pos and 
            action['to_pos'] == to_pos 
            for action in valid_actions
        )
    
    def is_game_over(self):
        """Check if the game is over (one player has no pieces left)."""
        red_count = self.count_soldiers(Soldier.RED)
        blue_count = self.count_soldiers(Soldier.BLUE)
        if red_count == 0 :
            return  Soldier.BLUE
        if blue_count == 0 :
            return  Soldier.RED
        
        return None
