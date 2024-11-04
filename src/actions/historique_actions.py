def add_move_to_history(move):
    return {
        "type": "ADD_MOVE_TO_HISTORY",
        "move": move
    }

def clear_move_history():
    return {
        "type": "CLEAR_MOVE_HISTORY"
    }

def save_game_state(game_state):
    return {
        "type": "SAVE_GAME_STATE",
        "game_state": game_state
    }

def load_game_state(game_state):
    return {
        "type": "LOAD_GAME_STATE",
        "game_state": game_state
    }