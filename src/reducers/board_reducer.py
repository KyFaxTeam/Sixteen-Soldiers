from typing import Dict, Tuple
from models.board import Board

class BoardReducer:
    
    @staticmethod
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
        
        board.make_move(action=action)
        return {**state, 'board': board}
        