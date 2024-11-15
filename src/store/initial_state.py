
from models.player import Player
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.theme_manager import ThemeManager
from agents.random_agent import RandomAgent
from utils.game_runner import GameRunner
from reducers.player_reducer import initialize_players


def main():
    ThemeManager.setup_theme()
    
    # Initialize empty state and add players
    initial_state = {}
    initial_state = initialize_players(initial_state)
    
    # Add theme to initial state
    initial_state["theme"] = "dark"
    
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
    
    # Create main window
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