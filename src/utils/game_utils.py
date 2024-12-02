from copy import deepcopy
from logging import getLogger
import time
import random
from CTkMessagebox import CTkMessagebox
from src.models.board import Board
from src.utils.history_utils import get_move_player_count
from src.utils.validator import is_valid_move
from src.agents.base_agent import BaseAgent
from src.store.store import Store
from src.utils.const import MAX_MOVES_WITHOUT_CAPTURE, Soldier, TIMINGS


def show_popup(message: str, title: str = "Message", auto_close: bool = True, duration: int = 2000):
    """Show a popup message using CTkMessagebox that auto-closes after duration milliseconds."""
    popup = CTkMessagebox(
        title=title,
        message=message,
        icon="info",
        width=250,
        height=150,
        font=("Roboto", 12),
        justify="center",
        fade_in_duration=0.2,
    )
    
    if auto_close:
        popup.after(duration, popup.destroy)

class GameRunner:
    def __init__(self, store: Store):
        self.store = store
        self.logger = getLogger(__name__)
        self.moves_without_capture = 0  
          
    def run_game(self, agent1: BaseAgent, agent2: BaseAgent, delay: float = 0.5):
        """Run a game between two AI agents"""
       
        timeout = {"RED": False, "BLUE": False}
        while not self.store.get_state().get("is_game_over", False) and not self.store.get_state().get("is_game_leaved", False):
            
            while self.store.get_state().get("is_game_paused", False):
                time.sleep(0.1)

            if self.store.get_state().get("is_game_leaved", False):
                return
               
            current_state = self.store.get_state()
            board : Board = current_state["board"]

            current_soldier_value = current_state.get("current_soldier_value")
            current_agent: BaseAgent = agent1 if current_soldier_value == Soldier.RED else agent2
            opponent_agent: BaseAgent = agent2 if current_soldier_value == Soldier.RED else agent1
            over = board.is_game_over()
            is_multi_capture = board.is_multiple_capture


            if over is not None:
                self.logger.info(f"No soldiers to move for {current_agent.name}")
                winner = over
                reason = "no_soldiers"
                break
            try:

                valid_actions = board.get_valid_actions()

                valid_actions = [action for action in valid_actions if is_valid_move(action, board)]

                if not valid_actions:
                    # No valid actions for current player means the opponent wins
                    self.logger.info(f"No valid actions for {current_agent.name}")
                    winner = opponent_agent.soldier_value
                    reason = "no_valid_actions"
                    break
                
                if current_state["time_manager"].is_time_up(current_soldier_value):

                    msg = f"Player {current_agent.name} ran out of time. \n \nNext moves of Soldier {current_agent.soldier_value.name} will be done by random."
     
                    # self.logger.info(msg)
                    if not timeout[current_soldier_value.name] :
                        show_popup(msg, "Time up")
                        timeout[current_soldier_value.name] = True

                    action = random.choice(valid_actions)
                    elapsed_time = 0.0
                else:
                    board_copy = deepcopy(board)
                    
                    start_time = time.perf_counter()
                    action = current_agent.choose_action(board=board_copy)
                    elapsed_time = time.perf_counter() - start_time

                # Validate action and fallback to random if invalid

                if not is_valid_move(action, current_state["board"]) and action not in valid_actions:
                    msg = f"{current_agent.name} made invalid move, using random"
                    # self.logger.warning(msg)
                    show_popup(msg, "Invalid move") 
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
                        "capture_multiple": is_multi_capture
                    }
                })
                
                self.store.dispatch({"type": "CHANGE_CURRENT_SOLDIER"})

                # Après l'action dispatch, mettre à jour le compteur
                if action.get("captured_soldier") is None:
                    self.moves_without_capture += 1
                else:
                    self.moves_without_capture = 0

                # Vérifier si on a atteint la limite de coups sans capture
                if self.moves_without_capture >= MAX_MOVES_WITHOUT_CAPTURE:
                    red_pieces = board.count_soldiers(Soldier.RED)
                    blue_pieces = board.count_soldiers(Soldier.BLUE)
                    
                    if red_pieces <= 3 and blue_pieces <= 3:
                        winner = None  # Match nul
                        reason = "draw_few_pieces"
                    else:
                        if red_pieces > blue_pieces:
                            winner = Soldier.RED
                        elif blue_pieces > red_pieces:
                            winner = Soldier.BLUE
                        else:
                            winner = None  # Match nul en cas d'égalité
                        reason = "more_pieces_wins"
                    break

            except Exception as e:
                self.logger.exception(f"Game error: {e}")
                self._conclude_game(agent1, agent2, winner=None, reason="error")
                break  

        
        if self.store.get_state().get("is_game_leaved"):
            self.logger.info("Game was left")
        else :
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
        print("***********************Reason", reason)
        # Only dispatch END_GAME if not already game over
        if not final_state.get("is_game_over"):
            self.store.dispatch({
                "type": "END_GAME",
                "reason": reason,
                "winner": winner,
                "error": None
            })