import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from models.assets.index import Assets
from utils.audio import Sounds
from utils.const import GAP, LINE_THICKNESS, PADDING, SOLDIER_SIZE
from utils.game_runner import GameRunner
from views.base_view import BaseView


class GameBoard(BaseView):
    
    def __init__(self, master, store, agent1, agent2):
        # store.state['board']
        super().__init__(master)
        self.store = store
        self.agent1 = agent1
        self.agent2 = agent2
        self.frame.pack(expand=True, fill="both")
        
        # Créer un conteneur pour le canvas et les boutons
        self.main_container = ctk.CTkFrame(self.frame)
        self.main_container.pack(expand=True, fill="both")
        
        
        self.canvas = tk.Canvas(self.main_container, 
                                    width= 4 * GAP + 2 * PADDING, 
                                    height= 8 * GAP + 2 * PADDING, 
                                    bg="#2d2d2e")

        # Créer un frame pour les boutons (en haut)
        self.button_frame = ctk.CTkFrame(self.main_container)
        self.button_frame.pack( padx=5, pady=5)
        
        self.canvas.pack()
        self.red_soldiers = []
        self.blue_soldiers = []
        self.sounds = Sounds()
        self._init_board()
        
        # Ajoutez un bouton "Play"
        self.play_button = ctk.CTkButton(self.button_frame, text="Play", command=self.start_game)
        self.play_button.pack()
        self.current_positions = {}  # Stocke les positions actuelles des pièces
        
    def _init_board(self):
        self.__draw_board()
        self._draw_pieces()
        self.sounds.background_music()
        self._decor()

    def __draw_board(self):
       
        # Dessiner le plateau de jeu (lignes pour relier les positions)
        lines = [
            # Horizontales
            [(PADDING, PADDING), (PADDING + 4 * GAP, PADDING)],
            [(PADDING + GAP, PADDING + GAP), (PADDING + 3 * GAP, PADDING + GAP)],
            
            [(PADDING, PADDING + 2 * GAP), (PADDING + 4 * GAP, PADDING + 2 * GAP)],
            [(PADDING, PADDING + 3 * GAP), (PADDING + 4 * GAP, PADDING + 3 * GAP)],
            [(PADDING, PADDING + 4 * GAP), (PADDING + 4 * GAP, PADDING + 4 * GAP)],
            [(PADDING, PADDING + 5 * GAP), (PADDING + 4 * GAP, PADDING + 5 * GAP)],
            [(PADDING, PADDING + 6 * GAP), (PADDING + 4 * GAP, PADDING + 6 * GAP)],
          
            [(PADDING + GAP, PADDING + 7 * GAP), (PADDING + 3 * GAP, PADDING + 7 * GAP)],
            [(PADDING, PADDING + 8 * GAP), (PADDING + 4 * GAP, PADDING + 8 * GAP)],
            
            # Verticales
            [(PADDING , PADDING + 2 * GAP), (PADDING, PADDING + 6 * GAP)],
            [(PADDING + GAP, PADDING + 2 * GAP), (PADDING + GAP, PADDING + 6 * GAP)],
            
            [(PADDING + 2* GAP, PADDING), (PADDING + 2* GAP, PADDING + 8 * GAP)],
            
            [(PADDING + 3 * GAP, PADDING + 2 * GAP), (PADDING + 3 * GAP, PADDING + 6 * GAP)],
            [(PADDING + 4 * GAP, PADDING + 2 * GAP), (PADDING + 4 * GAP, PADDING + 6 * GAP)],

            # diagonales
            [(PADDING, PADDING), (PADDING + 4 * GAP, PADDING + 4 * GAP)],
            [(PADDING + 4 * GAP, PADDING), (PADDING, PADDING + 4 * GAP)],
            
            [(PADDING, PADDING + 4 * GAP), (PADDING + 4 * GAP, PADDING + 8 * GAP)],
            [(PADDING + 4 * GAP, PADDING + 4 * GAP), (PADDING, PADDING + 8 * GAP)],
            
            [(PADDING, PADDING + 2 * GAP), (PADDING + 4 * GAP, PADDING + 6 * GAP)],
            [(PADDING, PADDING + 6 * GAP), (PADDING + 4 * GAP, PADDING + 2 * GAP)],
        ]
        
        for line in lines:
            self.canvas.create_line(line[0], line[1], width=LINE_THICKNESS, fill="black")
    
    def _draw_pieces(self, disposition=1):
        
        assert disposition == 1 or disposition == -1, "Disposition Invalide : Disposition doit être 1 ou -1"
        
        self.frame.red_soldier_icon = ImageTk.PhotoImage(Image.open(Assets.img_red_soldier).resize(SOLDIER_SIZE))
        self.frame.blue_soldier_icon = ImageTk.PhotoImage(Image.open(Assets.img_blue_soldier).resize(SOLDIER_SIZE))
        
        # Liste des positions de départ pour 16 pions rouges et verts
        positions_soldier_A  = []
        positions_soldier_B = []
        
        for col in range(6):
            for lin in range(4):
                if col == 1 and lin == 0 or col == 3 and lin == 0 or  col == 0 and lin == 1 or col == 4 and lin == 1:
                    continue
                positions_soldier_A.append((PADDING + col * GAP, PADDING + lin * GAP))
                positions_soldier_B.append((PADDING + (4 - col) * GAP, PADDING + (8 - lin) * GAP))
    
    
        for soldierA, soldierB in zip(positions_soldier_A, positions_soldier_B):
            if disposition == 1:
                red_piece = self.canvas.create_image(soldierA[0], soldierA[1], image=self.frame.red_soldier_icon)
                self.red_soldiers.append(red_piece)
                
                blue_piece = self.canvas.create_image(soldierB[0], soldierB[1], image=self.frame.blue_soldier_icon)
                self.blue_soldiers.append(blue_piece)
            else:
                red_piece = self.canvas.create_image(soldierB[0], soldierB[1], image=self.frame.red_soldier_icon)
                self.red_soldiers.append(red_piece)
                
                blue_piece = self.canvas.create_image(soldierA[0], soldierA[1], image=self.frame.blue_soldier_icon)
                self.blue_soldiers.append(blue_piece)
                
            self.canvas.update_idletasks()
            
    def _move_soldier_in_bord(self, piece_index, target: tuple, steps=50, delay=10):
        # TODO: impl assertion
        """
        Déplace un pion de sa position actuelle vers (target_x, target_y) en plusieurs étapes.
        
        Args:
            piece_index: L'index du soldat dans self.red_soldiers
            target: Tuple (x, y) des coordonnées cibles
            steps: Nombre d'étapes pour l'animation
            delay: Délai entre chaque étape en millisecondes
        """
        self.canvas.update_idletasks()
        target_x, target_y = target
        
        # Récupérer l'ID du soldat
        piece = self.red_soldiers[piece_index]
        
        # Vérifier que le soldat existe
        if not self.canvas.find_withtag(piece):
            print(f"Erreur: Le soldat {piece_index} n'existe pas sur le canvas")
            return
            
        # Récupérer les coordonnées actuelles
        coords = self.canvas.coords(self.red_soldiers[piece_index])
            
        current_x, current_y = coords
        delta_x = (target_x - current_x) / steps
        delta_y = (target_y - current_y) / steps
        
        def step_move(step):
            if step < steps:
                # Déplace le pion de façon incrémentale
                self.canvas.move(piece, delta_x, delta_y)
                # Re-appeler la fonction après un délai
                self.frame.after(delay, lambda: step_move(step + 1))
            else:
                # Ajuste les coordonnées finales pour être exactes
                self.canvas.coords(piece, target_x, target_y)
        
        # Lancer l'animation
        step_move(0)
    
    def _decor(self):
        """Initialise les boutons de contrôle"""
        # Bouton de réinitialisation
        self.reset_button = ctk.CTkButton(
            master=self.button_frame, text='Play',
            image=ctk.CTkImage(
                light_image=Image.open(Assets.icon_play), size=(20, 20)),
            compound="left", command=None, width=120, height=32,
            corner_radius=8, fg_color="#3B3B3B", hover_color="#131630", anchor="center"
        )
        self.reset_button.pack(side="left")
        
    def _move_soldier_offset(self):
        ...
        
    def _remove_soldier(self):
        # for piece in red_pieces:
        #     self.canvas.delete(piece)
        ...
        
    def _update_board(self):
        ...
    
    def update(self, state):
        """Met à jour le plateau en fonction du nouvel état"""
        if not state.get("board"):
            return
            
        # board = state["board"]
        # current_player = state.get("current_player_index", 0)
        
        # # Mettre à jour les positions des pièces
        # for position, soldier in board.soldiers.items():
        #     if position not in self.current_positions:
        #         # Nouvelle pièce à ajouter
        #         if soldier == -1:  # Rouge
        #             piece = self.canvas.create_image(
        #                 position[0], position[1],
        #                 image=self.frame.red_soldier_icon
        #             )
        #             self.red_soldiers.append(piece)
        #         else:  # Bleu
        #             piece = self.canvas.create_image(
        #                 position[0], position[1],
        #                 image=self.frame.blue_soldier_icon
        #             )
        #             self.blue_soldiers.append(piece)
        #         self.current_positions[position] = piece
        #     else:
        #         # Déplacer la pièce existante
        #         piece = self.current_positions[position]
        #         current_pos = self.canvas.coords(piece)
        #         if current_pos != position:
        #             self._move_soldier_in_bord(
        #                 self.red_soldiers.index(piece) if piece in self.red_soldiers else self.blue_soldiers.index(piece),
        #                 position
        #             )
        
        # # Supprimer les pièces qui ne sont plus sur le plateau
        # current_pieces = set(board.soldiers.keys())
        # for pos in list(self.current_positions.keys()):
        #     if pos not in current_pieces:
        #         piece = self.current_positions[pos]
        #         self.canvas.delete(piece)
        #         if piece in self.red_soldiers:
        #             self.red_soldiers.remove(piece)
        #         else:
        #             self.blue_soldiers.remove(piece)
        #         del self.current_positions[pos]
        
        # Mettre à jour l'interface si nécessaire
        self.canvas.update_idletasks()
        
        # Mise à jour du bouton Play en fonction de l'état du jeu
        if state.get("game_over"):
            self.play_button.configure(state="disabled")
        else:
            self.play_button.configure(state="normal")
    
    def start_game(self):
        runner = GameRunner(self.store)
        runner.run_player_game(self.agent1, self.agent2)
