import logging
from typing import Dict
from models.board import Board
from models.time_manager import TimeManager
from utils.const import PLAYER_CONFIG

logger = logging.getLogger(__name__)

def initialize_game(state: Dict) -> Dict:
    logger.info("Initializing game state")
    
    # Find PLAYER_1 index
    player_1_index = next(
        i for i, player in enumerate(state["players"]) 
        if player.id == PLAYER_CONFIG["PLAYER_1"]
    )
    
    # Reset all values to initial state
    new_state = state.copy()
    new_state.update({
        "board": Board(),  # Board constructor handles piece placement
        "time_manager": TimeManager(),
        "game_over": False,
        "is_game_paused": False,
        "current_player_index": player_1_index,
        "winner": {},
        "history": []
    })
    
    return new_state

def change_current_player(state: Dict) -> Dict:
    new_state = state.copy()
    new_state["current_player_index"] = (state["current_player_index"] + 1) % 2
    logger.info(f"Changed current player to index {new_state['current_player_index']}")
    return new_state

def end_game(state: Dict, winner_id: str) -> Dict:
    logger.info(f"Ending game. Winner ID: {winner_id}")
    new_state = state.copy()
    new_state["game_over"] = True
    # Find the winner player object
    winner_player = next(
        (player for player in state.get("players", []) if player.id == winner_id),
        None
    )
    # Store the winner player data in the state
    if winner_player:
        new_state["winner"] = {
            "id": winner_player.id,
            "profile_img": winner_player.profile_img,  # Ensure this attribute exists
            "team_pseudo": winner_player.team_pseudo,  # Ensure this attribute exists
            "agent_name": winner_player.agent_name,    # Ensure this attribute exists
            # Add any other necessary attributes
        }
    else:
        new_state["winner"] = {}
    return new_state

def pause_game(state: Dict) -> Dict:
    """Pause the game."""
    new_state = state.copy()
    new_state['is_game_paused'] = True
    logger.info("Game state: Paused")
    return new_state

def resume_game(state: Dict) -> Dict:
    """Resume the game."""
    new_state = state.copy()
    new_state['is_game_paused'] = False
    logger.info("Game state: Resumed")
    return new_state

def game_reducer(state: Dict, action: Dict) -> Dict:
    logger.debug(f"Reducer received action: {action}")
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
        case "PAUSE_GAME":
            return pause_game(state)
        case "RESUME_GAME":
            return resume_game(state)
        case "PASS_TURN":
            logger.info(f"Player {action['player_id']} passes turn.")
            return change_current_player(state)
        case _:
            return state
