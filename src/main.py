import customtkinter as ctk

from models.board import Board
from models.player import Player
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.const import PLAYER_CONFIG, THEME_PATH
from agents.random_agent import RandomAgent
from actions.time_actions import initialize_time_control_action


def main():
    # Configure le thème par défaut et le mode d'apparence
    ctk.set_default_color_theme(THEME_PATH)
    ctk.set_appearance_mode("System")  # ou "Dark", "Light" selon votre préférence
    
    # Initialize empty state
    initial_state = {
        "board": Board(),
        "game_over": False,
        "joueurs": [
        Player(id=PLAYER_CONFIG["PLAYER_1"], 
               color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_1"]]),
        Player(id=PLAYER_CONFIG["PLAYER_2"], 
               color=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_2"]])
    ]
    }
   
    # Créez la fenêtre principale
    root = ctk.CTk()
    
    # Create store with initial state
    store = Store(
        initial_state=initial_state,
        reducer=root_reducer
    )
    
    # Initialize game state using dispatch
    
    store.dispatch(initialize_time_control_action({}))
    
    # Create agents using store's state
    agent1 = RandomAgent(
        player=store.get_state()["players"][0],
        name="Random Agent"
    )
    agent2 = RandomAgent(
        player=store.get_state()["players"][1],
        name="Random Agent"
    )

    # Créez la vue principale en passant 'root' comme 'master'
    app = MainView(root, store, agent1, agent2)
    app.subscribe(store)
    
    app.run()

    # Comment faire alors pour relancer le jeu, recréer les agents 
    # à partir des ia sélectionnées dans l'interface ?
    
   
if __name__ == '__main__':
    main()
