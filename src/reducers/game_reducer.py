import logging
from typing import Dict
from src.store.store import initial_state
from src.utils.const import Soldier


def reset_game(state: Dict) -> Dict:

    new_state = initial_state.copy()
    new_state["agents"] = state["agents"]
    new_state["agents_info_index"] = state["agents_info_index"]
    new_state["is_game_leaved"] = True
    
    return new_state

def change_current_player(state: Dict) -> Dict:
    """
    Passe au joueur suivant 
    """
    state = state.copy()
    current_soldier_value = state.get("current_soldier_value", Soldier.RED)

    if current_soldier_value == Soldier.RED:
        state["current_soldier_value"] = Soldier.BLUE
    else:
        state["current_soldier_value"] = Soldier.RED
    
    return state


def end_game(state: Dict, winner: Soldier) -> Dict:
    new_state = state.copy()
    new_state["is_game_over"] = True
    new_state["is_game_paused"] = False
    new_state["is_game_started"] = False
    new_state["current_soldier_value"] = None
    new_state["winner"] = winner
    return new_state

def pause_game(state: Dict) -> Dict:
    """Pause the game."""
    new_state = state.copy()
    new_state['is_game_paused'] = True
    return new_state

def resume_game(state: Dict) -> Dict:
    """Resume the game."""
    new_state = state.copy()
    new_state['is_game_paused'] = False
    return new_state

def select_agent(state: Dict, action: Dict) -> Dict:
    new_state = state.copy()
    new_state["agents_info_index"][action["soldier_value"]] = action["info_index"]
    new_state["agents"][action["info_index"]] = {"pseudo" : action["info_index"].rsplit('_', 1)[0]}
    return new_state

def register_agents(state: Dict, action: Dict) -> Dict:
    
    
    new_state = state.copy()
    for payload in [action["payload1"], action["payload2"]]:
        if payload is None:
            continue
        else :
            pseudo = payload["pseudo"]
            soldier_value = payload["soldier_value"]
            info_index = f'{pseudo}_{soldier_value.name}'

            new_state["agents"][info_index] = payload

            new_state["agents_info_index"][soldier_value] = info_index
    
    logging.info(f"Have registered agent {new_state['agents']}")
    return new_state

def game_reducer(state: Dict, action: Dict) -> Dict:
    
        
    match action["type"]:
        case "RESET_GAME":
            return reset_game(state)
        case "CHANGE_CURRENT_SOLDIER":
            return change_current_player(state)
        case "END_GAME":
            return end_game(state, action.get("winner"))
        case "PAUSE_GAME":
            return pause_game(state)
        case "RESUME_GAME":
            return resume_game(state)
        case "REGISTER_AGENTS":
            return register_agents(state, action)
        case "SELECT_AGENT":
            return select_agent(state, action)
        
        case _:
            return state
