import customtkinter as ctk
from views.base_view import BaseView


class HistoriqueView(BaseView):
    """View for game history"""
    def __init__(self, master):
        super().__init__(master)
        self.frame.pack(fill="both", padx=10, pady=10)
        
        # History title
        self.title = ctk.CTkLabel(
            self.frame,
            text="Move History"
        )
        self.title.pack(pady=5)
        
        # Scrollable history list
        self.history_text = ctk.CTkTextbox(
            self.frame,
            height=400,
            width=250
        )
        self.history_text.pack(fill="both", expand=True)
        
    def add_move(self, move_text: str):
        """Add a move to the history"""
        self.history_text.insert("end", f"{move_text}\n")
        self.history_text.see("end")