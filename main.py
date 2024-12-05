import customtkinter as ctk
import logging
from src.models.assets.index import Assets
from src.utils.logger_config import get_logger, setup_logging
from src.views.main_view import MainView
from src.store.store import Store
from src.reducers.index import root_reducer
from src.utils.const import THEME_PATH

def main():
    # Setup logging
    setup_logging()
   
    logger = get_logger(__name__)
    
    ctk.set_default_color_theme(THEME_PATH)
    ctk.set_appearance_mode("System")
    
    # Créez la fenêtre principale
    root = ctk.CTk()
    
    # Create store with reducer only
    store = Store(reducer=root_reducer)
    
    # Add icons to the main window
    try:
        root.iconbitmap(Assets.icon_favicon)
    except Exception as e:
        logger.warning(f"Failed to set window favicon icon: {e}")
    
    app = MainView(root, store)
    app.subscribe(store)
    
    app.run()

    logger.info("Application closed")

if __name__ == '__main__':
    main()
