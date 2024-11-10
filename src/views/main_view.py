import customtkinter as ctk
from models.sauvegarde import Sauvegarde
from views.base_view import BaseView
from views.game_board import GameBoard
from views.sauvegarde_view import SauvegardeView
from .joueur_view import JoueurView
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

        # Initialize variables for sub-views; actual frames will be created later
        self.left_panel = None
        self.center_panel = None
        self.right_panel = None
        self.joueur_view = None
        self.plateau_view = None
        self.historique_view = None
        # Uncomment if using Sauvegarde
        # self.sauvegarde = Sauvegarde()

    def start_new_game(self):
        """Start a new game and switch to game board view"""
        self.home_view.hide()  # Hide the home screen
        self.window.geometry("1200x800")
        self.create_main_layout()  # Initialize main layout and sub-views
        self.plateau_view._move_soldier_in_bord(0, (200, 200))

    def review_match(self):
        """Review a match and switch to history view"""
        self.home_view.hide()  # Hide the home screen
        self.window.geometry("1200x800")
        self.create_main_layout()  # Initialize main layout and sub-views
        self.plateau_view._move_soldier_in_bord(0, (200, 200))

    def create_main_layout(self):
        """Create the main layout and initialize sub-views only when needed"""
        if not self.left_panel:  # Check if layout has already been created
            # Create main layout
            self.left_panel = ctk.CTkFrame(self.window, width=300)
            self.left_panel.pack(side="left", fill="y", padx=10, pady=10)
            
            self.center_panel = ctk.CTkFrame(self.window)
            self.center_panel.pack(side="left", expand=True, fill="both", padx=10, pady=10)
            
            self.right_panel = ctk.CTkFrame(self.window, width=300)
            self.right_panel.pack(side="right", fill="y", padx=10, pady=10)
            
            # Initialize sub-views within main layout
            self.joueur_view = JoueurView(self.left_panel)
            self.plateau_view = GameBoard(self.center_panel)
            self.historique_view = HistoriqueView(self.right_panel)
            # Uncomment if using SauvegardeView
            # self.sauvegarde_view = SauvegardeView(self.left_panel, self.plateau_view, self.joueur_view, self.sauvegarde)

    def run(self):
        """Start the application"""
        self.window.mainloop()
