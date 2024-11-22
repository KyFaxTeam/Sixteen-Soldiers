import logging
import customtkinter as ctk

from views.base_view import BaseView


class HistoryView(BaseView):
    """View for game history and settings"""
    def __init__(self, master, store=None):
        super().__init__(master)
        self.logger = logging.getLogger(__name__)
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



    def update(self, state):
        """Updates the move history by adding only new moves"""
        try:
            
            if 'history' not in state:
                self.logger.warning("No history in state")
                return
                
            current_moves = len(self.move_frames)
            history_moves = len(state['history'])
            
            self.logger.debug(f"Current moves: {current_moves}, History moves: {history_moves}")
            
            if history_moves > current_moves:
                self.logger.info(f"Adding {history_moves - current_moves} new moves")
                for move in state['history'][current_moves:]:
                    move_text = f"{move['pos'][0]} → {move['pos'][1]}"

                    self.add_move(move_text, move)
                    
        except Exception as e:
            self.logger.error(f"Error in update: {str(e)}")

    

# If you have any images being used, ensure they're wrapped with ctk.CTkImage
# Example:
# image = Image.open(image_path)
# ctk_image = ctk.CTkImage(image, size=(width, height))
# some_widget.configure(image=ctk_image)