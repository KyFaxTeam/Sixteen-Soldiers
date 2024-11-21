from typing import Any
import time
import logging
from agents.base_agent import BaseAgent
from store.store import Store

class GameRunner:
    def __init__(self, store: Store):
        self.store = store
        self.logger = logging.getLogger(__name__)

    def run_player_game(self, agent1: BaseAgent, agent2: BaseAgent, delay: float = 0.6):
        """
        Run a game between two AI agents
        """
        self.store.dispatch({"type": "INITIALIZE_GAME"})
        
        while not self.store.get_state().get("game_over", False):
            # Check if the game is paused
            while self.store.get_state().get("is_game_paused", False):
                time.sleep(0.1)  # Pause execution briefly
                
            current_state = self.store.get_state()
            current_player = current_state["players"][current_state.get("current_player")]
            current_agent = agent1 if current_player.id == agent1.player.id else agent2
            
            # Record start time for the move
            start_time = time.time()
            
            try:
                # Get and execute agent's action (removed time_limit parameter)
                action = current_agent.choose_action(board=current_state["board"])
                # Calculate elapsed time and update time manager
                elapsed_time = time.time() - start_time
                self.logger.debug(f"Agent action: {action}")

                if action['type'] == 'NO_OP':
                    self.logger.info(f"{current_agent.name} has no valid moves. Ramdom_agent action.")
                    # ici implémenter le random dans les actions disponibles ou plus simple appeler la fonction choose_action de Random
                   # self.store.dispatch({'type': 'PASS_TURN', 'player_id': current_player.id})


                   # Say bro, at the end here, you return a random 'action' variable, right ?

                else:
                    # Validate the action
                    if not current_state["board"].is_valid_move(action):
                        raise ValueError("Agent attempted an invalid move")
                    # Dispatch the action - board_reducer and player_reducer will both handle it
                    self.store.dispatch(action)
                
                self.store.dispatch({
                    "type": "UPDATE_TIME",
                    "player_id": current_player.id,
                    "elapsed_time": elapsed_time
                })

                # Record the move in history
                self.store.dispatch({
                    "type": "ADD_MOVE_TO_HISTORY",
                    "payload": {
                        "from_pos": action["from"],
                        "to_pos": action["to"],
                        "player_id": current_player.id,
                        "piece_capturee": action.get("piece_capturee"),
                        "timestamp": elapsed_time
                    }
                })
                            
                
                # Check for timeout using is_time_up
                if current_state["time_manager"].is_time_up(current_player.id):
                    self.store.dispatch({
                        "type": "END_GAME",
                        "reason": "timeout",
                        "loser": current_player.id
                    })
                    break
                
                # Ajouter le changement de joueur
                self.store.dispatch({"type": "CHANGE_CURRENT_PLAYER"})
                
                # Add delay for visualization
                time.sleep(delay)
                
                
                
            except Exception as e:
                self.logger.error(f"Error occurred during agent's turn: {e}")
                self.store.dispatch({
                    "type": "END_GAME",
                    "reason": "error",
                    "loser": current_player.id,
                    "error": str(e)
                })
                break

        self.logger.info("Game over")
        
        # Determine the winner and update agent stats
        winner_id = self.store.get_state().get("winner", {}).get("id")
        total_number_of_moves = len(self.store.get_state().get('history', []))
        match_times = self.store.get_state().get('time_manager', [])
        agent1.conclude_game(is_wwinner=(agent1.player.id == winner_id), opponent_name=agent2.name, number_of_moves=total_number_of_moves//2, time=match_times.get_remaining_time(agent1.player.id))
        agent2.conclude_game(is_winner=(agent2.player.id == winner_id), opponent_name=agent1.name, number_of_moves=total_number_of_moves//2, time=match_times.get_remaining_time(agent2.player.id))
        
        # Update agent info in the store after game ends
        self.store.register_agent(agent1)
        self.store.register_agent(agent2)
