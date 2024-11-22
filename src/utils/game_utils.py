from logging import getLogger
import time
from utils.validator import is_valid_move
from agents.base_agent import BaseAgent
from store.store import Store
from utils.const import Soldier


class GameRunner:
    def __init__(self, store: Store):
        self.store :Store = store
        self.logger = getLogger(__name__)

    def run_game(self, agent1: BaseAgent, agent2: BaseAgent, delay: float = 0.5):
        """
        Run a game between two AI agents
        """
        while not self.store.get_state().get("is_game_over", False):
            # Check if the game is paused
            while self.store.get_state().get("is_game_paused", False):
                time.sleep(0.1)  # Pause execution briefly
                
            current_state = self.store.get_state()
            current_soldier_value = current_state.get("current_soldier_value")
            current_agent: BaseAgent = agent1 if current_soldier_value == Soldier.RED else agent2
            
            try:
                # Record start time for the move
                start_time = time.time()

                # Get and execute agent's action (removed time_limit parameter)
                action = current_agent.choose_action(board=current_state["board"])
                # Calculate elapsed time and update time manager
                elapsed_time = time.time() - start_time

                self.logger.debug(f"Agent action: {action}")

                if action is None:
                    self.logger.info(f"{current_agent.name} has no valid moves. Ramdom_agent action.")
                    # ici implémenter le random dans les actions disponibles ou plus simple appeler la fonction choose_action de Random

                   # Say bro, at the end here, you return a random 'action' variable, right ?
                     # So, you can just call the choose_action method of the Random agent and return it

                else:
                    if not is_valid_move(action, current_state["board"]):
                        raise ValueError("Agent attempted an invalid move")
                    self.store.dispatch(action)
                
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
                if current_state["time_manager"].is_time_up(current_soldier_value):
                    self.store.dispatch({
                        "type": "END_GAME",
                        "reason": "timeout",
                        "loser": current_soldier_value
                    })
                    break
                
                # Ajouter le changement de joueur
                self.store.dispatch({"type": "CHANGE_CURRENT_soldier_value"})
                # Add delay for visualization
                time.sleep(delay)
                
            except Exception as e:
                self.logger.error(f"Error occurred during agent's turn: {repr(e)}")
                self.store.dispatch({
                    "type": "END_GAME",
                    "reason": "error",
                    "loser": current_soldier_value,
                    "error": str(e)
                })
                break

        self.logger.info("Game over")
        
        # Determine the winner and update agent stats
        winner = self.store.get_state().get("winner")
        total_number_of_moves = len(self.store.get_state().get('history', []))
        match_times = self.store.get_state().get('time_manager', [])
        
        if winner is None:
            issue1 = 'draw'
            issue2 = 'draw'
        elif winner == agent1.pseudo:
            issue1 = 'win'
            issue2 = 'loss'
        else:
            issue1 = 'loss'
            issue2 = 'win'
        agent1.conclude_game(issue1, opponent_name=agent2.name, number_of_moves=total_number_of_moves//2, time=match_times.get_remaining_time(agent1.soldier_value))
        agent2.conclude_game(issue2, opponent_name=agent1.name, number_of_moves=total_number_of_moves//2, time=match_times.get_remaining_time(agent2.soldier_value))
        
        # Update agent info in the store after game ends
        self.store.register_agents(agent1, agent2) # il faudrait plutôt créer un game_actions et gérer ça
        # il faudrait plutôt créer un game_actions et gérer ça
        

    

        self.store.dispatch({"type": "RESET_GAME"})

    