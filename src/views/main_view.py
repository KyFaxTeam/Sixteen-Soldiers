import customtkinter as ctk
from tkinter import filedialog
import logging
import os
from datetime import datetime, timedelta
from src.utils.const import  TIMINGS, Soldier, resolution, screen_width, screen_height, GameEndReason


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

from pathlib import Path
from src.tournament.double_elim_manager import DoubleEliminationManager
from src.tournament.config import TEAMS, TEAMS_MAPPING
from src.utils.history_utils import get_move_player_count
from src.views.bracket import create_tournament_bracket
import matplotlib.pyplot as plt

from CTkMessagebox import CTkMessagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

logger = logging.getLogger(__name__)
class MainView(BaseView):
    """Main window of the application"""
    def __init__(self, master, store):
        super().__init__(master)

        self.store :Store = store
        self.after_game_view = None  # Initialize the attribute to track the view
        self.retour_popup_shown = False  # Nouvel attribut
        
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
        
        # Create tournament directory
        self.tournament_dir = Path(__file__).parent.parent / "tournament" / "tournament_data"
        self.brackets_dir = self.tournament_dir / "brackets"
        self.tournament_dir.mkdir(exist_ok=True)
        self.brackets_dir.mkdir(exist_ok=True)


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
        # Automatically save the game
        try:
            save_game(self.store.get_state())  # Save the game
            self.logger.info("Game automatically saved when AfterGameView was displayed.")
            # show_popup("Game successfully saved automatically", "Success", "info")
        except Exception as e:
            self.logger.error(f"An error occurred while automatically saving the game: {e}")
    
    def handle_save(self, button):
        """Handles the save process and updates the button state."""
        if self.store.state["reason"]!="forfeit":
            try:
                save_game(self.store.get_state())  # Save the game
                button.configure(text="Saved", state="disabled")  # Update button text and disable it
                self.logger.info("Game successfully saved.")
                # show_popup("Game successfully saved", "Success", "info")
            except Exception as e:
                self.logger.error(f"An error occurred while saving the game: {e}")

    def return_to_home(self):
        """Reset game and return to HomeView"""
        if self.after_game_view:
            self.after_game_view.destroy()
            self.after_game_view = None
            self.master.update()  # Force update of UI

        if hasattr(self, 'game_board'):
            self.game_board.reset_game()
        
        if hasattr(self, 'history_view'):
            self.history_view.clear_moves()

        if hasattr(self, 'main_container'):
            self.main_container.pack_forget()
            self.main_container.destroy()
            del self.main_container
            self.master.update()  # Force update of UI

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
            if self.tournament_mode:
                if not self.handling_tournament_end:
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

    def show_transition_popup(self, current_match):
        """Show transition popup between tournament matches"""
        try:
            self.logger.info("Starting transition popup")
            # Obtenir d'abord les infos du prochain match
            next_match_info = self.tournament_manager.setup_next_match()
            next_teams = (f"{next_match_info['red_agent']} vs {next_match_info['blue_agent']}" 
                         if next_match_info else "Tournoi terminé")
            
            # Créer une fenêtre pour le bracket
            bracket_window = ctk.CTkToplevel()
            bracket_window.title("Tournament Bracket")
            
            # Mettre en plein écran
            bracket_window.state('zoomed')  # Pour Windows
            # Pour Linux/Mac, utiliser:
            # bracket_window.attributes('-fullscreen', True)
            
            def create_and_show_bracket():
                # Créer et sauvegarder le bracket
                fig = create_tournament_bracket()
                plt.tight_layout()
                
                # Sauvegarder l'image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"bracket_match_{current_match.id}_{timestamp}.png"
                filepath = self.brackets_dir / filename
                fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
                self.logger.info(f"Bracket saved to {filename}")
                
                # Intégrer le bracket dans la fenêtre avec Canvas
                canvas = FigureCanvasTkAgg(fig, master=bracket_window)
                canvas.draw()
                canvas_widget = canvas.get_tk_widget()
                canvas_widget.pack(fill='both', expand=True)
                plt.close(fig)
                
                # Afficher le popup après que le bracket soit chargé
                if next_match_info:
                    popup = CTkMessagebox(
                        master=bracket_window,
                        title="Tournament Match Complete",
                        message=f"Match {current_match.id} is complete.\n\nNext match:\n{next_teams}",
                        icon="info",
                        option_1="Continue",
                        width=400,
                        height=200
                    )
                    popup.wait_window()  # Attendre que l'utilisateur ferme le popup
                    bracket_window.destroy()  # Fermer la fenêtre du bracket
                    self._prepare_next_match()  # Continuer seulement après que l'utilisateur ait cliqué
            
            # Schedule bracket creation in main thread
            self.master.after(100, create_and_show_bracket)
                
        except Exception as e:
            self.logger.error(f"Error showing transition popup: {e}")
            self._prepare_next_match()

    def handle_tournament_match_end(self):
        if not self.handling_tournament_end:
            self.handling_tournament_end = True
            
            state = self.store.get_state()
            current_match = self.tournament_manager.bracket_manager.matches[
                self.tournament_manager.bracket_manager.current_match_id
            ]
            
            # Construction des stats cohérentes avec la structure de Duel
            is_second_game = current_match.duel.current_game == 2
            red_team = current_match.team2 if is_second_game else current_match.team1
            blue_team = current_match.team1 if is_second_game else current_match.team2

            winner_name = state['winner'].name if state['winner'] else None
            
            # Handle GameEndReason formatting
            reason = state["reason"]
            if isinstance(reason, GameEndReason):
                if winner_name and "{color}" in reason.value:
                    formatted_reason = reason.value.format(color=winner_name)
                else:
                    formatted_reason = reason.value
            else:
                formatted_reason = str(reason)
            
            stats = {
                "winner": winner_name,  # "RED" ou "BLUE"
                "RED_pieces": state["board"].count_soldiers(Soldier.RED),
                "BLUE_pieces": state["board"].count_soldiers(Soldier.BLUE),
                "RED_time": state["time_manager"].get_remaining_time(Soldier.RED),
                "BLUE_time": state["time_manager"].get_remaining_time(Soldier.BLUE),
                "RED_moves": get_move_player_count(state["history"], Soldier.RED),
                "BLUE_moves": get_move_player_count(state["history"], Soldier.BLUE),
                "reason": formatted_reason
            }
            
            self.tournament_manager.record_match_result(stats)
            self.show_transition_popup(current_match)

    def _prepare_next_match(self):
        """Prepare next match"""
        try:
            # Sécuriser la destruction des objets d'interface
            try:
                if self.after_game_view:
                    if hasattr(self.after_game_view, 'grab_release'):
                        self.after_game_view.grab_release()
                    self.after_game_view.destroy()
                    self.after_game_view = None
            except Exception as e:
                self.logger.error(f"Error cleaning up AfterGameView: {e}")

            # Reste de la méthode inchangé
            self.game_runner.cleanup(level='match')
            
            if hasattr(self, 'game_board'):
                self.game_board.reset_game()
            if hasattr(self, 'history_view'):
                self.history_view.clear_moves()
            
            self.handling_tournament_end = False
            self.store.dispatch({"type": "RESTART_GAME"})
            
            next_match = self.tournament_manager.setup_next_match()
            if next_match:
                self.match_start_time = datetime.now()
                self._configure_match_agents(next_match)
                self.game_runner.start()
            else:
                self.end_tournament()
                
        except Exception as e:
            self.logger.error(f"Error preparing next match: {e}")
            self.handling_tournament_end = False

    def _configure_match_agents(self, match_info):
        """Configure agents for the next match"""
        current_match = self.tournament_manager.bracket_manager.matches[
            self.tournament_manager.bracket_manager.current_match_id
        ]
        
        print(f"\n=== Configuring Match {current_match.id} Game {current_match.duel.current_game} ===")
        print(f"Teams: {current_match.team1} vs {current_match.team2}")
        print(f"RED: {match_info['red_agent']}, BLUE: {match_info['blue_agent']}")
        
        # Configure Red agent using TEAMS_MAPPING for file names
        self.store.dispatch({
            "type": "SELECT_AGENT",
            "soldier_value": Soldier.RED,
            "info_index": f"{TEAMS_MAPPING[match_info['red_agent']]}_{Soldier.RED.name}"
        })
        
        # Configure Blue agent using TEAMS_MAPPING for file names
        self.store.dispatch({
            "type": "SELECT_AGENT",
            "soldier_value": Soldier.BLUE,
            "info_index": f"{TEAMS_MAPPING[match_info['blue_agent']]}_{Soldier.BLUE.name}"
        })

    def end_tournament(self):
        """End tournament"""
        self.game_runner.cleanup(level='full')
        self.tournament_mode = False

        self.tournament_manager = None
        self.match_start_time = None
        
        show_popup(
            "Tournament completed.\nResults have been saved.",
            "Tournament End" 
        )

        
        try:
            def show_final_bracket():
                fig = create_tournament_bracket()
                plt.tight_layout()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"bracket_final_{timestamp}.png"
                filepath = self.brackets_dir / filename
                fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
                plt.close(fig)
                
                self.tournament_manager = None
                self.match_start_time = None
                
                show_popup(
                    f"Tournament completed.\nResults have been saved.\nBracket saved as: {filename}",
                    "Tournament End"
                )
                self.return_to_home()
                
            # Schedule final bracket creation in main thread
            self.master.after(100, show_final_bracket)
            
        except Exception as e:
            self.logger.error(f"Error displaying/saving final bracket: {e}")
            self.return_to_home()

    def start_tournament(self):
        """Initialize and start a new double elimination tournament"""
        try:
            self.tournament_mode = True
            print("\n=== Initializing Tournament ===")
            self.tournament_manager = DoubleEliminationManager(self.tournament_dir)
            
            if len(TEAMS) != 8:
                raise ValueError(f"Tournament requires exactly 8 teams, got {len(TEAMS)}")
                
            self.tournament_manager.start_tournament(TEAMS)
            self._prepare_next_match()
            
        except Exception as e:
            self.logger.error(f"Error starting tournament: {e}")
            show_popup(str(e), "Tournament Error")
            self.tournament_mode = False
            self.return_to_home()




