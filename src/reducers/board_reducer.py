from typing import Dict
from models.board import Board
from utils.const import Soldier

def move_soldier(state: Dict, action: Dict) -> Dict:
     
    new_state = state.copy()
   
    new_state['board'].soldiers[action['from_pos']] = Soldier.EMPTY
    new_state['board'].soldiers[action['to_pos']] = action['soldier_value']

    return new_state


def capture_soldier(state:Dict, action:Dict ) -> Dict:
    
    new_state = state.copy()
    
    new_state['board'].soldiers[action['from_pos']] = Soldier.EMPTY
    new_state['board'].soldiers[action['to_pos']] = action['soldier_value']
    new_state['board'].soldiers[action['captured_soldier']] = Soldier.EMPTY
    return new_state

    

def board_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications du board.
    """
    
    match action['type']:
        case 'MOVE_SOLDIER':
            new_state = move_soldier(state, action)
            return new_state 
        case 'CAPTURE_SOLDIER':
            new_state = capture_soldier(state, action)
            return new_state
        case _:
            return state




