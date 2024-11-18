import customtkinter as ctk
from views.base_view import BaseView

class HomeView(BaseView):
    """Home page of the application"""
    
    def __init__(self, master, on_new_game, on_review_match):
        super().__init__(master)
        self.frame = ctk.CTkFrame(self.master)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title label
        self.title_label = ctk.CTkLabel(self.frame, text="Bienvenue", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=20)
        
        # "Lancer un nouveau jeu" Button
        self.new_game_button = ctk.CTkButton(
            self.frame,
            text="Lancer un nouveau jeu",
            width=200,
            height=40,
            corner_radius=8,
            fg_color="#3B3B3B",
            hover_color="#131630",
            command=on_new_game
        )
        self.new_game_button.pack(pady=10)

        # "Revoir un match" Button
        self.review_match_button = ctk.CTkButton(
            self.frame,
            text="Revoir un match",
            width=200,
            height=40,
            corner_radius=8,
            fg_color="#3B3B3B",
            hover_color="#131630",
            command=on_review_match
        )
        self.review_match_button.pack(pady=10)

    def show(self):
        """Display the HomeView"""
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)

    def hide(self):
        """Hide the HomeView"""
        self.frame.pack_forget()
