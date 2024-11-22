from typing import Dict


def change_current_player(new_player):
    return {
        "type": "CHANGE_CURRENT_PLAYER",
        "new_player": new_player
    }

# def initialize_players_action():
#     return {
#         "type": "INITIALIZE_PLAYERS"
#     }

def reset_players():
    return {
        "type": "RESET_PLAYERS"
    }


def lose_piece(player_id: str) -> Dict:
    """Creates an action to decrement a player's piece count"""
    return {
        "type": "LOSE_PIECE",
        "player_id": player_id
    }

