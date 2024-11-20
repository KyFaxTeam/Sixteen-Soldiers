from typing import Dict
from models.time_manager import TimeManager
from utils.const import INITIAL_VALUES, PLAYER_CONFIG

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
            # Utiliser les time_limits fournis ou les valeurs par défaut
            time_limits = action.get("time_limits") or {
                PLAYER_CONFIG["PLAYER_1"]: INITIAL_VALUES["TIMER"],
                PLAYER_CONFIG["PLAYER_2"]: INITIAL_VALUES["TIMER"]
            }
            state["time_manager"].set_time_limits(time_limits)
            
    return state