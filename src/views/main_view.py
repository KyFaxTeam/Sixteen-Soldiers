import CTkMessagebox
import customtkinter as ctk
from tkinter import filedialog, Tk
import logging
import os

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

    def setup_game_view(self):  # Renamed from start_new_game
        """Setup the game view layout and initialize components"""
        self.home_view.hide()
        self.master.geometry("1200x800")
        self.create_main_layout()

    def start_new_game(self):
        """Start a new game and switch to game board view"""
        self.home_view.hide()  # Hide the home screen
        self.master.geometry("1200x600")
        self.create_main_layout()  # Initialize main layout and sub-views

    def review_match(self):
        """Review a match by selecting a saved game file and switching to the history view."""
        try:
            save_folder = os.path.join(os.getcwd(), "saved_game")
            if not os.path.exists(save_folder):
                self.show_popup("No saved games found. Play and save a game first.", "No Games")
                return
            
            # Open file dialog to select the saved game JSON file
            root = Tk()
            root.withdraw()  # Hide the root window
            root.attributes("-topmost", True)  # Bring the dialog to the front
            file_path = filedialog.askopenfilename(
                title="Select Saved Game File",
                filetypes=[("JSON Files", "*.json")],
                initialdir=os.path.join(os.getcwd(), "saved_game")
            )
            
            if not file_path:
                return
            
            # Load and validate the game file
            game_data = load_game(file_path)
            if not game_data or 'history' not in game_data:
                self.show_popup("Invalid or corrupted game file.", "Error")
                return
            
            if not game_data['history']:
                self.show_popup("This game file contains no moves to replay.", "Empty Game")
                return
            

            from src.utils.game_utils import GameRunner
            game_runner = GameRunner(self.store)

            self.home_view.hide()  # Hide the home screen
            self.master.geometry("400x300")
            self.create_main_layout()  # Initialize main layout and sub-views
            
        except Exception as e:
            print(f"An error occurred while reviewing the match: {e}")

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
        self.players_column.frame.grid(row=0, column=0, sticky="new", padx=(0, 0), pady=20)  # Ajout de pady=20
        
        # Center column - Game board
        self.center_column = ctk.CTkFrame(self.content)
        self.center_column.grid(row=0, column=1)
        
        # Créer le GameBoard sans agents
        self.game_board = GameBoard(self.center_column, self.store)
        self.game_board.frame.pack(expand=True, fill="both")
        self.game_board.subscribe(self.store)
        self.game_board.update(self.store.get_state())
        
        # Right column - Move history and settings
        self.right_column = ctk.CTkFrame(self.content)
        self.right_column.grid(row=0, column=2, sticky="ew", padx=(10, 0))  # Allow second row to expand vertically
        self.right_column.grid_columnconfigure(0, weight=1)  # Allow column to expand horizontally
        self.right_column.grid_rowconfigure(0, weight=3)  # Increased weight for history
        # History view
        self.history_view = HistoryView(self.right_column, self.store)
        self.history_view.frame.grid(row=0, column=0, sticky="new", padx=10)

        # Settings view
        self.settings_view = SettingsView(self.right_column, self.store)
        self.settings_view.frame.grid(row=1, column=0, sticky="new", padx=10)  # Changed to 'sew' to stick to bottom
        #self.settings_view.frame.grid_propagate(False) 

    def show_popup(message: str, title: str = "Message", auto_close: bool = True, duration: int = 2000):
        """Show a popup message using CTkMessagebox that auto-closes after duration milliseconds."""
        popup = CTkMessagebox(
            title=title,
            message=message,
            icon="info",
            width=250,
            height=150,
            font=("Roboto", 12),
            justify="center",
            fade_in_duration=0.2,
        )
        
        if auto_close:
            popup.after(duration, popup.destroy)

    def show_after_game_view(self):
        """Show AfterGameView with winner details"""
        if self.after_game_view is not None:
            # self.logger.warning("AfterGameView is already displayed.")
            return
        
        self.logger.info("Displaying AfterGameView.")
        self.after_game_view = AfterGameView(
            self.master,
            store=self.store,
            on_restart=self.restart_game,
            on_save=lambda button: self.handle_save(button)
        )
    
    def handle_save(self, button):
        """Handles the save process and updates the button state."""
        try:
            save_game(self.store.get_state())  # Save the game
            button.configure(text="Saved", state="disabled")  # Update button text and disable it
            self.logger.info("Game successfully saved.")
            self.show_popup("Game successfully saved", "Success", "info")
        except Exception as e:
            self.logger.error(f"An error occurred while saving the game: {e}")

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
        Update the view with new state based on game status.
        """
        # First priority: Check if game is over
        if state["is_game_over"]:
            if not self.after_game_view:
                self.show_after_game_view()
            return

        # Handle game reset/cleanup
        if not state["is_game_started"] and hasattr(self, 'history_view') and hasattr(self, 'game_board'):
            if state.get("is_game_leaved"):
                self.history_view.clear_moves()
                self.game_board.clear_board()
                # Reset after_game_view reference when game is reset
                self.after_game_view = None
        
        # Always update players column for agent selection
        if hasattr(self, 'players_column'):
            self.players_column.update(state)
        
        # If game hasn't started, don't update game components
        if not state["is_game_started"]:
            return

        # Normal game updates
        if hasattr(self, 'game_board'):
            self.game_board.update(state)
        if hasattr(self, 'history_view'):
            self.history_view.update(state)


