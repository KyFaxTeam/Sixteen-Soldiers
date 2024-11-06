from typing import List, Dict
from models.coup import Coup



def historique_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les modifications liées à l'historique des coups.
    """
    match action['type']:
        case 'ADD_MOVE':
            return {**state, 'historique': state['historique'] + [action['coup']]}
        case 'UNDO_MOVE':
            return {**state, 'historique': state['historique'][:-1]}
        case _:
            return state