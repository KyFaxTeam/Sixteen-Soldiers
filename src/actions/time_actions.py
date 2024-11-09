def update_time_action(player_id: str, elapsed_time: float):
    return {
        "type": "UPDATE_TIME",
        "player_id": player_id,
        "elapsed_time": elapsed_time
    }