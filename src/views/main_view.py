import customtkinter as ctk

from .home_view import HomeView
from views.base_view import BaseView
from views.game_board import GameBoard
from .historique_view import HistoriqueView
from views.after_game_view import AfterGameView
from views.historique_view import HistoriqueView
from views.Left_Column.players_column import PlayersColumn


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
        self.winner_data = {
            # "profile_img": "path/to/profile_image.png",  # Provide a real image path
            "team_pseudo": "Team A",
            "ai_name": "AI-1",
            "remaining_time": "25",
            "remaining_pawns": 3
        }


    def start_new_game(self):
        """Start a new game and switch to game board view"""
        self.home_view.hide()  # Hide the home screen
        self.window.geometry("1200x800")
        self.create_main_layout()  # Initialize main layout and sub-views
        

    def review_match(self):
        """Review a match and switch to history view"""
        self.home_view.hide()  # Hide the home screen
        self.window.geometry("1200x800")
        self.show_after_game_view()  # Initialize main layout and sub-views
        

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

    def check_game_end_condition(self):
        """Placeholder condition to trigger AfterGameView"""
        game_ended = True  # Replace this with real game-end logic
        if game_ended:
            self.show_after_game_view()

    def show_after_game_view(self):
        """Show AfterGameView with winner details"""
        self.after_game_view = AfterGameView(
            self.window,
            winner_data=self.winner_data,
            on_restart=self.restart_game,
            on_save=self.save_game
        )

    def restart_game(self):
        """Reset the game and return to HomeView"""
        # Close any existing AfterGameView if open
        if hasattr(self, 'after_game_view'):
            self.after_game_view.destroy()
            del self.after_game_view

        # Reset the main layout (clear current game views if necessary)
        if hasattr(self, 'main_container'):
            self.main_container.pack_forget()
            del self.main_container

        # Resize window for HomeView
        self.window.geometry("400x300")
        
        # Show HomeView again
        self.home_view.show()

    def save_game(self):
        """Save the game (implementation needed)"""
        print("Game saved.")
        
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

