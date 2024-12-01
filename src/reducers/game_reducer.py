import logging
from typing import Dict
from store.store import initial_state
from utils.const import Soldier
from utils.history_utils import get_last_move


def reset_game(state: Dict) -> Dict:
    new_state = initial_state.copy()

    return new_state

def change_current_player(state: Dict) -> Dict:
    """
    Passe au joueur suivant 
    """
    state = state.copy()

    last_move = get_last_move(state)

    if last_move is not None:
        
        current_soldier_value = last_move.soldier_value

        if state["board"].get_is_multi_capture() :
            state["current_soldier_value"] = current_soldier_value 
        else:
            state["current_soldier_value"] = Soldier.BLUE if current_soldier_value == Soldier.RED else Soldier.RED
            
        return state
    else :
        return state
    

def end_game(state: Dict, winner: Soldier) -> Dict:
    new_state = state.copy()
    new_state["is_game_over"] = True
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
