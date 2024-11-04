def change_current_player(new_player):
    return {
        "type": "CHANGE_CURRENT_PLAYER",
        "new_player": new_player
    }

def increment_score(player, points):
    return {
        "type": "INCREMENT_SCORE",
        "player": player,
        "points": points
    }

def set_player_name(player, new_name):
    return {
        "type": "SET_PLAYER_NAME",
        "player": player,
        "new_name": new_name
    }

def set_player_color(player, new_color):
    return {
        "type": "SET_PLAYER_COLOR",
        "player": player,
        "new_color": new_color
    }