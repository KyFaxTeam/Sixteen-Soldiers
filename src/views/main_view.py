import customtkinter as ctk

from views.game_board import GameBoard
from views.historique_view import HistoriqueView
from views.base_view import BaseView
from views.Left_Column.players_column import PlayersColumn
from .historique_view import HistoriqueView
from .home_view import HomeView

class MainView(BaseView):
    """Main window of the application"""

    def __init__(self):
        # Configure main window
        self.window = ctk.CTk()
        self.window.title("Sixteen Soldiers")
        self.window.geometry("400x300")
        
        # Initialize HomeView and set callback functions for the buttons
        self.home_view = HomeView(self.window, self.start_new_game, self.review_match)
        self.home_view.show()


    def start_new_game(self):
        """Start a new game and switch to game board view"""
        self.home_view.hide()  # Hide the home screen
        self.window.geometry("1200x800")
        self.create_main_layout()  # Initialize main layout and sub-views
        

    def review_match(self):
        """Review a match and switch to history view"""
        self.home_view.hide()  # Hide the home screen
        self.window.geometry("1200x800")
        self.create_main_layout()  # Initialize main layout and sub-views
        

    def create_main_layout(self):
        """Create the main layout and initialize sub-views only when needed"""
        # Create main container frame
        self.main_container = ctk.CTkFrame(self.window)
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Content frame with 3 columns
        self.content = ctk.CTkFrame(self.main_container)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)
        self.content.grid_columnconfigure(0, weight=1)  # Adjust left column width
        self.content.grid_columnconfigure(1, weight=2)  # Center column expands
        self.content.grid_columnconfigure(2, weight=1)  # Right column
        
        # Left column - Players
        self.players_column = PlayersColumn(self.content)
        self.players_column.frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        # Center column - Game board
        self.center_column = ctk.CTkFrame(self.content)
        self.center_column.grid(row=0, column=1, sticky="nsew")
        
        # Game board view
        self.game_board = GameBoard(self.center_column)
        
        # Right column - Move history and settings
        self.right_column = ctk.CTkFrame(self.content, fg_color="transparent")
        self.right_column.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # Historique view
        self.historique_view = HistoriqueView(self.right_column)
        
    def run(self):
        """Start the application"""
        if hasattr(self, 'window'):
            self.window.mainloop()

    def update_theme(self):
        """Update the theme for all components"""
        # Implement theme update logic if needed
        pass

    def update(self, state: dict):
        """Update the view with new state"""
        self.players_column.update(state)
        if hasattr(self, 'game_board'):
            self.game_board.update(state)
        if hasattr(self, 'historique_view'):
            self.historique_view.update(state)

