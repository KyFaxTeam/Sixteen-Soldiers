
import customtkinter as ctk
from views.base_view import BaseView
from views.Left_Column.player_view import PlayerView
from utils.theme import ThemeManager

class PlayersColumn(BaseView):
    def __init__(self, master: any):
        super().__init__(master)
        
        self.frame.configure(fg_color="transparent")
        
        # Configure grid weights
        self.frame.grid_rowconfigure(0, weight=45)  # Player 1
        self.frame.grid_rowconfigure(1, weight=50)  # VS label
        self.frame.grid_rowconfigure(2, weight=45)  # Player 2
        self.frame.grid_columnconfigure(0, weight=1)

        # Player 1
        self.player1 = PlayerView(self.frame)
        self.player1.frame.grid(row=0, column=0, sticky="nsew")

        # VS Label container
        self.vs_container = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.vs_container.grid(row=1, column=0, sticky="nsew")
        self.vs_container.grid_columnconfigure(0, weight=1)
        self.vs_container.grid_rowconfigure(0, weight=1)
        
        self.vs_label = ctk.CTkLabel(
            self.vs_container,
            text="VS",
            font=ThemeManager.get_font("heading")
        )
        self.vs_label.grid(row=0, column=0)

        # Player 2
        self.player2 = PlayerView(self.frame)
        self.player2.frame.grid(row=2, column=0, sticky="nsew")

    def update(self, state: dict):
        """Update both players with new state"""
        player1_state = {'joueur': state.get('player1', {})}
        player2_state = {'joueur': state.get('player2', {})}
        
        self.player1.update(player1_state)
        self.player2.update(player2_state)

    def update_theme(self):
        """Update theme for all components"""
        self.player1.update_theme()
        self.player2.update_theme()
        # Update VS label if needed