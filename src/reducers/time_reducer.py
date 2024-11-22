from typing import Dict

def time_reducer(state: Dict, action: Dict) -> Dict:
    if state is None:
        state = {}
    
    state = state.copy()
    
    match action["type"]:
        case "UPDATE_TIME":

            state["time_manager"].update_player_time(
                action["soldier_value"], 
                action["elapsed_time"]
            )
            
    return state