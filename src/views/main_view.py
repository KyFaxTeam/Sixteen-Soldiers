import customtkinter as ctk
from tkinter import filedialog
import logging
import os
from datetime import datetime, timedelta
from src.utils.const import  Soldier, resolution, screen_width, screen_height

from src.store.store import Store
from src.utils.save_utils import load_game, save_game
from src.views.Others_Windows.home_view import HomeView
from src.views.base_view import BaseView
from src.views.game_board import GameBoard
from src.views.Others_Windows.after_game_view import AfterGameView
from src.views.Right_Column.history_view import HistoryView
from src.views.Left_Column.players_column import PlayersColumn
from src.views.Right_Column.history_view import HistoryView
from src.views.Right_Column.setting_view import SettingsView
from src.utils.game_utils import GameRunner, show_popup

from src.tournament.tournament_manager import TournamentManager

logger = logging.getLogger(__name__)
class MainView(BaseView):
    """Main window of the application"""
    def __init__(self, master, store):
        super().__init__(master)

        self.store :Store = store
        self.after_game_view = None  # Initialize the attribute to track the view
        self.logger = logging.getLogger(__name__)
        # Set window title
        self.master.title("Sixteen Soldiers")
        
        # Get screen dimensions
        self.adjust_player_column = {
            "HD": "new",
            "Full HD": "nsew",
            "HD+": "nsew",
            "Quad HD":  "nsew",
            "4K Ultra HD":  "nsew"
        }

        
        # Calculate window sizes
        if resolution == "HD":
            self.home_width = int(screen_width * 0.3)
            self.home_height = int(screen_height * 0.4)
            self.game_width = int(screen_width * 0.75)
            self.game_height = int(screen_height * 0.75)
        else :

            self.home_width = int(screen_width * 0.2)
            self.home_height = int(screen_height * 0.3)
            self.game_width = int(screen_width * 0.75)
            self.game_height = int(screen_height * 0.75)
        
        # Set initial size for home view
        self.master.geometry(f"{self.home_width}x{self.home_height}")
        
        # Initialize all component references as None
        self.players_column = None
        self.game_board = None
        self.history_view = None
        self.settings_view = None
        
        # self.start_new_game()
        self.logger = logging.getLogger(__name__)
        # Initialize HomeView
        self.home_view = HomeView(self.master, self.configure_main_view, self.review_match)
        self.home_view.show()
        self.game_runner = GameRunner(self.store)

        # Ajouter un gestionnaire pour la fermeture de la fenêtre
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.tournament_mode = True
        self.tournament_manager = None
        self.handling_tournament_end = False
        self.match_start_time = None
        self.match_duration = timedelta(minutes=4)

    def configure_main_view(self, game_data=None):
        """Configure la vue principale"""
        self.home_view.hide()
        self.master.geometry(f"{self.game_width}x{self.game_height}")
        self.game_runner.set_mode('replay' if game_data else 'game', game_data)
        # Si on vient de la home view (pas de game_data) et qu'on est en mode tournoi
        if not game_data and self.tournament_mode:
            self.build_main_view()
            self.start_tournament()
        else:
            
            self.build_main_view()

    def review_match(self):
        """Review a match by selecting a saved game file and switching to the history view."""
        try:
            root = ctk.CTkToplevel()  # Utiliser CTkToplevel au lieu de Tk
            try:
                save_folder = os.path.join(os.getcwd(), "saved_game")
                if not os.path.exists(save_folder):
                    show_popup("No saved games found. Play and save a game first.", "No Games")
                    return
                
                root.withdraw()  # Cacher la fenêtre
                root.attributes("-topmost", True)
                file_path = filedialog.askopenfilename(
                    parent=root,  # Spécifier le parent
                    title="Select Saved Game File",
                    filetypes=[("JSON Files", "*.json")],
                    initialdir=save_folder
                )
                
                if not file_path:
                    return
                
                # Load and validate the game file
                game_data = load_game(file_path)
                if not game_data or 'history' not in game_data:
                    show_popup("Invalid or corrupted game file.", "Error")
                    return
                
                if not game_data['history']:
                    show_popup("This game file contains no moves to replay.", "Empty Game")
                    return

                self.configure_main_view(game_data=game_data)
            finally:
                root.destroy()  # S'assurer que la fenêtre est détruite
                 
        except Exception as e:
            self.logger.error(f"An error occurred while reviewing the match: {e}")
            show_popup("Error loading replay", "Error", "error")

    def build_main_view(self):
        """Create the main layout and initialize sub-views only when needed"""
        if hasattr(self, 'main_container'):
            self.main_container.destroy()

        # Create main container frame
        self.main_container = ctk.CTkFrame(self.master) 
        self.main_container.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Content frame with 3 columns
        self.content = ctk.CTkFrame(self.main_container)
        self.content.pack(expand=True, fill="both", padx=10, pady=10)
        self.content.grid_columnconfigure(0, weight=1)  # Adjust left column width
        self.content.grid_columnconfigure(1, weight=2)  # Center column expands
        self.content.grid_columnconfigure(2, weight=1)  # Right column
        
        # Left column - Players
        self.players_column = PlayersColumn(self.content, self.store)
        self.players_column.frame.grid(row=0, column=0, sticky= self.adjust_player_column[resolution],
                                        padx=(5, 0), pady=30)  # Ajout de pady=20
        
        # Center column - Game board
        self.center_column = ctk.CTkFrame(self.content)
        self.center_column.grid(row=0, column=1, sticky="n")
        
        # Créer le GameBoard sans agents
        self.game_board = GameBoard(self.center_column, self.store, self.game_runner)
        self.game_board.frame.grid(row=0, column=0, sticky="nsew")
        self.game_board.subscribe(self.store)
        self.game_board.update(self.store.get_state())
        
        # Right column - Move history and settings
        self.right_column = ctk.CTkFrame(self.content)#, fg_color="transparent")
        self.right_column.grid(row=0, column=2, sticky="nsew", padx=(0, 5), pady=(10, 1))
        
        # History view
        self.history_view = HistoryView(self.right_column, self.store)
        self.settings_view = SettingsView(self.right_column, self.store)

    def show_after_game_view(self):
        """Show AfterGameView with winner details"""
        if self.after_game_view is not None:
            # self.logger.warning("AfterGameView is already displayed.")
            return
        
        self.logger.info("Displaying AfterGameView.")
        self.after_game_view = AfterGameView(
            self.master,
            store=self.store,
            on_restart=self.return_to_home,
            on_save=lambda button: self.handle_save(button)
        )
    
    def handle_save(self, button):
        """Handles the save process and updates the button state."""
        try:
            save_game(self.store.get_state())  # Save the game
            button.configure(text="Saved", state="disabled")  # Update button text and disable it
            self.logger.info("Game successfully saved.")
            show_popup("Game successfully saved", "Success", "info")
        except Exception as e:
            self.logger.error(f"An error occurred while saving the game: {e}")

    def return_to_home(self):
        """Reset game and return to HomeView"""
        if self.after_game_view:
            self.after_game_view.destroy()
            self.after_game_view = None

        if hasattr(self, 'main_container'):
            self.main_container.pack_forget()
            del self.main_container

        # Clean up game runner state
        self.game_runner.cleanup()
        
        self.store.dispatch({"type": "RESTART_GAME"})
        
        self.master.geometry(f"{self.home_width}x{self.home_height}")
        self.home_view.show()
      
    def run(self):
        self.master.mainloop()
   
    def update(self, state: dict):
        """Update the view with new state based on game status."""
        if state["is_game_over"]:
            print(f"\nUpdate - Game Over détecté!")
            print(f"Tournament mode: {self.tournament_mode}")
            print(f"handling_tournament_end: {self.handling_tournament_end}")
            print(f"Reason: {state.get('reason')}")
            
            if self.tournament_mode:
                if not self.handling_tournament_end:
                    print("Début du handle_tournament_match_end")
                    self.handle_tournament_match_end()
                return
            else:
                if not self.after_game_view:
                    self.show_after_game_view()
                return

        # En mode tournoi, on ne gère pas le nettoyage ici
        if not self.tournament_mode:
            if hasattr(self, 'history_view') and hasattr(self, 'game_board'):
                if state.get("is_game_leaved"):
                    self.history_view.clear_moves()
                    self.game_board.reset_game()

        # Mise à jour normale des composants du jeu
        if hasattr(self, 'players_column'):
            self.players_column.update(state)

        if not state["is_game_started"]:
            return

        if hasattr(self, 'game_board'):
            self.game_board.update(state)
        if hasattr(self, 'history_view'):
            self.history_view.update(state)

    def on_closing(self):
        """Gestionnaire de l'événement de fermeture de la fenêtre"""
        # Fermer la fenêtre
        self.master.destroy()

    def handle_tournament_match_end(self):
        """Gère la fin d'un match de tournoi"""
        if not self.tournament_manager or self.handling_tournament_end:
            return

        self.handling_tournament_end = True
        
        try:
            # Show after game view
            self.show_after_game_view()
            
            # Collect match statistics
            state = self.store.get_state()
            history = state.get('move_history', [])

            perf_A, perf_B = [],  []
            teamA_data, teamB_data = {}, {}
            info_index = state.get("agents_info_index", {}).get(Soldier.RED)
            if info_index:
                teamA_data = state.get("agents", {}).get(info_index, {})
                perf_A = teamA_data.get("performances", [])[-1]

            info_index = state.get("agents_info_index", {}).get(Soldier.BLUE)
            if info_index:
                teamB_data = state.get("agents", {}).get(info_index, {})
                perf_B = teamB_data.get("performances", [])[-1]

    
            # Calculate statistics
            stats = {
                'pieces_a': state.get("board").count_soldiers(teamA_data.get('soldier_value')), # Red pieces
                'pieces_b': state.get("board").count_soldiers(teamB_data.get('soldier_value')),  # Blue pieces
                'moves_a': perf_A['number_of_moves'],    # Number of moves by red
                'moves_b': perf_B['number_of_moves'],   # Number of moves by blue
                'time_a': perf_A['time'],   # Time used by red
                'time_b': perf_A['time'],   # Time used by blue
                'reason': state.get('reason', 'unknown')
            }

            # Record match result with stats
            self.tournament_manager.record_match_result(
                winner=state.get("winner"),
                moves=len(history),
                forfeit=state.get("forfeit", False),
                stats=stats
            )

            # Handle match timing
            if self.match_start_time:
                elapsed = datetime.now() - self.match_start_time
                if elapsed < self.match_duration:
                    delay = int((self.match_duration - elapsed).total_seconds() * 1000)
                    print(f"Programmation du nettoyage dans {delay/1000:.1f} secondes")
                    # Programmer le nettoyage après le délai
                    self.master.after(delay, self._prepare_next_match)
                else:
                    
                    # Attente minimale de 30 secondes
                    # print("Programmation du nettoyage dans 30 secondes")
                    self.master.after(20000, self._prepare_next_match)
            else:
                self.master.after(20000, self._prepare_next_match)
            
        except Exception as e:
            print(f"Error in handle_tournament_match_end: {e}")
            self.handling_tournament_end = False
            raise e

    def _prepare_next_match(self):
        """Prépare le prochain match dans le bon ordre"""
        try:
            print("Préparation du prochain match...")
            print(f"handling_tournament_end: {self.handling_tournament_end}")
            
            # 1. Nettoyer l'interface actuelle
            if self.after_game_view:
                self.after_game_view.sounds.unpause()
                self.after_game_view.destroy()
                self.after_game_view = None

            # 2. Réinitialiser le jeu
            self.store.dispatch({"type": "RESTART_GAME"})
            if hasattr(self, 'game_board'):
                self.game_board.reset_game()
            if hasattr(self, 'history_view'):
                self.history_view.clear_moves()

            self.handling_tournament_end = False
            
            # 3. Configurer le prochain match
            next_match = self.tournament_manager.setup_next_match()
            if next_match:
                if next_match.get("phase_transition"):
                    show_popup(
                        "Fin de la phase ALLER\nDébut de la phase RETOUR",
                        "Transition de phase",
                        auto_close=True,
                        duration=10000  # 10 secondes de pause
                    )
                    self.tournament_manager._initialize_matches()
                    self._prepare_next_match()
                    return
                    
                if next_match["is_forfeit"]:
                    print(f"\nDétection d'un forfait!")
                    print(f"Équipe forfait: {next_match['is_forfeit']}")
                    print("Dispatch de l'événement END_GAME avec forfait...")
                    self.store.dispatch({
                        "type": "END_GAME",
                        "winner": next_match["is_forfeit"],
                        "reason": "forfait"
                    })
                else:
                    self._configure_match_agents(next_match)
                    self.match_start_time = datetime.now()
                    self.game_runner.start()
            else:
                self.end_tournament()

        except Exception as e:
            print(f"Erreur lors de la préparation du prochain match: {e}")
            self.handling_tournament_end = False

    def _configure_match_agents(self, match_info):
        """Configure les agents pour le match"""
        print("\n=== Configuration du match ===")
        print(f"Match info: {match_info}")
        
        print(f"\nMatch {match_info['round']}/{match_info['total_rounds']} - Phase {match_info['phase']}")
        # ...existing code...
        
        print("\nConfiguration des agents:")
        for color, agent in [("red", Soldier.RED), ("blue", Soldier.BLUE)]:
            print(f"Configuration agent {color}: {match_info[f'{color}_agent_file']} - {agent.name}")
            self.store.dispatch({
                "type": "SELECT_AGENT",
                "soldier_value": agent,
                "info_index": f"{match_info[f'{color}_agent_file']}_{agent.name}"
            })
        
        print(f"\nMatch {match_info['round']}/{match_info['total_rounds']}")
        print(f"{match_info['red_agent']} vs {match_info['blue_agent']}")
        print("Configuration du match terminée\n")

        return 

    def end_tournament(self):
        """Termine le tournoi"""
        self.tournament_mode = False
        self.tournament_manager = None
        self.match_start_time = None
        
        show_popup(
            "Le tournoi est terminé.\nLes résultats ont été sauvegardés dans le dossier 'results'.",
            "Fin du tournoi"
        )
        
        self.return_to_home()

    def start_tournament(self):
        """Initialise et démarre un nouveau tournoi"""
        try:
            self.tournament_mode = True
            self.tournament_manager = TournamentManager(self.store)
            self.handling_tournament_end = False
            
            # Initialiser le tournoi
            num_matches = self.tournament_manager._initialize_matches()
            
            if num_matches == 0:
                raise ValueError("Aucun match trouvé pour cette pool")
            
            # Démarrer le premier match 
            self._prepare_next_match()
            
        except Exception as e:
            self.logger.error(f"Erreur lors du démarrage du tournoi: {e}")
            show_popup(str(e), "Erreur de tournoi")
            self.tournament_mode = False
            self.return_to_home()