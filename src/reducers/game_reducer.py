import logging
from typing import Dict
from models.board import Board
from models.time_manager import TimeManager
from utils.const import PLAYER_CONFIG, INITIAL_VALUES

logger = logging.getLogger(__name__)

def initialize_game(state: Dict) -> Dict:
    logger.info("Initializing game state")
    
    # Find PLAYER_1 index
    player_1 = PLAYER_CONFIG["PLAYER_1"]
    
    # Create and initialize TimeManager
    time_manager = TimeManager()
    time_manager.set_time_limits({
        PLAYER_CONFIG["PLAYER_1"]: INITIAL_VALUES["TIMER"],
        PLAYER_CONFIG["PLAYER_2"]: INITIAL_VALUES["TIMER"]
    })
    
    # Reset all values to initial state
    new_state = state.copy()
    new_state.update({
        "board": Board(),
        "time_manager": time_manager,
        "is_game_over": False,
        "is_game_paused": False,
        "current_player": player_1,
        "winner": {},
        "history": []
    })
    
    return new_state

def change_current_player(state: Dict) -> Dict:
    new_state = state.copy()
    new_state["current_player"] = (state["current_player"] + 1) % 2  # Renommé de current_player_index à current_player
    logger.info(f"Changed current player to index {new_state['current_player']}")
    return new_state

def end_game(state: Dict, winner_id: str) -> Dict:
    logger.info(f"Ending game. Winner ID: {winner_id}")
    new_state = state.copy()
    new_state["is_game_over"] = True

    # Find the winner agent ID based on player_id
    winner_agent_id = next(
        (agent_id for agent_id, agent in state.get("agents", {}).items()
         if agent["player_id"] == winner_id),
        None
    )

    new_state["winner"] = winner_agent_id  # Store only the agent ID
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
        case "REGISTER_AGENT":
            new_state = state.copy()
            new_state["agents"] = new_state.get("agents", {})
            new_state["agents"][action["agent"]["name"]] = action["agent"]
            return new_state
        case _:
            return state
