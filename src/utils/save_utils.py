from datetime import datetime
import json
import os

from typing import Dict

from src.agents.base_agent import MatchPerformance
from src.tournament.config import TEAMS_MAPPING
from src.utils.const import Soldier

def convert_data(data, to_json=True):
    """Convert data between internal format and JSON format"""
    if isinstance(data, dict):
        if not to_json and "agents_info_index" in data:
            # Special handling for agents_info_index when loading
            return {k: convert_data(v, to_json) for k, v in data.items()}
        # Normal dict conversion
        return {str(k): convert_data(v, to_json) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_data(item, to_json) for item in data]
    elif isinstance(data, Soldier):
        return data.name if to_json else data
    elif isinstance(data, str) and not to_json and data in ['RED', 'BLUE']:
        return getattr(Soldier, data)
    return data

def convert_agents_info(agents_info):
    """Convert agents_info_index keys to Soldier enums"""
    if not agents_info:
        return {}
    converted = {}
    for key, value in agents_info.items():
        # Convert string key like "Soldier.RED" to enum
        if isinstance(key, str) and key.startswith("Soldier."):
            enum_value = getattr(Soldier, key.split(".")[1])
            converted[enum_value] = value
        else:
            converted[key] = value
    return converted

def save_game(state: Dict) -> Dict:
    """Save the game history to a JSON file with metadata and timestamps"""
    try:
        # Get the game history from the state
        history = state.get("history", [])
        agents = state.get("agents", {})
        agents_info_index = state.get("agents_info_index", {})
        winner = state.get("winner")

        # Define metadata
        metadata = {
            "agents": agents,
            "agents_info_index": agents_info_index,
            "winner": winner,
            "game_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Create the dictionary for JSON file
        data_to_save = {
            "metadata": metadata,
            "history": history
        }
        
        # Define the folder and timestamped file path
        save_folder = os.path.join(os.getcwd(), "saved_game")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        agent1 = state.get("agents_info_index").get(Soldier.RED)
        agent2 = state.get("agents_info_index").get(Soldier.BLUE)
        agent1_pseudo = TEAMS_MAPPING(state.get("agents").get(agent1)["pseudo"])
        agent2_pseudo = TEAMS_MAPPING(state.get("agents").get(agent2)["pseudo"])
        save_file = os.path.join(save_folder, f"game_{agent1_pseudo}_vs_{agent2_pseudo}_{timestamp}.json")
        
        # Create the folder if it doesn't exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Convert data to JSON format
        converted_data = convert_data(data_to_save, to_json=True)
        
        with open(save_file, "w", encoding="utf-8") as file:
            json.dump(converted_data, file, indent=4)
        
        return converted_data
    except Exception as e:

        return None

def load_game(save_file: str) -> Dict:
    """Load the game state from a JSON file"""
    try:
        with open(save_file, 'r', encoding='utf-8') as file:
            saved_state = json.load(file)
        
        # Convert loaded data to internal format
        converted_state = convert_data(saved_state, to_json=False)
        
        # Special handling for agents_info_index
        if "metadata" in converted_state:
            metadata = converted_state["metadata"]
            if "agents_info_index" in metadata:
                metadata["agents_info_index"] = convert_agents_info(metadata["agents_info_index"])
        
        return converted_state
        
    except FileNotFoundError:
        
        return None
    except json.JSONDecodeError as e:
        
        return None

def save_reducer(state: Dict, action: Dict) -> Dict:
    """
    Gère les actions liées à la sauvegarde de la partie.
    """
    match action['type']:
        case 'SAVE_GAME':
            return save_game(state)
        case 'LOAD_GAME':
            loaded_state = load_game()
            # Mise à jour de l'état seulement si un chargement a réussi
            return loaded_state if loaded_state else state
        
        case _:
            return state