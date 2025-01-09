# history_reducer.py
from typing import  Dict, Optional
from src.actions.history_actions import *
from src.utils.history_utils import *
from src.models.move import Move

def history_reducer(state: Dict, action: Optional[Dict] = None) -> Dict:
    """
    Main reducer for managing game history
    
    Args:
        state (Dict): Current state containing history
        action (Optional[Dict]): Action to be processed
    
    Returns:
        Dict: Updated state
    """

    match action["type"]:
        case "ADD_MOVE_TO_HISTORY":
            return add_move(state, action["payload"])
        case "UNDO_LAST_MOVE":
            return undo_move(state)
        case "REDO_MOVE":
            return redo_move(state)
        case "CLEAR_HISTORY":
            return clear_history(state)
        case _:
            return state

def add_move(state: Dict, payload: Dict) -> Dict:

    last_move = get_last_move(state)

    if last_move and last_move.is_valid_player(payload):
        # Update existing move for multiple capture
        last_move.pos.append(payload["to_pos"])
        last_move.timestamp.append(payload["timestamp"])
        last_move.captured_soldier.append(payload['captured_soldier'])
        last_move.capture_multiple = True
        state["history"][-1] = last_move.to_dict()
    else:
        # Create new move
        move = Move(
            pos=[payload["from_pos"], payload["to_pos"]],
            soldier_value=payload["soldier_value"],
            captured_soldier=[payload.get("captured_soldier")] if payload.get("captured_soldier") else None,
            timestamp=[payload["timestamp"]]
        )
        state["history"].append(move.to_dict())
    
    return state

def undo_move(state: Dict) -> Dict:
    """
    Undo the last move in the history
    
    Args:
        state (Dict): Current state
    
    Returns:
        Dict: Updated state with last move removed
    """
    # state = deepcopy(state)
    if state["history"]:
        last_move = state["history"].pop()
        if "redo_stack" not in state:
            state["redo_stack"] = []
        state["redo_stack"].append(last_move)
    return state

def redo_move(state: Dict) -> Dict:
    """
    Redo the last undone move
    
    Args:
        state (Dict): Current state
    
    Returns:
        Dict: Updated state with redone move
    """
    # state = deepcopy(state)
    if state.get("redo_stack") and state["redo_stack"]:
        move = state["redo_stack"].pop()
        state["history"].append(move)
    return state

def clear_history(state: Dict) -> Dict:
    """
    Clear all moves from history
    
    Args:
        state (Dict): Current state
    
    Returns:
        Dict: Empty history state
    """
    state['history'] = []
    state['redo_stack'] :  [] # type: ignore
    return state


