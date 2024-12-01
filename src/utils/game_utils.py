from copy import deepcopy
from logging import getLogger
import time
import random
import tkinter as tk
from utils.history_utils import get_move_player_count
from utils.validator import is_valid_move
from agents.base_agent import BaseAgent
from store.store import Store
from utils.const import Soldier, TIMINGS




def show_invalid_move_popup(agent_name):
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
    
    # Auto-close after 5 seconds
    popup.after(5000, popup.destroy)

class GameRunner:
    def __init__(self, store: Store):
        self.store = store
        self.logger = getLogger(__name__)
          
    def run_game(self, agent1: BaseAgent, agent2: BaseAgent, delay: float = 0.5):
        """Run a game between two AI agents"""

        can_continue_capture = False

        while not self.store.get_state().get("is_game_over", False):

            while self.store.get_state().get("is_game_paused", False):
                time.sleep(0.1)  
                
            current_state = self.store.get_state()
            current_soldier_value = current_state.get("current_soldier_value")
            current_agent: BaseAgent = agent1 if current_soldier_value == Soldier.RED else agent2
            opponent_agent: BaseAgent = agent2 if current_soldier_value == Soldier.RED else agent1
            over = current_state["board"].is_game_over()

            if over is not None:
                self.logger.info(f"No soldiers to move for {current_agent.name}")
                winner = over
                reason = "no_soldiers"
                break
            try:
                board_copy = deepcopy(current_state["board"])
                if can_continue_capture : 
                    valid_actions = board_copy.get_available_captures(current_soldier_value, action["to_pos"])
                else : 
                    valid_actions = board_copy.get_valid_actions(current_soldier_value)

                valid_actions = [action for action in valid_actions if is_valid_move(action, current_state["board"])]

                if not valid_actions:
                    # No valid actions for current player means the opponent wins
                    self.logger.info(f"No valid actions for {current_agent.name}")
                    winner = opponent_agent.soldier_value
                    reason = "no_valid_actions"
                    break
                
                if current_state["time_manager"].is_time_up(current_soldier_value):
                    self.logger.info(f"Player {current_agent.name} ran out of time using random move")
                    self._show_invalid_move_popup(current_agent.name)
                    action = random.choice(valid_actions)
                else:
                    start_time = time.perf_counter()
                    action = current_agent.choose_action(board=board_copy)
                    elapsed_time = time.perf_counter() - start_time

                # Validate action and fallback to random if invalid
                if not is_valid_move(action, current_state["board"]) and action not in valid_actions:
                        self.logger.warning(f"{current_agent.name} made invalid move, using random")
                        self._show_invalid_move_popup(current_agent.name)
                        action = random.choice(valid_actions)
                
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
                        "captured_soldier": action.get("captured_soldier", None),
                        "timestamp": elapsed_time, 
                        "capture_multiple": can_continue_capture
                    }
                })
                
                # Vérifier si des captures sont disponibles pour le joueur actuel
                board = self.store.get_state()["board"]

                can_continue_capture = action['type'] == "CAPTURE_SOLDIER" and board.get_available_captures(current_soldier_value, action["to_pos"], True)

                if can_continue_capture :     
                    self.logger.info(f"Player {current_agent.name} has additional captures available.")
                    continue  # Ne pas changer le joueur et permettre au joueur actuel de rejouer
                else:
                    # Passer au joueur suivant s'il n'y a pas de captures
                    self.store.dispatch({"type": "CHANGE_CURRENT_SOLDIER"})
 
            except Exception as e:
                self.logger.exception(f"Game error: {e}")
                self._conclude_game(agent1, agent2, winner=None, reason="error")
                break  

        
        self._conclude_game(agent1, agent2, winner=winner, reason=reason)
        self.logger.info("Game over")


    def _conclude_game(self, agent1: BaseAgent, agent2: BaseAgent, winner: Soldier = None, reason: str = ""):
        """Handle game conclusion and stats updates"""
        final_state = self.store.get_state()
        time_manager = final_state.get('time_manager')
        total_moves_agent1 = get_move_player_count(final_state, agent1.soldier_value)
        total_moves_agent2 = get_move_player_count(final_state, agent2.soldier_value)

        # Determine game outcome
        if winner is None:
            issue1, issue2 = 'draw', 'draw'
        elif winner == agent1.soldier_value:
            issue1, issue2 = 'win', 'loss'
        elif winner == agent2.soldier_value:
            issue1, issue2 = 'loss', 'win'
        else:
            issue1, issue2 = 'draw', 'draw'
            raise ValueError("Invalid winner value in _conclude_game")
            

        # Update agent stats
        agent1.conclude_game(issue1, opponent_name=agent2.name, 
                               number_of_moves=total_moves_agent1,
                               time=time_manager.get_remaining_time(agent1.soldier_value))
            
        agent2.conclude_game(issue2, opponent_name=agent1.name, 
                               number_of_moves=total_moves_agent2,
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
