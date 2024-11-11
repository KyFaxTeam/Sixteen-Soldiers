import customtkinter as ctk
import tkinter as tk
from views.base_view import BaseView
from PIL import Image
from models.assets.index import Assets

class HistoryView(BaseView):
    """View for game history and settings"""
    def __init__(self, master):
        super().__init__(master)
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
            font=("Poppins", 11, "bold")
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
            text=f"• {move_text}",
            anchor="w"
        )
        move_label.pack(side="left", padx=(5, 10))

        # Bouton de replay pour ce mouvement spécifique
        replay_button = ctk.CTkButton(
            move_frame,
            text="↻",
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

# Exemple de HistoriqueView corrigé
# class HistoriqueView(BaseView):
#     """View for game history and settings"""
#     def __init__(self, master):
#         super().__init__(master)
#         self.frame.configure(corner_radius=10)
#         self.frame.pack(fill="both", padx=10, pady=10)
        
#         # History Section
#         self.history_frame = ctk.CTkFrame(self.frame)
#         self.history_frame.pack(fill="both", expand=True, pady=(0, 20))
        
#         # Titre "Move History"
#         self.title_frame = ctk.CTkFrame(self.history_frame)
#         self.title_frame.pack(fill="both", padx=0, pady=10)
#         self.title = ctk.CTkLabel(
#             self.title_frame,
#             text="📜 History",
#             font=("Poppins", 11, "bold")
#         )
#         self.title.pack(pady=(5, 5))
        
#         # Container pour l'historique des mouvements
#         self.moves_container = ctk.CTkFrame(self.history_frame)
#         self.moves_container.pack(fill="both", expand=True)

#         # Utiliser `CTkTextbox` correctement avec `pack`
#         self.scrollable_frame = ctk.CTkTextbox(self.moves_container, height=350, width=200)
#         self.scrollable_frame.pack(fill="both", expand=True)

#         # Liste pour garder une référence aux mouvements
#         self.move_frames = []

#     def add_move(self, move_text: str, move_data=None):
#         """Ajouter un mouvement à l'historique avec un bouton de replay"""
#         move_frame = ctk.CTkFrame(self.scrollable_frame)
#         move_frame.pack(fill="x", padx=5, pady=2)
        
#         # Label pour le texte du mouvement
#         move_label = ctk.CTkLabel(move_frame, text=f"• {move_text}", anchor="w")
#         move_label.pack(side="left", padx=(5, 10))
        
#         # Bouton de replay pour ce mouvement spécifique
#         replay_button = ctk.CTkButton(
#             move_frame,
#             text="↻",
#             width=30,
#             height=30,
#             command=lambda: self.replay_move(move_data)
#         )
#         replay_button.pack(side="right", padx=5, pady=5)
        
#         # Ajouter à la liste des mouvements
#         self.move_frames.append({
#             "frame": move_frame,
#             "text": move_text,
#             "data": move_data
#         })
        
#         # Scroll vers le bas
#         self.scrollable_frame._parent_canvas.yview_moveto(1.0)
    
#     def replay_move(self, move_data):
#         """Rejouer un mouvement spécifique"""
#         if move_data:
#             print(f"Rejouer le mouvement: {move_data}")

#     def clear_history(self):
#         """Effacer tout l'historique"""
#         for move_frame_data in self.move_frames:
#             move_frame_data["frame"].destroy()
#         self.move_frames.clear()

# class HistoriqueView(BaseView):
#     """View for game history and settings"""
#     def __init__(self, master):
#         super().__init__(master)
#         self.frame.configure(corner_radius=10)
#         self.frame.pack(fill="both", padx=10, pady=10)
        
#         # History Section
#         self.history_frame = ctk.CTkFrame(self.frame)
#         self.history_frame.pack(fill="both", expand=True, pady=(0, 20))
        
#         # Titre "Move History"
#         self.title_frame = ctk.CTkFrame(self.history_frame)
#         self.title_frame.pack(fill="both", padx=0, pady=10)
#         self.title = ctk.CTkLabel(
#             self.title_frame,
#             text="📜 History",
#             font=("Poppins", 11, "bold")
#         )
#         self.title.pack(pady=(5, 5))
        
#         # Container pour l'historique des mouvements
#         self.moves_container = ctk.CTkFrame(self.history_frame)
#         self.moves_container.pack(fill="both", expand=True)

#         # Scrollable container
#         self.scrollable_frame = ctk.CTkTextbox(self.moves_container, height=350, width=200)
#         self.scrollable_frame.pack(fill="both", expand=True)
        
#         # # Scrollable container
#         # self.scrollable_frame = ctk.CTkScrollableFrame(self.moves_container)
#         # self.scrollable_frame.pack(fill="both", expand=True)
        
#         # Liste pour garder une référence aux mouvements
#         self.move_frames = []

#         # Scrollable history list
#         # self.history_text = ctk.CTkTextbox(
#         #     self.history_frame,
#         #     height=200,
#         #     width=200
#         # )
#         # self.history_text.pack(fill="both", expand=True)
        
#     def add_move(self, move_text: str, move_data=None):
#         """
#         Add a move to the history with a replay button
#         Args:
#             move_text: texte du mouvement (ex: "A5 => A3")
#             move_data: données nécessaires pour rejouer le mouvement
#         """
#         # Créer un frame pour chaque ligne
#         move_frame = ctk.CTkFrame(self.scrollable_frame)
#         move_frame.pack(fill="x", padx=5, pady=2)
        
#         # Label pour le texte du mouvement
#         move_label = ctk.CTkLabel(
#             move_frame,
#             text=f"• {move_text}",
#             anchor="w"
#         )
#         move_label.pack(side="left", padx=(5, 10))
        
#         # # Bouton de replay pour ce mouvement spécifique
#         # replay_button = ctk.CTkButton(
#         #     move_frame,
#         #     text="↻",
#         #     width=30,
#         #     height=30,
#         #     command=lambda: self.replay_move(move_data)
#         # )
#         # replay_button.pack(side="right", padx=5, pady=5)
        
#         # # Ajouter à la liste des mouvements
#         # self.move_frames.append({
#         #     "frame": move_frame,
#         #     "text": move_text,
#         #     "data": move_data
#         # })
        
#         # # Scroll vers le bas
#         # self.scrollable_frame._parent_canvas.yview_moveto(1.0)
    
#     def replay_move(self, move_data):
#         """
#         Rejouer un mouvement spécifique
#         Args:
#             move_data: données du mouvement à rejouer
#         """
#         if move_data:
#             print(f"Rejouer le mouvement: {move_data}")
#             # TODO: Implémenter la logique de replay
#             # Cette méthode devrait être connectée à votre GameBoard
#             pass

#     def clear_history(self):
#         """Effacer tout l'historique"""
#         for move_frame_data in self.move_frames:
#             move_frame_data["frame"].destroy()
#         self.move_frames.clear()

# class HistoriqueView(BaseView):
#     """View for game history and settings"""
#     def __init__(self, master):
#         super().__init__(master)
#         self.frame.pack(fill="both", padx=10, pady=10)

#         # History Section
#         self.history_frame = ctk.CTkFrame(self.frame)
#         self.history_frame.pack(fill="both", expand=True, pady=(0, 20))

#         # Titre "Move History"
#         self.title_frame = ctk.CTkFrame(self.history_frame)
#         self.title_frame.pack(fill="both", padx=5, pady=10)
#         self.title = ctk.CTkLabel(
#             self.title_frame,
#             text="  Move history",
#             font=("Poppins", 12, "bold")
#         )
#         self.title.pack(side="left")

#         # Scrollable container for history items
#         self.history_container = ctk.CTkFrame(self.history_frame)
#         self.history_container.pack(fill="both", expand=True)

#         # Create a Canvas and Scrollbar for scrolling
#         self.canvas = tk.Canvas(self.history_container)
#         self.scrollbar = ctk.CTkScrollbar(self.history_container, command=self.canvas.yview)
#         self.scrollbar.pack(side="right", fill="y")
#         self.canvas.pack(side="left", fill="both", expand=True)
#         self.canvas.configure(yscrollcommand=self.scrollbar.set)

#         # Frame inside the canvas to hold the history items
#         self.history_items_frame = ctk.CTkFrame(self.canvas)
#         self.canvas.create_window((0, 0), window=self.history_items_frame, anchor="nw")

#         # Track the number of moves to adjust the height of the canvas
#         self.history_items_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

#     def add_move(self, move_text: str):
#         """Add a move to the history with a replay button"""
#         # Frame for each history item
#         move_frame = ctk.CTkFrame(self.history_items_frame)
#         move_frame.pack(fill="x", padx=5, pady=2)

#         # Label for the move text
#         move_label = ctk.CTkLabel(move_frame, text=f"• {move_text}", anchor="w")
#         move_label.pack(side="left", fill="x", expand=True)

#         # Replay button for the move
#         replay_button = ctk.CTkButton(move_frame, text="↻", width=30, height=30, command=self.replay_move)
#         replay_button.pack(side="right")

#     def replay_move(self):
#         # Function to replay a move
#         print("Rejouer le mouvement")