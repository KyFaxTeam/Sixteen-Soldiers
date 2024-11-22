import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from models.assets.index import Assets
from utils.audio import Sounds
from utils.const import GAP, LINE_THICKNESS, PADDING,  SOLDIER_SIZE
from utils.game_runner import GameRunner
from views.base_view import BaseView
from utils.board_utils import BoardUtils  # Ajouter cet import
import logging


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
        self.previous_action = None
        
        # Ajoutez un bouton "Play"
        # self.play_button = ctk.CTkButton(self.button_frame, text="Play", command=self.start_game)
        # self.play_button.pack()
        
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
                red_piece = self.canvas.create_image(*soldierA, image=self.frame.red_soldier_icon)
                self.red_soldiers.append(red_piece)
                
                blue_piece = self.canvas.create_image(*soldierB, image=self.frame.blue_soldier_icon)
                self.blue_soldiers.append(blue_piece)
            else:
                red_piece = self.canvas.create_image(*soldierB, image=self.frame.red_soldier_icon)
                self.red_soldiers.append(red_piece)
                
                blue_piece = self.canvas.create_image(*soldierA, image=self.frame.blue_soldier_icon)
                self.blue_soldiers.append(blue_piece)
                
            self.canvas.update_idletasks()
            
            
    def _decor(self):
        """Initialise les boutons de contrôle"""
        # Bouton de réinitialisation ctk.CTkButton(self.button_frame, text="Play", command=self.start_game)
        self.play_button = ctk.CTkButton(
            master=self.button_frame, text='Play',
            image=ctk.CTkImage(
                light_image=Image.open(Assets.icon_play), size=(20, 20)),
            compound="left", command=self.start_game, width=120, height=32,
            corner_radius=8, fg_color="#3B3B3B", hover_color="#131630", anchor="center"
        )
        self.play_button.pack(side="left")
    
    def _make_action(self, action) :

        from_ = BoardUtils.algebraic_to_gameboard(action['from'])
        to = BoardUtils.algebraic_to_gameboard(action['to'])
        soldier = action['soldier']
        
        # print(to_x, to_y, BoardUtils.algebraic_to_cartesian(to))
        
        '''
            -1 -> red
            1 -> blue
        '''
        soldier_id = self._get_piece_id(from_, player=soldier)
        
        if soldier_id is None:
            print('_________________________________', *from_)
            return 
        
        if soldier == -1 :
            ...
        else:
            ...
        
        match action['type']:
            case 'MOVE_SOLDIER':
                print(*from_, "///////////////", *to, "***"*20)
                self._move_soldier_in_bord(soldier_id, to)
                exit()
            case 'CAPTURE_SOLDIER':
                # self._move_soldier_in_bord(soldier_id, to)
                # self._remove_soldier(soldier_id, player=soldier)
                ...
            
        self.previous_action = action
        
        
            
    def _move_soldier_in_bord(self, soldier_id: int, target: tuple, steps=50, delay=10):
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
        # piece = self.red_soldiers[piece_index]
        
        # Vérifier que le soldat existe
        if not self.canvas.find_withtag(soldier_id):
            print(f"Erreur: Le soldat {soldier_id} n'existe pas sur le canvas")
            return
            
        # Récupérer les coordonnées actuelles
        coords = self.canvas.coords(soldier_id)
        
        current_x, current_y = coords
        
        
        dx = (target_x - current_x) / steps  # Le décalage horizontal (en pixels)
        dy = (target_y - current_y) / steps  # Le décalage vertical (en pixels)
        
        print("88888888888", coords, target, dx, dy)
        
        def step_move(step):
            6
            if step < steps:
                # Déplace le pion de façon incrémentale
                self.canvas.move(soldier_id, dx, dy)
                # Re-appeler la fonction après un délai
                self.frame.after(delay, lambda: step_move(step + 1))
            else:
                # Ajuste les coordonnées finales pour être exactes
                self.canvas.coords(soldier_id, target_y, target_x)
        
        # Lancer l'animation
        # print("jjjjjjjjjjjjjjj") {'type': 'MOVE_SOLDIER', 'soldier': 1, 'from': 'd2', 'to': 'e3'}
        step_move(0)
        


    def _remove_soldier(self, soldier_id, player):
        """Supprime un soldat du canvas."""
        print(f"Action: Supprimer un soldat à la position  pour le joueur ")
        
        if player == -1:
            self.red_soldiers.remove(soldier_id)
        else:
            self.blue_soldiers.remove(soldier_id)
        self.canvas.delete(soldier_id)
        # soldiers_list = self.red_soldiers if soldier == PLAYER_CONFIG["PLAYER_1"] else self.blue_soldiers
        # piece = next((s for s in soldiers_list if self._get_position(s) == pos), None)
        # if piece:
        #     self.canvas.delete(piece)
        #     soldiers_list.remove(piece)
            
                
    def _get_piece_id(self, coord: tuple, player: int) -> int :
        closest_id = self.canvas.find_closest(*coord)[0]
        
        if closest_id in self.red_soldiers or closest_id in self.blue_soldiers:
            return closest_id
        # if player == -1 :
        #     if closest_id in self.red_soldiers:
                
        # if player == 1:
        #     if closest_id in self.blue_soldiers:
        #         return closest_id
        return None


    def _get_piece_index(self, piece):
        """ Retourne l'index d'un soldat dans sa liste respective. """
        if piece in self.red_soldiers:
            return self.red_soldiers.index(piece)
        elif piece in self.blue_soldiers:
            return self.blue_soldiers.index(piece)
        return -1

    def start_game(self):
        """Démarre le jeu en mode automatique avec les agents"""
        self.logger.info("Starting game from Play button")
        self.play_button.configure(state="disabled")
        
        # Lancer le jeu dans un thread séparé pour ne pas bloquer l'interface
        import threading
        def run_game():
            try:
                runner = GameRunner(self.store)
                runner.run_player_game(self.agent1, self.agent2)
            except Exception as e:
                self.logger.error(f"Error during game execution: {e}")
            finally:
                # Réactiver le bouton une fois le jeu terminé
                self.play_button.configure(state="normal")
            
        game_thread = threading.Thread(target=run_game)
        game_thread.daemon = True  # Le thread se terminera quand le programme principal se termine
        game_thread.start()
        
    def update(self, state):
        """Met à jour le plateau en fonction du nouvel état"""
        
        if not state.get("board"):
            return
            
        board = state["board"]
        new_soldiers = board.soldiers
        
        # Ne comparer que si previous_soldiers existe déjà
        # self._diff_and_update(self.previous_soldiers, new_soldiers)
        # Mettre à jour l'état précédent
        self.previous_soldiers = new_soldiers.copy()
        if state["last_board_action"] is not None and self.previous_action != state["last_board_action"] :
            self._make_action(state["last_board_action"])
            # exit()

        # # Mettre à jour l'interface
        # self.canvas.update_idletasks()
        
        # Mise à jour du bouton Play
        if state.get("game_over"):
            self.play_button.configure(state="disabled")
        else:
            self.play_button.configure(state="normal")
