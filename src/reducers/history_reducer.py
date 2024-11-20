# history_reducer.py
from typing import List, Dict, Optional
from copy import deepcopy
from ..actions.history_actions import *
from ..utils.history_utils import *
from ..models.move import Move

def history_reducer(state: Dict, action: Optional[Dict] = None) -> Dict:
    """
    Main reducer for managing game history
    
    Args:
        state (Dict): Current state containing history
        action (Optional[Dict]): Action to be processed
    
    Returns:
        Dict: Updated state
    """
    if action is None:
        return state

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
    """
    Add a new move to the history or update the last move in case of multiple capture
    
    Args:
        state (Dict): Current state
        payload (Dict): Move information including positions, player, and capture details
    
    Returns:
        Dict: Updated state with new move
    """
    last_move = get_last_move(state)

    if last_move and last_move.is_valid_player(payload):
        # print("/////////////////////// Je ne suis jamais venu ici")
        # Update existing move for multiple capture
        last_move.pos.append(payload["to_pos"])
        last_move.timestamp.append(payload["timestamp"])
        last_move.capture_multiple = True
        state["history"][-1] = last_move.to_dict()
    else:
        # print("***************************** I'm here : here")
        # Create new move
        move = Move(
            # id=len(state["history"]),
            pos=[payload["from_pos"], payload["to_pos"]],
            player_id=payload["player_id"],
            piece_capturee=payload.get("piece_capturee"),
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


