from copy import deepcopy
from logging import getLogger
import time
import random
import tkinter as tk
from utils.validator import is_valid_move
from agents.base_agent import BaseAgent
from store.store import Store
from utils.const import Soldier, TIMINGS


class GameRunner:
    def __init__(self, store: Store):
        self.store = store
        self.logger = getLogger(__name__)

    def _show_invalid_move_popup(self, agent_name):
        """Show a popup when agent makes an invalid move"""
        popup = tk.Toplevel()
        popup.title("Invalid Move")
        
        # Center the popup
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        popup.geometry(f"300x100+{(screen_width-300)//2}+{(screen_height-100)//2}")
        
        msg = f"Invalid move by {agent_name}\nUsing random move instead"
        label = tk.Label(popup, text=msg, pady=20)
        label.pack()
        
        # Auto-close after 2 seconds
        popup.after(2000, popup.destroy)

    def _conclude_game(self, agent1: BaseAgent, agent2: BaseAgent, winner: Soldier = None, reason: str = ""):
        """Handle game conclusion and stats updates"""
        final_state = self.store.get_state()
        time_manager = final_state.get('time_manager')
        total_moves = len(final_state.get('history', []))

        # Determine game outcome
        if winner is None:
            issue1, issue2 = 'draw', 'draw'
        elif winner == agent1.soldier_value:
            issue1, issue2 = 'win', 'loss'
        elif winner == agent2.soldier_value:
            issue1, issue2 = 'loss', 'win'
        else:
            self.logger.error("Mauvaise valeur de winner")
            issue1, issue2 = 'draw', 'draw'

        # Update agent stats
        if time_manager:
            agent1.conclude_game(issue1, opponent_name=agent2.name, 
                               number_of_moves=total_moves//2,
                               time=time_manager.get_remaining_time(agent1.soldier_value))
            agent2.conclude_game(issue2, opponent_name=agent1.name, 
                               number_of_moves=total_moves//2,
                               time=time_manager.get_remaining_time(agent2.soldier_value))
            
        # Update store with final stats
        self.store.register_agents(agent1, agent2)

        # Only dispatch END_GAME if not already game over
        if not final_state.get("is_game_over"):
            self.store.dispatch({
                "type": "END_GAME",
                "reason": reason,
                "winner": winner,
                "error": None
            })

    def run_game(self, agent1: BaseAgent, agent2: BaseAgent, delay: float = 0.5):
        """Run a game between two AI agents"""
        try:
            while not self.store.get_state().get("is_game_over", False):

                while self.store.get_state().get("is_game_paused", False):
                    time.sleep(0.1)  
                    
                current_state = self.store.get_state()
                current_soldier_value = current_state.get("current_soldier_value")
                current_agent: BaseAgent = agent1 if current_soldier_value == Soldier.RED else agent2

                try:
                    
                    start_time = time.time()
                    
                    # Get valid actions from board
                    board_copy = deepcopy(current_state["board"])
                    valid_actions = board_copy.get_valid_actions(current_soldier_value)
                    valid_actions = [action for action in valid_actions if is_valid_move(action, current_state["board"])]

                    if not valid_actions:
                        # si pas de mouvement possible, on décide de la fin du jeu, le current_soldier_value est le perdant
                        self.logger.info(f"No valid actions for {current_agent.name}")
                        self._conclude_game(agent1, agent2, winner=current_soldier_value, reason="no_moves")
                        return

                    action = current_agent.choose_action(board=board_copy)
                    
                    # Validate action and fallback to random if invalid
                    if not is_valid_move(action, current_state["board"]) or action not in valid_actions:
                        self.logger.warning(f"{current_agent.name} made invalid move, using random")
                        self._show_invalid_move_popup(current_agent.name)
                        action = random.choice(valid_actions)

                    elapsed_time = time.time() - start_time
                    
                    self.store.dispatch(action=action)

                    delay = self.store.game_speed.get_delay_time(elapsed_time)
                    time.sleep(delay)


                    
                    self.store.dispatch({
                        "type": "UPDATE_TIME",
                        "soldier_value": current_soldier_value,
                        "elapsed_time": elapsed_time
                    })

                    # Record the move in history
                    self.store.dispatch({
                        "type": "ADD_MOVE_TO_HISTORY",
                        "payload": {
                            "from_pos": action["from_pos"],
                            "to_pos": action["to_pos"],
                            "soldier_value": current_soldier_value,
                            "captured_soldier": action.get("captured_soldier"),
                            "timestamp": elapsed_time
                        }
                    })
                    
                    # Check for timeout using is_time_up
                    # ne pas déclencher la fin du jeu mais plutôt random
                    if current_state["time_manager"].is_time_up(current_soldier_value):
                        if current_soldier_value == Soldier.RED:
                            winner = Soldier.BLUE
                        else:
                            winner = Soldier.RED
                        self._conclude_game(agent1, agent2, winner=winner, reason="timeout")
                        break
                    
                    # Ajouter le changement de joueur
                    self.store.dispatch({"type": "CHANGE_CURRENT_SOLDIER"})

                    
                except Exception as e:
                    self.logger.exception(f"Game error: {e}")
                    self._conclude_game(agent1, agent2, winner=None, reason="error")
                    return  # Exit immediately after error END_GAME

            # Only dispatch END_GAME if we reached end of game normally
            # and game isn't already over
            self._conclude_game(agent1, agent2, winner=current_soldier_value)
            self.logger.info("Game over")

        except Exception as e:
            self.logger.exception(f"Fatal game error: {e}")

