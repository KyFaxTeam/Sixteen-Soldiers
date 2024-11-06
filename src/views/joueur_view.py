import customtkinter as ctk
from views.base_view import BaseView

class JoueurView(BaseView):
    """View for player information"""
    def __init__(self, master):
        super().__init__(master)
        self.frame.pack(fill="both", padx=10, pady=10)
        
        # Player information
        self.player_frame = ctk.CTkFrame(self.frame)
        self.player_frame.pack(fill="x", pady=5)
        
        self.current_player_label = ctk.CTkLabel(
            self.player_frame,
            text="Current Player: Red"
        )
        self.current_player_label.pack(pady=5)
        
        # Score information
        self.score_label = ctk.CTkLabel(
            self.player_frame,
            text="Soldiers Remaining\nRed: 8  Green: 8"
        )
        self.score_label.pack(pady=5)

