from typing import Dict


def change_current_player(new_player):
    return {
        "type": "CHANGE_CURRENT_PLAYER",
        "new_player": new_player
    }

def initialize_players(player1_time: float, player2_time: float) -> Dict:
    """Creates an action to initialize players with time controls"""
    return {
        "type": "INITIALIZE_PLAYERS",
        "player1_time": player1_time,
        "player2_time": player2_time
    }

def update_player_time(player_id: str, elapsed_time: float) -> Dict:
    """Creates an action to update a player's time"""
    return {
        "type": "UPDATE_PLAYER_TIME",
        "player_id": player_id,
        "elapsed_time": elapsed_time
    }


def set_player_color(player, new_color):
    return {
        "type": "SET_PLAYER_COLOR",
        "player": player,
        "new_color": new_color
    }