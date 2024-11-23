import logging
from typing import Dict
import customtkinter as ctk

from views.base_view import BaseView


class MoveFormatter:
    def __init__(self, red_soldier_icon, blue_soldier_icon):
        """
        Initialise le formateur avec les icônes des soldats
        
        Args:
            red_soldier_icon: ImageTk.PhotoImage du soldat rouge
            blue_soldier_icon: ImageTk.PhotoImage du soldat bleu
        """
        self.red_soldier_icon = red_soldier_icon
        self.blue_soldier_icon = blue_soldier_icon

    def create_soldier_label(self, master, is_red: bool, value: int = None) -> ctk.CTkLabel:
        """
        Crée un label contenant l'icône du soldat et sa valeur
        """
        icon = self.red_soldier_icon if is_red else self.blue_soldier_icon
        label = ctk.CTkLabel(
            master,
            image=icon,
            text=f" {value}⭐" if value is not None else "",
            compound="left",
            font=ctk.CTkFont(size=10)
        )
        return label

class HistoryView(BaseView):
    def __init__(self, master, store=None):
        super().__init__(master)
        self.logger = logging.getLogger(__name__)
        self.frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.store = store

        self.logger = logging.getLogger(__name__)
        
        self.frame.configure(corner_radius=10)
        self.frame.pack(fill="both", padx=10, pady=10)
        
        # Ajouter le formateur de mouvement
        self.move_formatter = MoveFormatter(
            self.frame.red_soldier_icon,
            self.frame.blue_soldier_icon
        )

    def add_move(self, move_data):
        """Ajouter un mouvement à l'historique avec les icônes des soldats"""
        move_frame = ctk.CTkFrame(self.moves_container)
        move_frame.pack(fill="x", padx=5, pady=2)

        # Création du conteneur pour organiser les éléments horizontalement
        content_frame = ctk.CTkFrame(move_frame)
        content_frame.pack(fill="x", padx=5, pady=2)

        # Timestamp
        time_label = ctk.CTkLabel(
            content_frame,
            text=f"{move_data['timestamp'].strftime('%H:%M:%S')} |",
            font=ctk.CTkFont(size=10)
        )
        time_label.pack(side="left", padx=(2, 5))

        # Soldat qui effectue le mouvement
        moving_soldier = self.move_formatter.create_soldier_label(
            content_frame,
            is_red=True,  # Tu devras adapter ceci selon la logique de ton jeu
            value=move_data['soldier_value']
        )
        moving_soldier.pack(side="left", padx=(2, 5))

        # Mouvement
        move_label = ctk.CTkLabel(
            content_frame,
            text=f"🎯 {move_data['pos'][0]} → {move_data['pos'][1]}",
            font=ctk.CTkFont(size=10)
        )
        move_label.pack(side="left", padx=(2, 5))

        # Information de capture si présente
        if move_data['captured_soldier']:
            capture_icon = "👑" if move_data['capture_multiple'] else "⚔️"
            capture_label = ctk.CTkLabel(
                content_frame,
                text=f"{capture_icon} Capture:",
                font=ctk.CTkFont(size=10)
            )
            capture_label.pack(side="left", padx=(5, 2))

            # Soldat capturé
            captured_soldier = self.move_formatter.create_soldier_label(
                content_frame,
                is_red=False,  # Tu devras adapter ceci selon la logique de ton jeu
                value=move_data['captured_soldier']
            )
            captured_soldier.pack(side="left", padx=2)

        # Bouton de replay
        replay_button = ctk.CTkButton(
            content_frame,
            text="↺",
            font=ctk.CTkFont(size=10),
            width=30,
            height=30,
            command=lambda: self.replay_move(move_data)
        )
        replay_button.pack(side="right", padx=5)

        # Ajouter à la liste des mouvements
        self.move_frames.append({
            "frame": move_frame,
            "data": move_data
        })

        # Faire défiler vers le bas
        self.frame.after(100, self.scroll_to_bottom)

    def update(self, state):
        """Updates the move history by adding only new moves"""
        try:
            if 'history' not in state:
                self.logger.warning("No history in state")
                return
                
            current_moves = len(self.move_frames)
            history_moves = len(state['history'])
            
            if history_moves > current_moves:
                self.logger.info(f"Adding {history_moves - current_moves} new moves")
                for move in state['history'][current_moves:]:
                    self.add_move(move)
                                         
        except Exception as e:
            self.logger.error(f"Error in update: {str(e)}")

# class HistoryView(BaseView):
#     """View for game history and settings"""
#     def __init__(self, master, store=None):
#         super().__init__(master)
#         self.logger = logging.getLogger(__name__)
#         self.frame = ctk.CTkFrame(self.master, corner_radius=10)
#         self.store = store

#         self.logger = logging.getLogger(__name__)
        
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
#             font=ctk.CTkFont(size=11, weight="bold")
#         )
#         self.title.pack(pady=(5, 5))

#         # Container pour l'historique des mouvements
#         self.moves_container = ctk.CTkScrollableFrame(self.history_frame, height=300)
#         self.moves_container.pack(fill="both", expand=True)

#         # Liste pour garder une référence aux mouvements
#         self.move_frames = []

#     def add_move(self, move_text: str, move_data=None):
#         """Ajouter un mouvement à l'historique avec un bouton de replay"""
#         move_frame = ctk.CTkFrame(self.moves_container)
#         move_frame.pack(fill="x", padx=5, pady=2)

#         # Label pour le texte du mouvement
#         move_label = ctk.CTkLabel(
#             move_frame,
#             text=move_text,
#             font=ctk.CTkFont(size=10)
#         )
#         move_label.pack(side="left", padx=(5, 10))

#         # Bouton de replay pour ce mouvement spécifique
#         replay_button = ctk.CTkButton(
#             move_frame,
#             text="Replay",
#             font=ctk.CTkFont(size=10),
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

#         # Faire défiler vers le bas après un court délai pour s'assurer que le widget est mis à jour
#         self.frame.after(10000, self.scroll_to_bottom)

#     # def add_move(self, move_data: dict):
#     #     """Ajouter un mouvement à l'historique avec un bouton de replay"""
#     #     # Construire un texte enrichi
#     #     move_text = f"🕒 {move_data['timestamp']} | {move_data['pos'][0]} → {move_data['pos'][1]} | ⚔️ {move_data['soldier_value']} pts"

#     #     if move_data.get('captured_soldier'):
#     #         move_text += f" | 🎯 Capturé : {move_data['captured_soldier']}"

#     #     if move_data.get('capture_multiple'):
#     #         move_text += " | 💥 Multi-Capture"

#     #     # Création de l'interface
#     #     move_frame = ctk.CTkFrame(self.moves_container)
#     #     move_frame.pack(fill="x", padx=5, pady=2)

#     #     # Label pour le texte du mouvement
#     #     move_label = ctk.CTkLabel(
#     #         move_frame,
#     #         text=move_text,
#     #         font=ctk.CTkFont(size=10)
#     #     )
#     #     move_label.pack(side="left", padx=(5, 10))

#     #     # Bouton de replay pour ce mouvement spécifique
#     #     replay_button = ctk.CTkButton(
#     #         move_frame,
#     #         text="Replay",
#     #         font=ctk.CTkFont(size=10),
#     #         width=30,
#     #         height=30,
#     #         command=lambda: self.replay_move(move_data),
#     #         state="disabled"
            
        
#     #     )
#     #     replay_button.pack(side="right", padx=5, pady=5)

#     #     # Ajouter à la liste des mouvements
#     #     self.move_frames.append({
#     #         "frame": move_frame,
#     #         "text": move_text,
#     #         "data": move_data
#     #     })

#     #     # Faire défiler vers le bas après un court délai pour s'assurer que le widget est mis à jour
#     #     self.frame.after(100, self.scroll_to_bottom)

#     def format_move_text(self, move: Dict) -> str:
#         """
#         Formate le texte d'un mouvement pour l'affichage dans l'historique.
        
#         Args:
#             move: Dictionnaire contenant les informations du mouvement
            
#         Returns:
#             str: Texte formaté du mouvement
#         """
#         # Extraction des informations de base
#         from_pos, to_pos = move['pos']
        
#         # Formatage du texte de base du mouvement
#         base_text = f"🎯 {from_pos} → {to_pos}"
        
#         # Informations sur le soldat
#         soldier_info = f"[{move['soldier_value']}⭐]" if move['soldier_value'] else ""
        
#         # Informations sur la capture
#         capture_info = ""
#         if move['captured_soldier']:
#             capture_icon = "👑" if move['capture_multiple'] else "⚔️"
#             capture_info = f" {capture_icon} Capture: {move['captured_soldier']}"
            
#         # Timestamp formaté (optionnel, uniquement les minutes et secondes)
#         # time_str = move['timestamp'][-1].strftime("%H:%M:%S")
#         time_str = move['timestamp'][-1]
        
#         # Assemblage du texte final
#         # return f"{time_str} | {base_text} {soldier_info}{capture_info}"
#         return f"| {base_text} |"
    


#     def scroll_to_bottom(self):
#         """Défiler vers le bas de l'historique"""
#         self.moves_container._parent_canvas.yview_moveto(1.0)

#     def replay_move(self, move_data):
#         """Rejouer un mouvement spécifique"""
#         if move_data:
#             print(f"Rejouer le mouvement: {move_data}")



#     def update(self, state):
#         """Updates the move history by adding only new moves"""
#         try:
#             if 'history' not in state:
#                 self.logger.warning("No history in state")
#                 return
                
#             current_moves = len(self.move_frames)
#             history_moves = len(state['history'])
            
#             self.logger.debug(f"Current moves: {current_moves}, History moves: {history_moves}")
            
#             if history_moves > current_moves:
#                 self.logger.info(f"Adding {history_moves - current_moves} new moves")
#                 for move in state['history'][current_moves:]:
#                     # move_text = f"{move['pos'][0]} → {move['pos'][1]}"
#                     move_text = self.format_move_text(move)

#                     self.add_move(move_text, move)
                    
                    
#         except Exception as e:
#             self.logger.error(f"Error in update: {str(e)}")

    

# # If you have any images being used, ensure they're wrapped with ctk.CTkImage
# # Example:
# # image = Image.open(image_path)
# # ctk_image = ctk.CTkImage(image, size=(width, height))
# # some_widget.configure(image=ctk_image)