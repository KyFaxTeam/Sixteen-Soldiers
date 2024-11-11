from typing import Dict
from models.board import Board
from models.time_manager import TimeManager

def initialize_game(state: Dict) -> Dict:
    """Initialize the game state"""
    # Ensure we have a valid state to work with
    if state is None:
        state = {}
    
    new_state = state.copy()
    new_state.update({
        "board": Board(),
        "time_manager": TimeManager(),
        "game_over": False,
        "current_player_index": 0,
        "winner": None,
        "players": new_state.get("players", [])  # Preserve existing players if any
    })
    return new_state

def change_current_player(state: Dict) -> Dict:
    """Switch to next player"""
    new_state = state.copy()
    new_state["current_player_index"] = (state["current_player_index"] + 1) % 2
    return new_state

def end_game(state: Dict, winner_id: str) -> Dict:
    """End the game and set winner"""
    new_state = state.copy()
    new_state["game_over"] = True
    new_state["winner"] = winner_id
    return new_state

def game_reducer(state: Dict, action: Dict) -> Dict:
    """Main game state reducer"""
    # Ensure we have a valid state
    if state is None:
        state = {}
        
    match action["type"]:
        case "INITIALIZE_GAME":
            return initialize_game(state)
        case "CHANGE_CURRENT_PLAYER":
            return change_current_player(state)
        case "END_GAME":
            return end_game(state, action.get("winner_id"))
        case _:
            return state
