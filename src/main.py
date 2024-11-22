import customtkinter as ctk
import logging

from models.board import Board
from utils.game_utils import GameRunner
from utils.logger_config import get_logger, setup_logging
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.const import THEME_PATH

def main():
    # Configure basic logging
    setup_logging(level=logging.INFO)
    logger = get_logger(__name__)
    
    # Configure le thème par défaut et le mode d'apparence
    ctk.set_default_color_theme(THEME_PATH)
    ctk.set_appearance_mode("System")
    
    # Créez la fenêtre principale
    root = ctk.CTk()
    
    # Create store with reducer only
    store = Store(reducer=root_reducer)
    
    # Create main view without agents - they'll be created through the UI
    app = MainView(root, store)
    app.subscribe(store)
    
    app.run()

    logger.info("Starting the Sixteen Soldiers game")
   
if __name__ == '__main__':
    main()
