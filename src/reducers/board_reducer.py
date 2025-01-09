from typing import Dict
from src.models.board import Board
from src.utils.const import Soldier


def board_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications du board.
    """
    
    match action['type']:
        case 'MOVE_SOLDIER':
            new_state = state.copy()
            new_state['board'].move_soldier(action)
    
            return new_state 
        case 'CAPTURE_SOLDIER':
            new_state = state.copy()
            new_state['board'].capture_soldier(action)
    
            return new_state
        case _:
            return state




