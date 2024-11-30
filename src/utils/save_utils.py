import datetime
import json
import os
import pickle

from typing import Dict


def save_game( state: Dict) -> Dict:
    
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
        
        # Save the JSON data to the file
        try:
            with open(save_file, "w", encoding="utf-8") as file:
                json.dump(data_to_save, file, indent=4)
            print(f"Game saved successfully to {save_file}")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")

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