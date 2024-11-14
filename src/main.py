from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.theme import ThemeManager
from agents.random_agent import RandomAgent
from utils.game_runner import GameRunner


def main():
    
    ThemeManager.setup_theme()
    
    # Create two random agents with different names
    agent1 = RandomAgent(id="red", nom="Agent Rouge", couleur="red")
    agent2 = RandomAgent(id="green", nom="Agent Vert", couleur="green")
    
    # Initialize store with minimal initial state
    initial_state = {
        "players": [agent1, agent2]  # Only initialize players, rest will be handled by INITIALIZE_GAME
    }
    
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
    
    # Run the GUI
    app.run()

if __name__ == "__main__":
    main()