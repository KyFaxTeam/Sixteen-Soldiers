import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from models.assets.index import Assets
from utils.audio import Sounds
from utils.const import GAP, LINE_THICKNESS, PADDING, PLAYER_CONFIG, SOLDIER_SIZE
from utils.game_runner import GameRunner
from views.base_view import BaseView
from utils.board_utils import BoardUtils  # Ajouter cet import


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
        # Initialiser previous_soldiers avec l'état initial du plateau
        self.previous_soldiers = store.get_state()["board"].soldiers.copy()
        self.sounds = Sounds()
        self._init_board()
        
        # Ajoutez un bouton "Play"
        self.play_button = ctk.CTkButton(self.button_frame, text="Play", command=self.start_game)
        self.play_button.pack()
        
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
        
    
    
    def update(self, state):
        """Met à jour le plateau en fonction du nouvel état"""
        if not state.get("board"):
            return
            
        board = state["board"]
        new_soldiers = board.soldiers
        
        # Ne comparer que si previous_soldiers existe déjà
        self._diff_and_update(self.previous_soldiers, new_soldiers)
        print()
        # Mettre à jour l'état précédent
        self.previous_soldiers = new_soldiers.copy()

        # Mettre à jour l'interface
        self.canvas.update_idletasks()
        
        # Mise à jour du bouton Play
        if state.get("game_over"):
            self.play_button.configure(state="disabled")
        else:
            self.play_button.configure(state="normal")

    def _diff_and_update(self, old_soldiers, new_soldiers):
        """Compare l'ancien et le nouvel état des soldats et met à jour le canvas."""
        
        # Détecter les ajouts et les mouvements
        for pos, soldier in new_soldiers.items():
            old_soldier = old_soldiers.get(pos, 0)
            if soldier != old_soldier:
                if soldier != PLAYER_CONFIG["EMPTY"]:
                    if old_soldier == PLAYER_CONFIG["EMPTY"]:
                        # Nouveau soldat ajouté
                        self._add_soldier(pos, soldier)
                    else:
                        # Soldat déplacé ou changé de type
                        self._move_soldier(old_soldiers, pos, soldier)
        
        # Détecter les suppressions
        for pos, soldier in old_soldiers.items():
            if pos not in new_soldiers or new_soldiers[pos] == PLAYER_CONFIG["EMPTY"]:
                if soldier != PLAYER_CONFIG["EMPTY"]:
                    self._remove_soldier(pos, soldier)

    def _add_soldier(self, pos, soldier):
        """Ajoute un soldat au canvas."""
        print(f"Action: Ajouter un soldat à la position {pos} pour le joueur {PLAYER_CONFIG['COLORS'][soldier]}")
        canvas_x, canvas_y = BoardUtils.algebraic_to_gameboard(pos)
        if soldier == PLAYER_CONFIG["PLAYER_1"]:
            piece = self.canvas.create_image(canvas_x, canvas_y, image=self.frame.red_soldier_icon)
            self.red_soldiers.append(piece)
        elif soldier == PLAYER_CONFIG["PLAYER_2"]:
            piece = self.canvas.create_image(canvas_x, canvas_y, image=self.frame.blue_soldier_icon)
            self.blue_soldiers.append(piece)

    def _remove_soldier(self, pos, soldier):
        """Supprime un soldat du canvas."""
        print(f"Action: Supprimer un soldat à la position {pos} pour le joueur {PLAYER_CONFIG['COLORS'][soldier]}")
        soldiers_list = self.red_soldiers if soldier == PLAYER_CONFIG["PLAYER_1"] else self.blue_soldiers
        piece = next((s for s in soldiers_list if self._get_position(s) == pos), None)
        if piece:
            self.canvas.delete(piece)
            soldiers_list.remove(piece)

    def _move_soldier(self, old_soldiers, new_pos, soldier):
        """Déplace un soldat de sa position précédente vers une nouvelle position."""
        print(f"Action: Déplacer un soldat pour le joueur {PLAYER_CONFIG['COLORS'][soldier]} vers la position {new_pos}")
        old_pos = next((pos for pos, s in old_soldiers.items() if s == soldier and new_pos not in old_soldiers.get(pos, PLAYER_CONFIG["EMPTY"])), None)
        if old_pos:
            piece = next((s for s in (self.red_soldiers if soldier == PLAYER_CONFIG["PLAYER_1"] else self.blue_soldiers)
                         if self._get_position(s) == old_pos), None)
            if piece:
                target_x, target_y = BoardUtils.algebraic_to_gameboard(new_pos)
                self._move_soldier_in_bord(self._get_piece_index(piece), (target_x, target_y))
                soldiers_list = self.red_soldiers if soldier == PLAYER_CONFIG["PLAYER_1"] else self.blue_soldiers
                soldiers_list.remove(piece)
                soldiers_list.append(piece)

    def _get_position(self, piece):
        """Retourne la position algébrique d'un soldat à partir de son ID canvas."""
        coords = self.canvas.coords(piece)
        cartesian = (coords[0] - PADDING) // GAP, (coords[1] - PADDING) // GAP
        # Convertir cartésien en algébrique
        letter = chr(int(cartesian[0]) + ord('a'))
        number = str(int(cartesian[1]) + 1)
        return f"{letter}{number}"

    def _get_piece_index(self, piece):
        """Retourne l'index d'un soldat dans sa liste respective."""
        if piece in self.red_soldiers:
            return self.red_soldiers.index(piece)
        elif piece in self.blue_soldiers:
            return self.blue_soldiers.index(piece)
        return -1

    def start_game(self):
        """Démarre le jeu en mode automatique avec les agents"""
        # Désactiver le bouton pendant le jeu
        self.play_button.configure(state="disabled")
        
        # Lancer le jeu dans un thread séparé pour ne pas bloquer l'interface
        import threading
        def run_game():
            runner = GameRunner(self.store)
            runner.run_player_game(self.agent1, self.agent2)
            # Réactiver le bouton une fois le jeu terminé
            self.play_button.configure(state="normal")
            
        game_thread = threading.Thread(target=run_game)
        game_thread.daemon = True  # Le thread se terminera quand le programme principal se termine
        game_thread.start()
