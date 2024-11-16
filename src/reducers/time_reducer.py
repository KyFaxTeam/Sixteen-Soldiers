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
            # Utilise directement INITIAL_VALUES['TIMER'] pour tous les joueurs
            state["time_manager"].set_time_limits(
                {player_id: INITIAL_VALUES['TIMER'] for player_id in action["time_limits"].keys()}
            )
            
    return state