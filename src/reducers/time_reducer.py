from typing import Dict
from models.time_manager import TimeManager

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
            
    return state