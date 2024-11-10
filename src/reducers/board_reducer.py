from typing import Dict, Tuple
from models.board import GameBoard

def plateau_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications du plateau.
    """
    
    plateau = state['plateau']
    match action['type']:
        case 'MOVE_PIECE':
            from_pos = action['from_pos']
            to_pos = action['to_pos']
            if plateau.is_valid_move(from_pos, to_pos):
                plateau.move_piece(from_pos, to_pos)

            return {**state, 'plateau': plateau}
        
        case 'CAPTURE_PIECE':
            pos = action['pos']
            if plateau.pieces[pos] != 0:
                plateau.capture_piece(pos)
            return {**state, 'plateau': plateau}
        case _:
            return state