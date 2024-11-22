# Actions types
ADD_MOVE_TO_HISTORY = "ADD_MOVE_TO_HISTORY"
UNDO_MOVE = "UNDO_MOVE"
CLEAR_HISTORY = "CLEAR_HISTORY"
SET_HISTORY_NAVIGATION_INDEX = "SET_HISTORY_NAVIGATION_INDEX"

def add_move_to_history(from_pos: str, to_pos: str, player_id: int, timestamp: float, piece_capturee:str = None):
    """Ajoute un nouveau mouvement à l'historique"""
    return {
        "type": ADD_MOVE_TO_HISTORY,
        "payload": {
            "from_pos": from_pos,
            "to_pos": to_pos,
            "player_id": player_id,
            "timestamp": timestamp,
            "piece_capturee": piece_capturee,
        }
    }

def undo_last_move():
    """Crée une action pour annuler le dernier mouvement"""
    return {
        "type": "UNDO_LAST_MOVE"
    }

def redo_move():
    """Crée une action pour refaire un mouvement annulé"""
    return {
        "type": "REDO_MOVE"
    }

def clear_history():
    """Efface tout l'historique"""
    return {
        "type": CLEAR_HISTORY
    }

def set_history_navigation_index(index):
    """Définit l'index de navigation dans l'historique"""
    return {
        "type": SET_HISTORY_NAVIGATION_INDEX,
        "payload": index
    }

# def undo_move(moves_count=1):
#     """Annule un nombre spécifique de mouvements"""
#     return {
#         "type": UNDO_MOVE,
#         "payload": moves_count
#     }


# def save_history():
#     """Sauvegarde l'historique actuel"""
#     return {
#         "type": SAVE_HISTORY
#     }

# def load_history(saved_history):
#     """Charge un historique sauvegardé"""
#     return {
#         "type": LOAD_HISTORY,
#         "payload": saved_history
#     }

