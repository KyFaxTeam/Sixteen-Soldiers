from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.theme import ThemeManager
from agents.random_agent import RandomAgent
from utils.game_runner import GameRunner
from utils.const import PLAYER_CONFIG


def main():
    
    ThemeManager.setup_theme()
    
    # Create two random agents with different IDs (1 and -1)
    agent1 = RandomAgent(
        id=PLAYER_CONFIG["PLAYER_1"],
        nom="Agent Rouge", 
        couleur=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_1"]]
    )
    agent2 = RandomAgent(
        id=PLAYER_CONFIG["PLAYER_2"],
        nom="Agent Bleu", 
        couleur=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_2"]]
    )
    
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