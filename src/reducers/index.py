from logging import getLogger
from typing import Dict
from copy import deepcopy
from .game_reducer import game_reducer
from .board_reducer import board_reducer

from .history_reducer import history_reducer
from .time_reducer import time_reducer

logger = getLogger(__name__)

def root_reducer(state: Dict, action: Dict) -> Dict:
    """
    Combine all reducers and apply them in specific order:
    game → board → history → time
    """
    # Log action reception with simple separator
    if action['type'] not in ['UPDATE_TIME', 'ADD_MOVE_TO_HISTORY', 'CHANGE_CURRENT_SOLDIER', "MOVE_SOLDIER", "CAPTURE_SOLDIER"]:
       logger.info(f"▶ Processing {action['type']}")
    
    # Create single copy of state
    new_state = deepcopy(state)
    
    # Define reducer chain
    reducers = [
        ('game', game_reducer),
        ('board', board_reducer),
        ('history', history_reducer),
        ('time', time_reducer)
    ]

    # Apply reducers sequentially
    for name, reducer in reducers:
        try:
            new_state = reducer(new_state, action)
        except Exception as e:
            logger.error(f"Error in {name}_reducer: {e}")

            # mettre le jeu sur pause s'il y a une erreur
            # new_state["is_game_paused"] = True
        
    if action['type'] in ['MOVE_SOLDIER', 'CAPTURE_SOLDIER']:
        # logger.info(f"Action done :{action}")
        ...
        
    return new_state

