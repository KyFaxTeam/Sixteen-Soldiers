import logging
from typing import Dict
import customtkinter as ctk
from PIL import Image, ImageTk

from models.assets.index import Assets
from utils.const import SOLDIER_SIZE_HISTORY, Soldier, EMOJIS_SIZE
from utils.history_utils import get_last_move, is_equals
from views.base_view import BaseView


## Je voudrais faire de sorte qu'on s'assure que le jeu soit en pause 
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
            # ⭐
            text=f"{value}" if value is not None else "",
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
        

        self.frame.red_soldier_icon = ctk.CTkImage(
            light_image=Image.open(Assets.img_red_soldier),
            dark_image=Image.open(Assets.img_red_soldier),
            size=SOLDIER_SIZE_HISTORY
        )
        self.frame.blue_soldier_icon = ctk.CTkImage(
            light_image=Image.open(Assets.img_blue_soldier),
            dark_image=Image.open(Assets.img_blue_soldier),
            size=SOLDIER_SIZE_HISTORY
    )
        
        # Ajouter le formateur de mouvement
        self.move_formatter = MoveFormatter(
            self.frame.red_soldier_icon,
            self.frame.blue_soldier_icon
        )


        # History Section
        self.history_frame = ctk.CTkFrame(self.frame)
        self.history_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Titre "Move History"
        self.title_frame = ctk.CTkFrame(self.history_frame)
        self.title_frame.pack(fill="both", padx=0, pady=10)
        #self.title_frame.history_icon = ImageTk.PhotoImage(Image.open(Assets.icon_history_collante).resize(EMOJIS_SIZE))
        self.title_frame.history_icon = ctk.CTkImage(
            light_image=Image.open(Assets.icon_history_collante),
            dark_image=Image.open(Assets.icon_history_collante),
            size=EMOJIS_SIZE
)

        self.title = ctk.CTkLabel(
            self.title_frame,
            image=self.title_frame.history_icon,
            text=" History",
            compound="left",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        self.title.pack(pady=(5, 5))

        # Container pour l'historique des mouvements
        self.moves_container = ctk.CTkScrollableFrame(self.history_frame, height=300)
        self.moves_container.pack(fill="both", expand=True)

        # Liste pour garder une référence aux mouvements
        self.move_frames = []

        self.previous_move = None


    def add_move(self, move_data, state):
        """Ajouter un mouvement à l'historique avec les icônes des soldats"""
        # move_frame = ctk.CTkFrame(self.moves_container)
        # move_frame.pack(fill="x", padx=5, pady=2)

        # Création du conteneur pour organiser les éléments horizontalement
        # content_frame = ctk.CTkFrame(move_frame)
        content_frame = ctk.CTkFrame(self.moves_container)
        content_frame.pack(fill="x", padx=8, pady=5)

        content_frame.cible = ImageTk.PhotoImage(Image.open(Assets.cible).resize((12, 12)))
        content_frame.approuve = ImageTk.PhotoImage(Image.open(Assets.approuve).resize((18, 18)))


        # Soldat qui effectue le mouvement
        moving_soldier = self.move_formatter.create_soldier_label(
            content_frame,
            is_red=move_data['soldier_value'] == Soldier.RED, 
        )
        moving_soldier.pack(side="left", padx=(5, 5), pady=2)

        # Timestamp
        time_text = f"{move_data['timestamp'][-1] * 1e3:.3f} ms"
        time_label = ctk.CTkLabel(
            content_frame,
            # text=f"{move_data['timestamp'].strftime('%H:%M:%S')} |",
            text=f"{time_text.ljust(10)}  |",
            font=ctk.CTkFont(size=10)
        )
        time_label.pack(side="left", padx=(2, 5))


        # Mouvement
        move_label = ctk.CTkLabel(
            content_frame,
            image=content_frame.cible,
            # text=f"🎯 {move_data['pos'][0]} → {move_data['pos'][1]}",
            text=f" {move_data['pos'][-2]} → {move_data['pos'][-1]}",
            font=ctk.CTkFont(size=10),
            compound="left"
        )
        move_label.pack(side="left", padx=(2, 5))

        # Information de capture si présente
        if move_data['captured_soldier']:
            # capture_icon = "👑" if move_data['capture_multiple'] else "⚔️"
            capture_label = ctk.CTkLabel(
                content_frame,
                image=content_frame.approuve,
                # text=f"| {capture_icon} Capture:",
                text="| Capture:",
                font=ctk.CTkFont(size=10),
                compound="left"
            )
            capture_label.pack(side="left", padx=(5, 2))

            # Soldat capturé
            captured_soldier = self.move_formatter.create_soldier_label(
                content_frame,
                is_red=move_data['soldier_value'] != Soldier.RED,  
                value=move_data['captured_soldier'][-1]
            )
            captured_soldier.pack(side="left", padx=2)

        # Bouton de replay
        replay_button = ctk.CTkButton(
            content_frame,
            text="↺",
            font=ctk.CTkFont(size=10),
            width=25,
            height=25,
            command=lambda: self.replay_move(move_data, state),
            state="disabled" if not state['is_game_paused'] else "normal",
            
        )
        replay_button.pack(side="right", padx=5)

        # Ajouter à la liste des mouvements
        self.move_frames.append({
            # "frame": move_frame,
            "data": move_data
        })

        # Faire défiler vers le bas
        self.frame.after(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        """Défiler vers le bas de l'historique"""
        self.moves_container._parent_canvas.yview_moveto(1.0)

    def replay_move(self, move_data, state):
        """Rejouer un mouvement spécifique"""
        if move_data and state['is_game_paused']:
            print(f"Rejouer le mouvement: {move_data}")


    def update(self, state):
        """Updates the move history by adding only new moves"""
        if not state['is_game_started'] or state['is_game_over'] or state['is_game_paused']: 
            return
        try:
            if 'history' not in state or state['history'] == []:
                self.logger.warning("No history in state")
                return

                
            # current_moves = len(self.move_frames)
            # history_moves = len(state['history'])
            
            # if history_moves > current_moves:
            #     self.logger.info(f"Adding {history_moves - current_moves} new moves")
            #     for move in state['history'][current_moves:]:
            #         self.add_move(move, state)
            # else : 
            #     print(" ***************************************************len(current_moves ): ", current_moves)
            #     print(" ***************************************************len(history ): ", history_moves)
            
            move = state["history"][-1]
            if not is_equals(self.previous_move, move) : 
                self.add_move(move, state)   

            self.previous_move = state['history'][-1]      

        except Exception as e:
            self.logger.error(f"Error in update: {str(e)}")