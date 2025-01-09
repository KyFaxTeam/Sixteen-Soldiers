import time
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import screeninfo
from src.models.assets.index import Assets
from src.utils.audio import Sounds
from src.utils.const import  LINE_THICKNESS, PADDING, SOLDIER_SIZE, resolution, Soldier
from src.utils.game_utils import GameRunner
from src.views.base_view import BaseView
from src.utils.board_utils import BoardUtils  
from src.utils.history_utils import get_last_move, is_equals  
import logging
import traceback
from src.store.store import Store
from enum import Enum

pad_board = {
    "HD": 5,
    "Full HD": 10,
    "HD+": 10,
    "Quad HD": 10,
    "4K Ultra HD": 10
}


class GameBoard(BaseView):
    
    def __init__(self, master, store: Store, game_runner: GameRunner):
        # store.state['board']
        super().__init__(master)
        self.store = store
        self.game_runner = game_runner  # Stocke la référence au GameRunner

        self.button_frame = ctk.CTkFrame(self.frame, bg_color="transparent")
        self.button_frame.pack(pady= (pad_board[resolution], 1))
        self.create_canvas()

        self.store.subscribe_theme(self.change_canvas_color)
        
        self.red_soldiers = []
        self.blue_soldiers = []
        self.previous_move = None

        self.sounds = Sounds()
        self._init_board()
        
        self.logger = logging.getLogger(__name__)

    def _init_board(self):
        """Initializes the game board by drawing the board, pieces, playing background music, and setting up the decor."""
        self.__draw_board()
        self._draw_pieces()
        self._add_button()
        self.sounds.background_music()
        
    def create_canvas(self):
        """Crée un canvas pour le plateau de jeu."""
        # Get resolution of the screen

        screen_info = screeninfo.get_monitors()[0]
        
        
        screen_height = screen_info.height
        

        # Calculer le self.GAP_ en fonction de la résolution de l'écran
        self.GAP_ = int(screen_height /12)
        
        mode = ctk.get_appearance_mode().lower()
        bg_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"][0 if mode == "light" else 1]

        canvas_frame = ctk.CTkFrame(
            self.frame, 
            width=4 * self.GAP_ + 2 * PADDING , 
            height=8 * self.GAP_ + 2 * PADDING,
            corner_radius=15,  # Coins arrondis avec CustomTkinter
        )
        canvas_frame.pack(pady=(pad_board[resolution], 0), expand=True, fill = "both")

        # Créer un canvas pour le plateau de jeu
        self.canvas = tk.Canvas(canvas_frame, width= 4 * self.GAP_ + 2 * PADDING , height= 8 * self.GAP_ + 2 * PADDING , bg =bg_color, highlightthickness=0, highlightbackground="#424977")
        self.canvas.pack(padx=(35,35), pady=(0, pad_board[resolution]), expand=True, fill ="both")

    def __draw_board(self):
       
        # Dessiner le plateau de jeu (lignes pour relier les positions)
        lines = [
            # Horizontales
            [(PADDING, PADDING), (PADDING + 4 * self.GAP_, PADDING)],
            [(PADDING + self.GAP_, PADDING + self.GAP_), (PADDING + 3 * self.GAP_, PADDING + self.GAP_)],
            
            [(PADDING, PADDING + 2 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 2 * self.GAP_)],
            [(PADDING, PADDING + 3 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 3 * self.GAP_)],
            [(PADDING, PADDING + 4 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 4 * self.GAP_)],
            [(PADDING, PADDING + 5 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 5 * self.GAP_)],
            [(PADDING, PADDING + 6 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 6 * self.GAP_)],
          
            [(PADDING + self.GAP_, PADDING + 7 * self.GAP_), (PADDING + 3 * self.GAP_, PADDING + 7 * self.GAP_)],
            [(PADDING, PADDING + 8 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 8 * self.GAP_)],
            
            # Verticales
            [(PADDING , PADDING + 2 * self.GAP_), (PADDING, PADDING + 6 * self.GAP_)],
            [(PADDING + self.GAP_, PADDING + 2 * self.GAP_), (PADDING + self.GAP_, PADDING + 6 * self.GAP_)],
            
            [(PADDING + 2* self.GAP_, PADDING), (PADDING + 2* self.GAP_, PADDING + 8 * self.GAP_)],
            
            [(PADDING + 3 * self.GAP_, PADDING + 2 * self.GAP_), (PADDING + 3 * self.GAP_, PADDING + 6 * self.GAP_)],
            [(PADDING + 4 * self.GAP_, PADDING + 2 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 6 * self.GAP_)],

            # diagonales
            [(PADDING, PADDING), (PADDING + 4 * self.GAP_, PADDING + 4 * self.GAP_)],
            [(PADDING + 4 * self.GAP_, PADDING), (PADDING, PADDING + 4 * self.GAP_)],
            
            [(PADDING, PADDING + 4 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 8 * self.GAP_)],
            [(PADDING + 4 * self.GAP_, PADDING + 4 * self.GAP_), (PADDING, PADDING + 8 * self.GAP_)],
            
            [(PADDING, PADDING + 2 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 6 * self.GAP_)],
            [(PADDING, PADDING + 6 * self.GAP_), (PADDING + 4 * self.GAP_, PADDING + 2 * self.GAP_)],
        ]
        
        
        for line in lines:
            self.canvas.create_line(line[0], line[1], width=LINE_THICKNESS, fill="black")
              
    def _draw_pieces(self):
        '''Dessine les pions sur le plateau de jeu'''
        self.frame.red_soldier_icon = ImageTk.PhotoImage(Image.open(Assets.img_red_soldier).resize(SOLDIER_SIZE))
        self.frame.blue_soldier_icon = ImageTk.PhotoImage(Image.open(Assets.img_blue_soldier).resize(SOLDIER_SIZE))
        
        # Liste des positions de départ pour 16 pions rouges et verts
        positions_soldier_A  = []
        positions_soldier_B = []
        
        for col in range(6):
            for lin in range(4):
                if col == 1 and lin == 0 or col == 3 and lin == 0 or  col == 0 and lin == 1 or col == 4 and lin == 1:
                    continue
                # Ajouter les positions des pions rouges et bleus
                positions_soldier_A.append((PADDING + col * self.GAP_, PADDING + lin * self.GAP_))
                positions_soldier_B.append((PADDING + (4 - col) * self.GAP_, PADDING + (8 - lin) * self.GAP_))

    
        for soldierA, soldierB in zip(positions_soldier_A, positions_soldier_B):
            
            red_piece = self.canvas.create_image(soldierA[0], soldierA[1], image=self.frame.red_soldier_icon)
            self.red_soldiers.append(red_piece)
                
            blue_piece = self.canvas.create_image(soldierB[0], soldierB[1], image=self.frame.blue_soldier_icon)
            self.blue_soldiers.append(blue_piece)
            
            
            self.canvas.update_idletasks()
        
        mode = ctk.get_appearance_mode().lower()
        text_color = ctk.ThemeManager.theme["CTkTextbox"]["text_color"][0 if mode == "light" else 1]
            
        # Annotation des coordonnées de chaque pion
        for i in range(9):
            custom_font = ctk.CTkFont(family=Assets.font_montserrat, size=15)
            if i < 5:
                x = PADDING + i * self.GAP_
                self.canvas.create_text(x, 8*self.GAP_ + 2 * PADDING -10 , text=str(i + 1), font=custom_font, fill=text_color, anchor="center", tags="optional_tag")
            y = PADDING + i * self.GAP_
            self.canvas.create_text(10, y, text=chr(ord('a') + i), font=custom_font, fill=text_color, anchor="center", tags="optional_tag")
        
    def _add_button(self):
        """Initialise les boutons de contrôle"""
        # Play button
        self.play_pause_button = ctk.CTkButton(
                    master=self.button_frame, text='Play' if self.store.get_state().get("game_mode") == "game" else 'Replay',
                    image=ctk.CTkImage(
                        light_image=Image.open(Assets.icon_play), size=(20, 20)),
                    compound="left", command=self.toggle_play_pause, width=120, height=32,
                    corner_radius=8, anchor="center"
                )
        
        self.reset_button = ctk.CTkButton(
                    master=self.button_frame, text='Restart',
                    image=ctk.CTkImage(
                        light_image=Image.open(Assets.icon_reset), size=(20, 20)),
                    compound="left", command=self.reset_game, width=120, height=32,
                    corner_radius=8, anchor="center"
                )   
        
        self.play_pause_button.pack(side="left", padx=10, pady=5)
        self.reset_button.pack(side="left", padx=10, pady=5)

    def _move_soldier_in_board(self, soldier_id: int, target: tuple, timestamp: float = 0.5):
        self.canvas.update_idletasks()

        if soldier_id is None:
            self.logger.error("Error: Soldier not found")
            return
        
        board_params = self.store.game_speed.get_board_speed(timestamp) 
        steps = board_params['steps']
        delay = board_params['delay']

        # Récupérer les coordonnées actuelles
        coords = self.canvas.coords(soldier_id)
        current_x, current_y = coords
        target_x, target_y = target

        # Calculate movement increments
        dx = (target_x - current_x) / steps
        dy = (target_y - current_y) / steps

        def step_move(step):
            if step < steps:
                self.canvas.move(soldier_id, dx, dy)
                self.frame.after(delay, lambda: step_move(step + 1))
            else:
                # Final position adjustment
                self.canvas.coords(soldier_id, target_x, target_y)
        
        step_move(0)

    def _get_piece_id(self, position: tuple, soldier_value: Soldier):
        """Retourne l'ID du soldat à partir de sa position et du type de soldat (RED ou BLUE)."""
        soldiers = self.red_soldiers if soldier_value == Soldier.RED else self.blue_soldiers
        for piece in soldiers:
            coords = self.canvas.coords(piece)
            if tuple(coords) == position:
                return piece
        self.logger.error(f"No soldier found at position {position} for {soldier_value.name}")
        return None
        
    def _make_action(self, move: dict) :

        """Effectue une action sur le plateau de jeu."""
        from_pos = move["pos"][-2] if len(move["pos"]) >= 2 else move["pos"][0]
        to_pos = move["pos"][-1]
        player = move["soldier_value"]
        timestamp = move["timestamp"][-1]

        # Conversion en coordonnées du plateau
        from_coords = BoardUtils.algebraic_to_gameboard(from_pos, gap=self.GAP_)
        #to_coords = BoardUtils.algebraic_to_gameboard(to_pos, gap=self.GAP_)
        

        soldier_id = self._get_piece_id(position=from_coords, soldier_value=move["soldier_value"])
        if soldier_id is None:
            self.logger.error(f"No soldier found at position {from_coords} for player {player}")
            return 

        
        # Faire le mouvement 
        self._move_soldier_in_board(
            soldier_id, 
            BoardUtils.algebraic_to_gameboard(to_pos, gap=self.GAP_),
            timestamp = timestamp
        )
        # Préparer l'ID du pion capturé
        captured_id = None
        if move.get("captured_soldier") is not None:
            captured_soldier = move["captured_soldier"][-1]
            captured_pos = BoardUtils.algebraic_to_gameboard(captured_soldier, gap=self.GAP_)
            captured_id = self._get_piece_id(
                position=captured_pos, 
                soldier_value=Soldier.BLUE if move["soldier_value"] == Soldier.RED else Soldier.RED
            )
            
            self.sounds.kill_soldier()
            self.canvas.delete(captured_id)
        

        
    def update(self, state):
        """ Updates the board based on the new state """
        
        if state.get("is_game_leaved"):
            return
        
        if state.get("is_game_over"):
            self.previous_move = None
            # self.logger.info("Game is over - Change the text on play button")
            # self.play_pause_button.configure(state="disabled")
            self.play_pause_button.configure(
                image=ctk.CTkImage(
                    light_image=Image.open(Assets.icon_play), size=(20, 20)),
                text="Play" if state.get("game_mode") == "game" else "Replay"
            )
            self.reset_button.configure(state="normal")
            return
        
        if not state.get("is_game_started"):
            return
        
        try:
            last_move = get_last_move(state)
            if last_move is None :
                return
            if not is_equals(last_move, self.previous_move):
                # self.logger.info(f"Processing new move: {last_move}")
                try:
                    self._make_action(last_move.to_dict())
                except Exception as e:
                    self.logger.error(f"Error in _make_action: {e}")
                    self.logger.error(traceback.format_exc())

                self.previous_move = last_move

            self.canvas.update_idletasks()
        except Exception as e:
            self.logger.error(f"Error in update: {e}")
            self.logger.error(traceback.format_exc())

    def change_canvas_color(self, mode: str):
        """Change la couleur de fond du canvas."""
        self.canvas.configure(
            bg=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][
                0 if mode == "light" else 1
            ]
        )
        mode = ctk.get_appearance_mode().lower()
        text_color = ctk.ThemeManager.theme["CTkTextbox"]["text_color"][0 if mode == "light" else 1]
            
        # Annotation des coordonnées de chaque pion
        for i in range(9):
            custom_font = ctk.CTkFont(family=Assets.font_montserrat, size=15)
            if i < 5:
                x = PADDING + i * self.GAP_
                self.canvas.create_text(x, 8*self.GAP_ + 2 * PADDING -10 , text=str(i + 1), font=custom_font, fill=text_color, anchor="center", tags="optional_tag")
            y = PADDING + i * self.GAP_
            self.canvas.create_text(10, y, text=chr(ord('a') + i), font=custom_font, fill=text_color, anchor="center", tags="optional_tag")

    def toggle_play_pause(self):
        """Toggle the play/pause state of the game"""
        current_state = self.store.get_state()
        
        if not current_state.get("is_game_started"):
            if self.game_runner.start():
                self._update_button_state(True)
            return

        is_paused = current_state.get('is_game_paused', False)
        self.store.dispatch({'type': 'RESUME_GAME' if is_paused else 'PAUSE_GAME'})
        # On récupère l'état mis à jour après le dispatch
        updated_state = self.store.get_state()
        self._update_button_state(not updated_state.get('is_game_paused', False))

    def _update_button_state(self, is_playing: bool):
        """Met à jour l'état des boutons"""
        self.play_pause_button.configure(
            text="Pause" if is_playing else "Resume",
            image=ctk.CTkImage(
                light_image=Image.open(
                    Assets.icon_pause if is_playing else Assets.icon_play
                ), 
                size=(20, 20)
            )
        )
        self.reset_button.configure(state="disabled" if is_playing else "normal")

    def reset_game(self):
        """Reset the game board"""

        if self.store.get_state().get("is_game_leaved"):
            return
        else :
            self.store.dispatch({"type": "RESET_GAME"})

            
    def cleanup(self):
        """Nettoie le plateau de jeu"""
        self.canvas.delete("all")
        self.red_soldiers = []
        self.blue_soldiers = []
        self.previous_move = None

        
        self.play_pause_button.configure(state="normal")
        self.reset_button.configure(state="normal")
        self.__draw_board()
        self._draw_pieces()
