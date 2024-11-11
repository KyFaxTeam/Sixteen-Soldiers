from typing import Dict, Tuple
from models.board import Board

def board_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications du board.
    """
    # Ensure we have a valid state
    if state is None or 'board' not in state:
        return state if state else {}
    
    board = state['board']
    if board is None:
        board = Board()
        state = {**state, 'board': board}
    
    match action['type']:
        case 'MOVE_PIECE':
            from_pos = action['from_pos']
            to_pos = action['to_pos']
            if board.is_valid_move(from_pos, to_pos):
                board.move_piece(from_pos, to_pos)

            return {**state, 'board': board}
        
        case 'CAPTURE_PIECE':
            pos = action['pos']
            if board.pieces[pos] != 0:
                board.capture_piece(pos)
            return {**state, 'board': board}
        case _:
            return state