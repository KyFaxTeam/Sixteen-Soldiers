import customtkinter as ctk
import logging

from store.store import Store
from utils.save_utils import save_game

from views.Others_Windows.home_view import HomeView
from views.base_view import BaseView
from views.game_board import GameBoard
from views.Others_Windows.after_game_view import AfterGameView
from views.Right_Column.history_view import HistoryView
from views.Left_Column.players_column import PlayersColumn
from .Right_Column.history_view import HistoryView
from .Right_Column.setting_view import SettingsView

logger = logging.getLogger(__name__)

class MainView(BaseView):
    """Main window of the application"""

    def __init__(self, master, store):
        super().__init__(master)
        self.store :Store = store
        self.after_game_view = None  # Initialize the attribute to track the view
        self.logger = logging.getLogger(__name__)
        self.master.title("Sixteen Soldiers")
        self.master.geometry("400x300")
        
        # Initialize all component references as None
        self.players_column = None
        self.game_board = None
        self.history_view = None
        self.settings_view = None
        
        # self.start_new_game()
        self.logger = logging.getLogger(__name__)
        # Initialize HomeView
        self.home_view = HomeView(self.master, self.start_new_game, self.review_match)
        self.home_view.show()
        
    def start_new_game(self):
        """Start a new game and switch to game board view"""
        self.home_view.hide()  # Hide the home screen
        self.master.geometry("1200x800")
        self.create_main_layout()  # Initialize main layout and sub-views

    def review_match(self):
        """Review a match and switch to history view"""
        self.home_view.hide()  # Hide the home screen
        self.master.geometry("1200x700")
        self.create_main_layout()  # Ensure the main layout is created
        # Initialize or load state as needed
        # For example, you might load a saved game state here
        # self.load_saved_game_state()
        

    def create_main_layout(self):
        """Create the main layout and initialize sub-views only when needed"""
        # Destroy existing frames if they exist
        if hasattr(self, 'main_container'):
            self.main_container.destroy()

        # Create main container frame
        self.main_container = ctk.CTkFrame(self.master) 
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Content frame with 3 columns
        self.content = ctk.CTkFrame(self.main_container)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)
        self.content.grid_columnconfigure(0, weight=1)  # Adjust left column width
        self.content.grid_columnconfigure(1, weight=2)  # Center column expands
        self.content.grid_columnconfigure(2, weight=1)  # Right column
        
        # Left column - Players
        self.players_column = PlayersColumn(self.content, self.store)
        self.players_column.frame.grid(row=0, column=0, sticky="nsew", padx=(0, 0), pady=30)  # Ajout de pady=20
        
        # Center column - Game board
        self.center_column = ctk.CTkFrame(self.content)
        self.center_column.grid(row=0, column=1)
        
        # Créer le GameBoard sans agents
        self.game_board = GameBoard(self.center_column, self.store)
        self.game_board.frame.pack(expand=True, fill="both")
        self.game_board.subscribe(self.store)
        self.game_board.update(self.store.get_state())
        
        # Right column - Move history and settings
        self.right_column = ctk.CTkFrame(self.content)#, fg_color="transparent")
        self.right_column.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # History view
        self.history_view = HistoryView(self.right_column, self.store)
        self.settings_view = SettingsView(self.right_column, self.store)


    def show_after_game_view(self):
        """Show AfterGameView with winner details"""
        if self.after_game_view is not None:
            self.logger.warning("AfterGameView is already displayed.")
            return
        
        self.logger.info("Displaying AfterGameView.")
        self.after_game_view = AfterGameView(
            self.master,
            store=self.store,
            on_restart=self.restart_game,
            on_save=lambda: save_game(self.store.get_state())
        )

    def restart_game(self):
        """Reset the game and return to HomeView"""
        # Close any existing AfterGameView if open
        if self.after_game_view:
            self.after_game_view.destroy()
            self.after_game_view = None  # Reset the view reference

        self.store.dispatch({"type":"RESET_GAME"})
        
        # Reset the main layout (clear current game views if necessary)
        if hasattr(self, 'main_container'):
            self.main_container.pack_forget()
            del self.main_container

        # Resize window for HomeView
        self.master.geometry("400x300")
        
        # Show HomeView again
        self.home_view.show()

        
    def run(self):
        self.master.mainloop()

    

    def update(self, state: dict):
        """
        Update the view with new state.
        Only updates components if the game has started.
        """
        # Ne pas réassigner directement le state
        if not state["is_game_started"]:
            if hasattr(self, 'players_column'):
                self.players_column.update(state)
            return 
        
        if hasattr(self, 'players_column'):
            self.players_column.update(state)
        if hasattr(self, 'game_board'):
            self.game_board.update(state)
        if hasattr(self, 'history_view'):
            self.history_view.update(state)
        if state["is_game_over"]:
            self.logger.info("Game is over - show_after_game_view")
            self.show_after_game_view()


