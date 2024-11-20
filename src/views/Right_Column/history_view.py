import customtkinter as ctk
import tkinter as tk
from views.base_view import BaseView
from PIL import Image
from models.assets.index import Assets

class HistoryView(BaseView):
    """View for game history and settings"""
    def __init__(self, master, store=None):
        super().__init__(master)
        self.frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.store = store
        
        self.frame.configure(corner_radius=10)
        self.frame.pack(fill="both", padx=10, pady=10)

        # History Section
        self.history_frame = ctk.CTkFrame(self.frame)
        self.history_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Titre "Move History"
        self.title_frame = ctk.CTkFrame(self.history_frame)
        self.title_frame.pack(fill="both", padx=0, pady=10)
        self.title = ctk.CTkLabel(
            self.title_frame,
            text="📜 History",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.title.pack(pady=(5, 5))

        # Container pour l'historique des mouvements
        self.moves_container = ctk.CTkScrollableFrame(self.history_frame, height=350)
        self.moves_container.pack(fill="both", expand=True)

        # Liste pour garder une référence aux mouvements
        self.move_frames = []

    def add_move(self, move_text: str, move_data=None):
        """Ajouter un mouvement à l'historique avec un bouton de replay"""
        move_frame = ctk.CTkFrame(self.moves_container)
        move_frame.pack(fill="x", padx=5, pady=2)

        # Label pour le texte du mouvement
        move_label = ctk.CTkLabel(
            move_frame,
            text=move_text,
            font=ctk.CTkFont(size=10)
        )
        move_label.pack(side="left", padx=(5, 10))

        # Bouton de replay pour ce mouvement spécifique
        replay_button = ctk.CTkButton(
            move_frame,
            text="Replay",
            font=ctk.CTkFont(size=10),
            width=30,
            height=30,
            command=lambda: self.replay_move(move_data)
        )
        replay_button.pack(side="right", padx=5, pady=5)

        # Ajouter à la liste des mouvements
        self.move_frames.append({
            "frame": move_frame,
            "text": move_text,
            "data": move_data
        })

        # Faire défiler vers le bas après un court délai pour s'assurer que le widget est mis à jour
        self.frame.after(10000, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """Défiler vers le bas de l'historique"""
        self.moves_container._parent_canvas.yview_moveto(1.0)

    def replay_move(self, move_data):
        """Rejouer un mouvement spécifique"""
        if move_data:
            print(f"Rejouer le mouvement: {move_data}")

    def clear_history(self):
        """Effacer tout l'historique"""
        for move_frame_data in self.move_frames:
            move_frame_data["frame"].destroy()
        self.move_frames.clear()

    def update(self, state):
        """Updates the move history based on the state"""
        if 'history' in state:
            self.refresh_history(state['move_history'])

    def refresh_history(self, move_history):
        """Clears and repopulates the history view"""
        # Clear existing history
        self.clear_history()
        # Populate with new move history
        for move in move_history:
            self.add_move(move['description'], move)

# If you have any images being used, ensure they're wrapped with ctk.CTkImage
# Example:
# image = Image.open(image_path)
# ctk_image = ctk.CTkImage(image, size=(width, height))
# some_widget.configure(image=ctk_image)