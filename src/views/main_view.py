import customtkinter as ctk
from tkinter import filedialog, Tk
import logging
import os

from src.utils.const import resolution, screen_width, screen_height

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

# winfo_screenwidth() and winfo_screenheight() to get the screen width and height
# winfo_x() and winfo_

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
        self.home_view = HomeView(self.master, self.start_new_game, self.review_match)
        self.home_view.show()
        
    

    def start_new_game(self):
        """Start a new game and switch to game board view"""
        self.home_view.hide()  # Hide the home screen
        self.master.geometry(f"{self.game_width}x{self.game_height}")
        print(f"Game window size: {self.game_width}x{self.game_height}")
        self.create_main_layout()  # Initialize main layout and sub-views

    def review_match(self):
        """Review a match by selecting a saved game file and switching to the history view."""
        try:
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
                # print("No file selected.")
                return
            
            # Load the game state from the selected file
            game_load = load_game(file_path)
            
            if game_load is None:
                # print("Failed to load the game.")
                return
            

            # Display the game history (or pass it to another view)
            # self.logger.info("Game successfully loaded for review.")
            # print(f"Metadata: {game_load['metadata']}")
        

            self.home_view.hide()  # Hide the home screen
            self.master.geometry(f"{self.game_width}x{self.game_height}")
            self.create_main_layout()  # Initialize main layout and sub-views
            
            # Start game replay
            from src.utils.game_utils import GameRunner
            game_runner = GameRunner(self.store)
            game_runner.replay_game(game_load)

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
        self.players_column.frame.grid(row=0, column=0, sticky= self.adjust_player_column[resolution],
                                        padx=(5, 0), pady=30)  # Ajout de pady=20
        
        # Center column - Game board
        self.center_column = ctk.CTkFrame(self.content)
        self.center_column.grid(row=0, column=1, sticky="n")
        
        # Créer le GameBoard sans agents
        self.game_board = GameBoard(self.center_column, self.store)
        self.game_board.frame.grid(row=0, column=0, sticky="nsew")
        self.game_board.subscribe(self.store)
        self.game_board.update(self.store.get_state())
        
        # Right column - Move history and settings
        self.right_column = ctk.CTkFrame(self.content)#, fg_color="transparent")
        self.right_column.grid(row=0, column=2, sticky="nsew", padx=(0, 5), pady=(10, 1))
        
        # History view
        self.history_view = HistoryView(self.right_column, self.store)
        self.settings_view = SettingsView(self.right_column, self.store)

    def show_popup(self, msg: str, title: str = "Warning Message"):
        """Show a popup message relative to the main window position"""
        popup = ctk.CTkToplevel(self.master)
        popup.title(title)
        
        # Make popup stay on top
        popup.transient(self.master)
        popup.grab_set()
        
        # Get main window position and size
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        
        # Position popup relative to main window's center column
        popup_width = 300
        popup_height = 100
        x_position = main_x + (main_width // 2) - (popup_width // 2)
        y_position = main_y + 100  # Position it near the top of the window
        
        popup.geometry(f"{popup_width}x{popup_height}+{x_position}+{y_position}")
        
        label = ctk.CTkLabel(popup, text=msg, pady=20)
        label.pack()
        
        # Auto-close after 4 seconds
        popup.after(4000, popup.destroy)

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

        self.master.geometry(f"{self.home_width}x{self.home_height}")
        
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


