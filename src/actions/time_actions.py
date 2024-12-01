from src.utils.const import Soldier

def update_time_action(soldier_value:Soldier , elapsed_time: float):
    return {
        "type": "UPDATE_TIME",
        "soldier_value": soldier_value,
        "elapsed_time": elapsed_time
    }

