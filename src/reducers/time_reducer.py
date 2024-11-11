from typing import Dict
from models.time_manager import TimeManager

def time_reducer(state: Dict, action: Dict) -> Dict:
    if state is None:
        state = {}
    
    state = state.copy()
    
    if action["type"] == "UPDATE_TIME":
        player_id = action["player_id"]
        elapsed = action["elapsed_time"]
        
        if "time_manager" not in state or state["time_manager"] is None:
            #déclencher une erreur
            raise ValueError("TimeManager is not initialized")
            
        state["time_manager"].update_player_time(player_id, elapsed)
        
    elif action["type"] == "INITIALIZE_TIME_CONTROL":
        # Supposant que l'action peut inclure un 'increment' optionnel
        increment = action.get("increment", 0.0)
        state["time_manager"].set_time_limits(action["time_limits"], increment)
    
    elif action["type"] == "END_GAME":
        # Optionnel : Finaliser le TimeManager si nécessaire
        pass
    
    # ... implémenter d'autres actions liées au temps si nécessaire ...
    
    return state