import customtkinter as ctk
import logging
from utils.logger_config import get_logger, setup_logging
from views.main_view import MainView
from store.store import Store
from reducers.index import root_reducer
from utils.const import THEME_PATH

def main():
    # Setup logging
    setup_logging()
    # Configure logging for all modules
    # logging.basicConfig(
    #     level=logging.INFO,
    #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #     handlers=[
    #         logging.StreamHandler(),
    #         logging.FileHandler('game.log')
    #     ]
    # )
    # # Ensure loggers propagate to root
    # logging.getLogger().setLevel(logging.INFO)
    
    logger = get_logger(__name__)
    
    ctk.set_default_color_theme(THEME_PATH)
    ctk.set_appearance_mode("System")
    
    # Créez la fenêtre principale
    root = ctk.CTk()
    
    # Create store with reducer only
    store = Store(reducer=root_reducer)
    
   
    app = MainView(root, store)
    app.subscribe(store)
    
    app.run()

    logger.info("Application closed")

if __name__ == '__main__':
    main()
