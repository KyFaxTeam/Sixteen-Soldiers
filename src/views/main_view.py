from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from tkinter import filedialog, Tk
import logging
import os

from src.utils.const import Soldier, resolution, screen_width, screen_height

from src.store.store import Store
from src.utils.save_utils import load_game, save_game
from src.views.Others_Windows.home_view import HomeView
from src.views.base_view import BaseView
from src.views.game_board import GameBoard
from src.views.Others_Windows.after_game_view import AfterGameView
from src.views.Right_Column.history_view import HistoryView
from src.views.Left_Column.players_column import PlayersColumn
from src.views.Right_Column.history_view import HistoryView
from src.views.Right_Column.setting_view import SettingsView
from src.utils.game_utils import GameRunner, show_popup

logger = logging.getLogger(__name__)
class MainView(BaseView):
    """Main window of the application"""
    def __init__(self, master, store):
        super().__init__(master)
        self.store :Store = store
        self.after_game_view = None  # Initialize the attribute to track the view
        self.logger = logging.getLogger(__name__)
        # Set window title
        self.master.title("Sixteen Soldiers")
        
        # Get screen dimensions
        self.adjust_player_column = {
            "HD": "new",
            "Full HD": "nsew",
            "HD+": "nsew",
            "Quad HD":  "nsew",
            "4K Ultra HD":  "nsew"
        }

        
        # Calculate window sizes
        if resolution == "HD":
            self.home_width = int(screen_width * 0.3)
            self.home_height = int(screen_height * 0.4)
            self.game_width = int(screen_width * 0.75)
            self.game_height = int(screen_height * 0.75)
        else :

            self.home_width = int(screen_width * 0.2)
            self.home_height = int(screen_height * 0.3)
            self.game_width = int(screen_width * 0.75)
            self.game_height = int(screen_height * 0.75)
        
        # Set initial size for home view
        self.master.geometry(f"{self.home_width}x{self.home_height}")
        
        # Initialize all component references as None
        self.players_column = None
        self.game_board = None
        self.history_view = None
        self.settings_view = None
        
        # self.start_new_game()
        self.logger = logging.getLogger(__name__)
        # Initialize HomeView
        self.home_view = HomeView(self.master, self.configure_main_view, self.review_match)
        self.home_view.show()
        self.game_runner = GameRunner(self.store)

        # Ajouter un gestionnaire pour la fermeture de la fenêtre
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def configure_main_view(self, game_data=None):
        """Configure la vue principale"""
        self.home_view.hide()
        self.master.geometry(f"{self.game_width}x{self.game_height}")
        self.game_runner.set_mode('replay' if game_data else 'game', game_data)
        self.build_main_view()

    def review_match(self):
        """Review a match by selecting a saved game file and switching to the history view."""
        try:
            root = ctk.CTkToplevel()  # Utiliser CTkToplevel au lieu de Tk
            try:
                save_folder = os.path.join(os.getcwd(), "saved_game")
                if not os.path.exists(save_folder):
                    show_popup("No saved games found. Play and save a game first.", "No Games")
                    return
                
                root.withdraw()  # Cacher la fenêtre
                root.attributes("-topmost", True)
                file_path = filedialog.askopenfilename(
                    parent=root,  # Spécifier le parent
                    title="Select Saved Game File",
                    filetypes=[("JSON Files", "*.json")],
                    initialdir=save_folder
                )
                
                if not file_path:
                    return
                
                # Load and validate the game file
                game_data = load_game(file_path)
                if not game_data or 'history' not in game_data:
                    show_popup("Invalid or corrupted game file.", "Error")
                    return
                
                if not game_data['history']:
                    show_popup("This game file contains no moves to replay.", "Empty Game")
                    return

                self.configure_main_view(game_data=game_data)
            finally:
                root.destroy()  # S'assurer que la fenêtre est détruite
                 
        except Exception as e:
            self.logger.error(f"An error occurred while reviewing the match: {e}")
            show_popup("Error loading replay", "Error", "error")

    def build_main_view(self):
        """Create the main layout and initialize sub-views only when needed"""
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
        self.players_column.frame.grid(row=0, column=0, sticky= self.adjust_player_column[resolution],
                                        padx=(5, 0), pady=30)  # Ajout de pady=20
        
        # Center column - Game board
        self.center_column = ctk.CTkFrame(self.content)
        self.center_column.grid(row=0, column=1, sticky="n")
        
        # Créer le GameBoard sans agents
        self.game_board = GameBoard(self.center_column, self.store, self.game_runner)
        self.game_board.frame.grid(row=0, column=0, sticky="nsew")

        
        # Right column - Move history and settings
        self.right_column = ctk.CTkFrame(self.content)#, fg_color="transparent")
        self.right_column.grid(row=0, column=2, sticky="nsew", padx=(0, 5), pady=(10, 1))
        
        # History view
        self.history_view = HistoryView(self.right_column, self.store)
        self.settings_view = SettingsView(self.right_column, self.store)

    def show_after_game_view(self):
        """Show AfterGameView with winner details"""
        if self.after_game_view is not None:
            # self.logger.warning("AfterGameView is already displayed.")
            return
        
        self.logger.info("Displaying AfterGameView.")
        self.after_game_view = AfterGameView(
            self.master,
            store=self.store,
            on_restart=self.return_to_home,
            on_save=lambda button: self.handle_save(button)
        )
    
    def handle_save(self, button):
        """Handles the save process and updates the button state."""
        try:
            save_game(self.store.get_state())  # Save the game
            button.configure(text="Saved", state="disabled")  # Update button text and disable it
            self.logger.info("Game successfully saved.")
            show_popup("Game successfully saved", "Success", "info")
        except Exception as e:
            self.logger.error(f"An error occurred while saving the game: {e}")

    def return_to_home(self):
        """Reset game and return to HomeView"""
        if self.after_game_view:
            self.after_game_view.destroy()
            self.after_game_view = None

        if hasattr(self, 'main_container'):
            self.main_container.pack_forget()
            del self.main_container

        # Clean up game runner state
        self.game_runner.cleanup()
        
        self.store.dispatch({"type": "RESTART_GAME"})
        
        self.master.geometry(f"{self.home_width}x{self.home_height}")
        self.home_view.show()
      
    def run(self):
        self.master.mainloop()
   
    def update(self, state: dict):
        """Update the view with new state based on game status."""
        # Handle game cleanup
        if state.get("is_game_leaved"):
            self.game_runner.cleanup()
            if hasattr(self, 'history_view'):
                self.history_view.clear_moves()
            if hasattr(self, 'game_board'):    
                self.game_board.cleanup()
            self.after_game_view = None
            self.store.state["is_game_leaved"] = False
            

        # First priority: Check if game is over
        if state["is_game_over"]:
            self.game_runner.cleanup()
            if not self.after_game_view:
                self.show_after_game_view()
            

        # Normal game updates
        if hasattr(self, 'game_board'):
            self.game_board.update(state)

        # Always update players column for agent selection
        if hasattr(self, 'players_column'):
            self.players_column.update(state)

        # Update history view        
        if hasattr(self, 'history_view'):
            self.history_view.update(state)

    def on_closing(self):
        """Gestionnaire de l'événement de fermeture de la fenêtre"""
        # Fermer la fenêtre
        self.master.destroy()