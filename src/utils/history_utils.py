from typing import Dict, List, Optional
from models.move import Move

def get_history(state: Dict) -> List[Dict]:
    """
    Get complete history of moves
    
    Args:
        state (Dict): Current state
    
    Returns:
        List[Dict]: List of all moves
    """
    return state.get("history", [])

def get_last_move(state: Dict) -> Optional[Move]:
    """
    Get the last move from history
    """
    history = get_history(state)
    if history:
        return Move.from_dict(history[-1])
    return None

def is_equals(move1: Dict, move2: Dict) -> bool:
    
    return move1 == move2

def get_move_at(state: Dict, index: int) -> Optional[Move]:
    """
    Get a specific move from history by index
    
    Args:
        state (Dict): Current state
        index (int): Index of the move to retrieve
    
    Returns:
        Optional[Move]: Move at specified index or None if invalid index
    """
    history = get_history(state)
    if 0 <= index < len(history):
        return Move.from_dict(history[index])
    return None

def get_move_count(state: Dict) -> int:
    """
    Get total number of moves in history
    
    Args:
        state (Dict): Current state
    
    Returns:
        int: Number of moves
    """
    return len(get_history(state))


def get_move_player_count(state: Dict, player_id: int) -> int:
    """
    Get total number of moves in history for a specific player
    
    Args:
        state (Dict): Current state
        player_id (int): ID of the player to count moves for

    Returns:
        int: Number of moves made by the specified player
    """
    history = get_history(state)
    return sum(1 for move_dict in history if Move.from_dict(move_dict).player_id == player_id)


def can_undo(state: Dict) -> bool:
    """
    Check if undo operation is possible
    
    Args:
        state (Dict): Current state
    
    Returns:
        bool: True if there are moves that can be undone
    """
    return bool(get_history(state))

def can_redo(state: Dict) -> bool:
    """
    Check if redo operation is possible
    
    Args:
        state (Dict): Current state
    
    Returns:
        bool: True if there are moves that can be redone
    """
    return bool(state.get("redo_stack", []))

