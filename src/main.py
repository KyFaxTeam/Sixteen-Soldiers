import customtkinter as ctk
from models.player import Player
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.const import THEMES_DIR, THEME_PATH
from agents.random_agent import RandomAgent
from utils.game_runner import GameRunner
from reducers.player_reducer import initialize_players


def main():
    # Configure le thème par défaut et le mode d'apparence
    ctk.set_default_color_theme(THEME_PATH)
    ctk.set_appearance_mode("System")  # ou "Dark", "Light" selon votre préférence
    
    # Initialize empty state and add players
    initial_state = {}
    initial_state = initialize_players(initial_state)
    
    # Create agents using the initialized players
    agent1 = RandomAgent(
        player=initial_state["players"][0],
        name="Random Agent"
    )
    agent2 = RandomAgent(
        player=initial_state["players"][1],
        name="Random Agent"
    )
    
    # Create store with initial state
    store = Store(
        initial_state=initial_state,
        reducer=root_reducer
    )
    
    # Create main window and ensure all child views are subscribed
    app = MainView()
    app.subscribe(store)

    # Start the game between agents
    runner = GameRunner(store)
    runner.run_player_game(agent1, agent2)

    # Comment faire alors pour relancer le jeu, recréer les agents 
    # à partir des ia sélectionnées dans l'interface ?
    
    # Run the GUI
    app.run()

if __name__ == "__main__":
    main()