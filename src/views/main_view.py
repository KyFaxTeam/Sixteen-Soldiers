import customtkinter as ctk
from views.Left_Column.player_view import PlayerView
from views.game_board import GameBoard
from views.historique_view import HistoriqueView
from views.base_view import BaseView
from views.Left_Column.players_column import PlayersColumn

class MainView(BaseView):
    def __init__(self, master: any = None):
        # Configure main window if no master is provided
        if master is None:
            self.window = ctk.CTk()
            self.window.title("Sixteen Soldiers")
            self.window.geometry("1200x800")
            master = self.window
        
        # Create main container frame
        self.main_container = ctk.CTkFrame(master)
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
        # Assumons que GameBoard gère son propre affichage
        
        # Right column - Move history and settings
        self.right_column = ctk.CTkFrame(self.content, fg_color="transparent")
        self.right_column.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        
        # Historique view
        self.historique_view = HistoriqueView(self.right_column)
        # Assumons que HistoriqueView gère son propre affichage
        
        

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