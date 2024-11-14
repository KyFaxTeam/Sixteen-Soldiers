import customtkinter as ctk
from views.base_view import BaseView
from views.Left_Column.player_view import PlayerView
# Removed ThemeManager import
# from utils.theme_manager import ThemeManager

class PlayersColumn(BaseView):
    def __init__(self, master: any):
        super().__init__(master)
        
        self.frame.configure(fg_color="transparent")
        
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=40)
        self.frame.grid_rowconfigure(1, weight=30)
        self.frame.grid_rowconfigure(2, weight=40)
        self.frame.grid_columnconfigure(0, weight=1)

        # Player 1
        self.player1 = PlayerView(self.frame)
        self.player1.frame.grid(row=0, column=0, sticky="nsew", pady=(5, 0))

        # VS Label container with transparent background
        self.vs_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.vs_container.grid(row=1, column=0, sticky="nsew")
        self.vs_container.grid_columnconfigure(0, weight=1)
        self.vs_container.grid_rowconfigure(0, weight=1)
        
        self.vs_label = ctk.CTkLabel(
            self.vs_container,
            text="VS",
            font=("Poppins", 16, "bold")  # Set font directly
        )
        self.vs_label.grid(row=0, column=0)

        # Player 2
        self.player2 = PlayerView(self.frame)
        self.player2.frame.grid(row=2, column=0, sticky="nsew", pady=(0, 5))

    def update(self, state: dict):
        """Update both players with new state"""
        player1_state = {'joueur': state.get('player1', {})}
        player2_state = {'joueur': state.get('player2', {})}
        
        self.player1.update(player1_state)
        self.player2.update(player2_state)