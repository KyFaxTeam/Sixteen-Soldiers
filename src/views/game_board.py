
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from models.assets.index import Assets
from utils.audio import Sounds
from utils.const import GAP, LINE_THICKNESS, PADDING, SOLDIER_SIZE, Soldier
from utils.game_utils import GameRunner
from views.base_view import BaseView
from utils.board_utils import BoardUtils  
from utils.history_utils import get_last_move, is_equals  
import logging
import traceback
from store.store import Store

# theme_colors = ctk.ThemeManager.theme["CTkFrame"]  # Obtenir les styles de base
# bg_color = theme_colors["fg_color"]


class GameBoard(BaseView):
    
    def __init__(self, master, store: Store):
        # store.state['board']
        super().__init__(master)
        self.store = store
        self.frame.pack(expand=True, fill="both")
        
        # Créer un conteneur pour le canvas et les boutons
        self.main_container = ctk.CTkFrame(self.frame)
        self.main_container.pack(expand=True, fill="both")
        
        
        self.canvas = tk.Canvas(self.main_container, 
                                    width= 4 * GAP + 2 * PADDING, 
                                    height= 8 * GAP + 2 * PADDING,  highlightthickness=0,
                                    bg="#2b3665", highlightbackground="#424977",      # Couleur de la bordure inactive
                                    )

        # Créer un frame pour les boutons (en haut)
        self.button_frame = ctk.CTkFrame(self.main_container)
        self.button_frame.pack(padx=5, pady=5)
        
        self.canvas.pack()
        self.red_soldiers = []
        self.blue_soldiers = []
        self.previous_move = None
        self.is_game_started = False
        self.is_paused = True

        self.sounds = Sounds()
        self._init_board()
        
        self.logger = logging.getLogger(__name__)
        self.previous_move = None  # Ajouter cet attribut
        # self.logger.info("GameBoard initialized")
        
    def _init_board(self):
        """Initializes the game board by drawing the board, pieces, playing background music, and setting up the decor."""
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
                positions_soldier_A.append((PADDING + col * GAP, PADDING + lin * GAP))
                positions_soldier_B.append((PADDING + (4 - col) * GAP, PADDING + (8 - lin) * GAP))
    
    
        for soldierA, soldierB in zip(positions_soldier_A, positions_soldier_B):
            
            red_piece = self.canvas.create_image(soldierA[0], soldierA[1], image=self.frame.red_soldier_icon)
            self.red_soldiers.append(red_piece)
                
            blue_piece = self.canvas.create_image(soldierB[0], soldierB[1], image=self.frame.blue_soldier_icon)
            self.blue_soldiers.append(blue_piece)
            
                
            self.canvas.update_idletasks()
    
    def _decor(self):
        """Initialise les boutons de contrôle"""
        # Play button
        self.play_pause_button = ctk.CTkButton(
                    master=self.button_frame, text='Play',
                    image=ctk.CTkImage(
                        light_image=Image.open(Assets.icon_play), size=(20, 20)),
                    compound="left", command=self.toggle_play_pause, width=120, height=32,
                    corner_radius=8, fg_color="#3B3B3B", hover_color="#131630", anchor="center"
                )
        self.play_pause_button.pack(side="left", padx=5)
        # self.play_pause_button.configure(command=self.toggle_play_pause)
    
        
        # Annotation des coordonnées de chaque pion
        for i in range(9):
            custom_font = ctk.CTkFont(family=Assets.font_montserrat, size=15)
            if i < 5:
                x = PADDING + i * GAP
                self.canvas.create_text(x, 8*GAP + 2 * PADDING -10 , text=str(i + 1), font=custom_font, fill="white", anchor="center", tags="optional_tag")
            y = PADDING + i * GAP
            self.canvas.create_text(10, y, text=chr(ord('a') + i), font=custom_font, fill="white", anchor="center", tags="optional_tag")
        
        # self.play_button.pack(side="left", padx=5)
        # self.pause_button.pack(side="left")

    
            
    def _move_soldier_in_board(self, soldier_id: int, target: tuple, player: int, steps=50, delay=10):
        """
            Moves a piece from its current position to (target_x, target_y) in multiple steps.
            
            Args:
                piece_index: The index of the soldier in self.red_soldiers
                target: Tuple (x, y) of the target coordinates
                steps: Number of steps for the animation
                delay: Delay between each step in milliseconds
            """
        
        self.canvas.update_idletasks()
        
        
        if soldier_id is None:
            self.logger.error(f"""\nError: Soldier not found at position {soldier_position}\nFrom: _move_soldier_in_board""")
            return
            
        # Récupérer les coordonnées actuelles
        coords = self.canvas.coords(soldier_id)
        
        current_x, current_y = coords
        target_x, target_y = target
        
        dh = (target_x - current_x) / steps
        dv = (target_y - current_y) / steps
        
        def step_move(step):
            if step < steps:
                # Déplace le pion de façon incrémentale
                self.canvas.move(soldier_id, dh, dv)
                # Re-appeler la fonction après un délai
                self.frame.after(delay, lambda: step_move(step + 1))
            else:
                # Ajuste les coordonnées finales pour être exactes
                self.canvas.coords(soldier_id, target_x, target_y)
        
        # Lancer l'animation
        step_move(0)
    
    def _get_piece_id(self, position: tuple, player: int):
        """Retourne l'ID du soldat à partir de sa position et du joueur."""
        soldiers = self.red_soldiers if player == 0 else self.blue_soldiers
        for piece in soldiers:
            coords = self.canvas.coords(piece)
            if tuple(coords) == position:
                return piece
        return None
        
    
    def _make_action(self, move: dict) :
        """Effectue une action sur le plateau de jeu."""
        from_pos = move["pos"][-2] if len(move["pos"]) >= 2 else move["pos"][0]
        to_pos = move["pos"][-1]
        player = move["soldier_value"].value
        
        # print(to_x, to_y, BoardUtils.algebraic_to_cartesian(to))
        
        soldier_id = self._get_piece_id(position=BoardUtils.algebraic_to_gameboard(from_pos), player=player)
        
        if soldier_id is None:
            return 

        self._move_soldier_in_board(soldier_id, BoardUtils.algebraic_to_gameboard(to_pos), player=player)
        
        is_capture = move.get("captured_soldier") is not None
        
        if is_capture:
            
            captured_soldier = move["captured_soldier"][-1]
            
            captured_id = self._get_piece_id(position=BoardUtils.algebraic_to_gameboard(captured_soldier), player=1 - player)
            
            if captured_id is not None:
                # self.sounds.pause()
                self.sounds.kill_soldier()
                # self.sounds.unpause()
                self.canvas.delete(captured_id)
            
        self.previous_action = move
        # exit()
        
    def update(self, state):
        """ Updates the board based on the new state """
        # update seulement si le jeu est en cours
        
        if not self.is_game_started:
            return
        try:
            # self.logger.info("Starting GameBoard update")
            # self.logger.debug(f"Current state: {state.get('is_game_over')}, {state.get('board')}")
            
            if not state.get("board"):
                self.logger.warning("No board in state")
                return
                
            last_move = get_last_move(state)
            #self.logger.info(f"Last move: {last_move}")

            if not is_equals(last_move, self.previous_move):
                # self.logger.info(f"Processing new move: {last_move}")
                try:
                    self._make_action(last_move.to_dict())
                except Exception as e:
                    self.logger.error(f"Error in _make_action: {e}")
                    self.logger.error(traceback.format_exc())

            self.canvas.update_idletasks()
            
            # Update button states
            if state.get("is_game_over"):
                self.logger.info("Game is over - disabling play button")
                # self.play_button.configure(state="disabled")
            else:
                ...
                # self.play_button.configure(state="normal")

            if state.get("is_game_paused"):
                self.logger.info("Game is paused - changing pause button text")
                # self.pause_button.configure(text="Resume")
                # self.sounds.pause()

        except Exception as e:
            self.logger.error(f"Error in update: {e}")
            self.logger.error(traceback.format_exc())

    def _move_soldier_from_history(self, from_pos: str, to_pos: str, role: str):
        """Déplace un soldat basé sur l'historique des mouvements."""
        try:
            self.logger.info(f"Moving soldier for role {role} from {from_pos} to {to_pos}")
            
            soldiers_list = self.red_soldiers if role == "PLAYER_1" else self.blue_soldiers
            self.logger.debug(f"Using {'red' if role == 'PLAYER_1' else 'blue'} soldiers list")
            
            piece = next((s for s in soldiers_list if self._get_position(s) == from_pos), None)
            if piece:
                self.logger.info(f"Found piece at position {from_pos}")
                target_x, target_y = BoardUtils.algebraic_to_gameboard(to_pos)
                piece_index = self._get_piece_index(piece)
                self.logger.debug(f"Moving to ({target_x}, {target_y}), piece index: {piece_index}")
                # self._move_soldier_in_board(piece_index, (target_x, target_y))
            else:
                self.logger.error(f"No piece found at position {from_pos}")
                
        except Exception as e:
            self.logger.error(f"Error in _move_soldier_from_history: {e}")
            self.logger.error(traceback.format_exc())

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
        # Vérifie d'abord dans les soldats rouges (PLAYER_1)
        if piece in self.red_soldiers:
            return self.red_soldiers.index(piece)
        # Sinon vérifie dans les soldats bleus (PLAYER_2)
        elif piece in self.blue_soldiers:
            return self.blue_soldiers.index(piece)
        return -1

    def start_game(self):
        """Start the game in automatic mode with agents."""
        self.logger.info("Starting game from Play button")
        # self.play_button.configure(state="disabled")
        
        # Créer les agents lors du clic sur le bouton Play seulement si dans le store, les attributs les 
        # concernant sont à None
        agents_info_index = self.store.get_state().get("agents_info_index", {})
        agents = self.store.get_state().get("agents", {})
        if not agents_info_index[Soldier.RED]:
            self.logger.info("Agent RED not found, we will create RandomAgent")
            agents_info_index[Soldier.RED] = "minimax_RED"

        if not agents_info_index[Soldier.BLUE]:
            self.logger.info("Agent BLUE not found, we will create RandomAgent")
            agents_info_index[Soldier.BLUE] = "random_agent_BLUE"
            
        # file 1 = agents_info_index[Soldier.RED] en enlevant RED du nom du file 
        file_1 = agents_info_index[Soldier.RED].rsplit('_', 1)[0]
        agent_module_1 = __import__(f"agents.{file_1}", fromlist=['Agent'])
        agent1 = agent_module_1.Agent(
            soldier_value=Soldier.RED,
            data = agents.get(agents_info_index[Soldier.RED], None)

        )
 
        file_2 = agents_info_index[Soldier.BLUE].rsplit('_', 1)[0]
        agent_module_2 = __import__(f"agents.{file_2}", fromlist=['Agent'])
        agent2 = agent_module_2.Agent(
            soldier_value=Soldier.BLUE,
            data = agents.get(agents_info_index[Soldier.BLUE], None)
        )



        # Enregistrer les agents dans le store
        self.store.register_agents(agent1, agent2)
        
        import threading
        def run_game():
            self.store.state["is_game_started"] = True
            runner = GameRunner(self.store)
            runner.run_game(agent1, agent2)
            # Réactiver le bouton une fois le jeu terminé

        self.is_game_started = True
        game_thread = threading.Thread(target=run_game)
        game_thread.daemon = True  # Le thread se terminera quand le programme principal se termine
        game_thread.start()

    def toggle_play_pause(self):
        """Toggle the play/pause state of the game."""
        if not self.is_game_started:
            # If the game has not started, start the game
            self.start_game()
            # Change the button text to "Pause"
            self.play_pause_button.configure(text="Pause")
            # Set the game state to not paused
            self.is_paused = False
        else:
            # Get the current state from the store
            current_state = self.store.get_state()
            # Check if the game is currently paused
            is_paused = current_state.get('is_game_paused', False)
            
            if not is_paused:
                # If the game is not paused, pause the game
                self.logger.info("Game paused\nFrom: toggle_play_pause")
                self.store.dispatch({'type': 'PAUSE_GAME'})
                # Change the button text to "Resume"
                self.play_pause_button.configure(text="Resume")
                # Change the button icon to play
                self.play_pause_button.configure(
                    image = ctk.CTkImage(
                        light_image=Image.open(Assets.icon_play), size=(20, 20)))
            else:
                # If the game is paused, resume the game
                self.logger.info("Game resumed\nFrom: toggle_play_pause")
                self.store.dispatch({'type': 'RESUME_GAME'})
                # Change the button icon to pause
                self.play_pause_button.configure(
                    image = ctk.CTkImage(
                        light_image=Image.open(Assets.icon_pause), size=(20, 20)))
                # Change the button text to "Pause"
                self.play_pause_button.configure(text="Pause")
            # Toggle the paused state
            self.is_paused = not is_paused
