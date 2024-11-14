from models.player import Player
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.theme import ThemeManager
from agents.random_agent import RandomAgent
from utils.game_runner import GameRunner
from utils.const import PLAYER_CONFIG
from reducers.player_reducer import initialize_players


def main():
    ThemeManager.setup_theme()
    
    # Initialize empty state and add players
    initial_state = {}
    initial_state = initialize_players(initial_state)
    
    # Create agents using the initialized players
    agent1 = RandomAgent(
        player=initial_state["players"][0],
        name="Agent Rouge"
    )
    agent2 = RandomAgent(
        player=initial_state["players"][1],
        name="Agent Bleu"
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
    
    # Run the GUI
    app.run()

if __name__ == "__main__":
    main()