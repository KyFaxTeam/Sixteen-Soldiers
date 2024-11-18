from typing import Dict
from copy import deepcopy
from .game_reducer import game_reducer
from .board_reducer import BoardReducer
from .player_reducer import player_reducer
from .history_reducer import history_reducer
from .time_reducer import time_reducer

def root_reducer(state: Dict, action: Dict) -> Dict:
    """
    Combine all reducers and apply them in specific order:
    game → board → player → history → time
    """
    # Create a deep copy to avoid state mutations
    new_state = deepcopy(state)
    
    # Apply reducers in sequence
    new_state = game_reducer(new_state, action)
    
    new_state = BoardReducer.board_reducer(new_state, action)
    
    new_state = player_reducer(new_state, action)
    
    new_state = history_reducer(new_state, action)
   
    new_state = time_reducer(new_state, action)
    
    
    return new_state