from datetime import datetime
import json
import os
import pickle

from typing import Dict

from src.agents.base_agent import MatchPerformance
from src.utils.const import Soldier


def save_game( state: Dict) -> Dict:
        
        print("saving game")
    
        """Save the game history to a JSON file with metadata and a timestamped filename"""
        # Get the game history from the state
        history = state.get("history", [])
        agents = state.get("agents", {})
        agents_info_index = state.get("agents_info_index", {})
        winner = state.get("winner")

        # Define metadata
        metadata = {
            "players": agents,
            "info_index": agents_info_index,
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
        save_file = os.path.join(save_folder, f"game_{timestamp}.json")
        
        # Create the folder if it doesn't exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        converted_data = convert_keys_to_strings(data_to_save)
        
        # Save the JSON data to the file
        try:
            with open(save_file, "w", encoding="utf-8") as file:
                json.dump(converted_data, file, indent=4, default=custom_serializer)
            print(f"Game saved successfully to {save_file}")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")

# Define a custom serializer for Enum
def custom_serializer(obj):
    if isinstance(obj, Soldier):
        return obj.name  # Serialize as the enum name (e.g., "RED", "BLUE")
    if isinstance(obj, MatchPerformance):
        # Serialize MatchPerformance as a dictionary
        return {
            "issue": obj.issue,
            "number_of_moves": obj.number_of_moves,
            "time": obj.time,
            "opponent": obj.opponent,
        }
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

def convert_keys_to_strings(data):
    """
    Recursively converts dictionary keys to strings if they are not of a JSON-compatible type.
    """
    if isinstance(data, dict):
        return {str(k): convert_keys_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_strings(item) for item in data]
    elif isinstance(data, Soldier):
        return data.name  # Convert Soldier directly to its name
    else:
        return data



def load_game(save_file: str = 'save.pkl') -> Dict:
    """
    Charge l'état des joueurs et de l'historique à partir d'une sauvegarde.
   
    Args:
        save_file (str): Chemin du fichier de sauvegarde (par défaut 'save.pkl').
   
    Returns:
        dict: Nouvel état des joueurs et de l'historique.
    """
    try:
        with open(save_file, 'rb') as f:
            saved_state = pickle.load(f)
    except FileNotFoundError:
        print("No saved game found.")
        return None
    
    players = saved_state['players']
    history = saved_state['history']
    
    return {
        'players': players,
        'history': history
    }

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