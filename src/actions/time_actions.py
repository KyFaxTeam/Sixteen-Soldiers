from utils.const import Soldier

def update_time_action(soldier_value:Soldier , elapsed_time: float):
    return {
        "type": "UPDATE_TIME",
        "soldier_value": soldier_value,
        "elapsed_time": elapsed_time
    }

def initialize_time_control_action(time_limits: dict):
    return {
        "type": "INITIALIZE_TIME_CONTROL",
        "time_limits": time_limits
    }