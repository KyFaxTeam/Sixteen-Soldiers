from typing import Dict
from models.time_manager import TimeManager
from utils.const import INITIAL_VALUES

def time_reducer(state: Dict, action: Dict) -> Dict:
    if state is None:
        state = {}
    
    state = state.copy()
    
    match action["type"]:
        case "UPDATE_TIME":
            if "time_manager" not in state or state["time_manager"] is None:
                raise ValueError("TimeManager is not initialized")
                
            state["time_manager"].update_player_time(
                action["player_id"], 
                action["elapsed_time"]
            )
            
        case "INITIALIZE_TIME_CONTROL":
            state["time_manager"] = TimeManager()
            time_limits = action.get("time_limits", {})
            
            # Si time_limits est vide ou None, utilise INITIAL_VALUES['TIMER'] pour les deux joueurs
            if not time_limits:
                time_limits = {1: INITIAL_VALUES['TIMER'], -1: INITIAL_VALUES['TIMER']}
            
            state["time_manager"].set_time_limits(time_limits)
            
    return state