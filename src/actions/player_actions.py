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

def lose_piece(player_id: str) -> Dict:
    """Creates an action to decrement a player's piece count"""
    return {
        "type": "LOSE_PIECE",
        "player_id": player_id
    }

