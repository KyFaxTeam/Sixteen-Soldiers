from typing import Dict


def time_reducer(state: Dict, action: Dict) -> Dict:
    if action["type"] == "UPDATE_TIME":
        player_id = action["player_id"]
        elapsed = action["elapsed_time"]
        # Update time based on your chosen structure
        # ...