import customtkinter as ctk
import logging

from models.board import Board
from models.player import Player
from utils.game_runner import GameRunner
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.const import PLAYER_CONFIG, THEME_PATH
from agents.random_agent import RandomAgent
from actions.time_actions import initialize_time_control_action


def main():
    # Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='****%(levelname)s  - %(name)s - %(message)s****'# - %(asctime)s****
    )
    logger = logging.getLogger(__name__)
    
    # Configure le thème par défaut et le mode d'apparence
    ctk.set_default_color_theme(THEME_PATH)
    ctk.set_appearance_mode("System")  # ou "Dark", "Light" selon votre préférence
    
    # Créez la fenêtre principale
    root = ctk.CTk()
    
    # Create store with reducer only
    store = Store(
        reducer=root_reducer
    )
    
    # Create and register agents
    agent1 = RandomAgent(
        player=store.get_state()["players"][0],
        name="Random Agent 1"
    )
    agent2 = RandomAgent(
        player=store.get_state()["players"][1],
        name="Random Agent 2"
    )
    
    # Register agents with store
    store.register_agent(agent1)
    store.register_agent(agent2)

    # Créez la vue principale en passant 'root' comme 'master'
    app = MainView(root, store, agent1, agent2)
    app.subscribe(store)
    
    app.run()

    logger.info("Starting the Sixteen Soldiers game")

    # Comment faire alors pour relancer le jeu, recréer les agents 
    # à partir des ia sélectionnées dans l'interface ?
    
   
if __name__ == '__main__':
    main()
