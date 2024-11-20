from typing import Dict
from models.board import Board
from models.time_manager import TimeManager
from utils.const import PLAYER_CONFIG

def initialize_game(state: Dict) -> Dict:
    """Initialize the game state"""
    # Ensure we have a valid state to work with
    if state is None:
        state = {}
    
    # Trouver l'index du PLAYER_1 dans la liste des joueurs
    player_1_index = next(
        (i for i, player in enumerate(state.get("players", [])) 
         if player.id == PLAYER_CONFIG["PLAYER_1"]), 
        0  # default to 0 if not found
    )
    # winner = {name: agent.name, avatar : ..., remaining_soldiers : agent..., ai_name :...., time_remaining : TimeManager[]..., }
    new_state = state.copy()
    new_state.update({
        "board": new_state.get("board", Board()),
        "time_manager": new_state.get("time_manager",TimeManager()),
        "players": new_state.get("players", []), # Preserve existing players if any
        "game_over": False,
        "current_player_index": player_1_index,  # Utiliser l'index du PLAYER_1
        "winner": {},
        "history": [],
        "last_board_action": None

    })
    return new_state

def change_current_player(state: Dict) -> Dict:
    """Switch to next player"""
    new_state = state.copy()
    new_state["current_player_index"] = state["current_player_index"] * -1
    return new_state

def end_game(state: Dict, winner_id: str) -> Dict:
    """End the game and set winner"""
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
