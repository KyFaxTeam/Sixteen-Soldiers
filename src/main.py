from models.player import Player
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.theme import ThemeManager
from agents.random_agent import RandomAgent
from utils.game_runner import GameRunner
from utils.const import PLAYER_CONFIG


def main():
    
    ThemeManager.setup_theme()
    
    # Créer d'abord les Players
    player1 = Player(
        id=PLAYER_CONFIG["PLAYER_1"],
        nom="Joueur Rouge", 
        couleur=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_1"]]
    )
    player2 = Player(
        id=PLAYER_CONFIG["PLAYER_2"],
        nom="Joueur Bleu", 
        couleur=PLAYER_CONFIG["COLORS"][PLAYER_CONFIG["PLAYER_2"]]
    )
    
    # Puis créer les agents qui utilisent ces players
    agent1 = RandomAgent(player1)
    agent2 = RandomAgent(player2)
    
    # Initialize store with minimal initial state
    initial_state = {
        "players": [player1, player2]  # On stocke les Players, pas les Agents
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