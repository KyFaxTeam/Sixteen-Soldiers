from typing import Any
import time
from agents.base_agent import BaseAgent

class GameRunner:
    def __init__(self, store: Any):
        self.store = store

    def run_player_game(self, agent1: BaseAgent, agent2: BaseAgent, delay: float = 0.6):
        """
        Run a game between two AI agents with time control
        
        Args:
            agent1: First agent (red player)
            agent2: Second agent (green player)
            delay: Delay between moves for visualization
            time_limit: Time limit per player in seconds (default 10 minutes)
        """
        # Initialize game and time control
        self.store.dispatch({"type": "INITIALIZE_GAME"})
        
        
        while not self.store.get_state().get("game_over", False):
            # Check if the game is paused
            while self.store.get_state().get("is_game_paused", False):
                time.sleep(0.1)  # Pause execution briefly
                
            current_state = self.store.get_state()
            current_player = current_state["players"][current_state.get("current_player_index", 0)]
            current_agent = agent1 if current_player.id == agent1.player.id else agent2
            
            # Record start time for the move
            start_time = time.time()
            
            try:
                # Get and execute agent's action
                action = current_agent.choose_action(board=current_state["board"])
                print(action)
                
                self.store.dispatch(action)
                
                # Calculate elapsed time and update time manager
                elapsed_time = time.time() - start_time
                self.store.dispatch({
                    "type": "UPDATE_TIME",
                    "player_id": current_player.id,
                    "elapsed_time": elapsed_time
                })
                
                # Check for timeout
                remaining_time = current_state["time_manager"].get_remaining_time(current_player.id)
                if remaining_time <= 0:
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
                
            except Exception as error:
                raise Exception(error)
                # print(f"Error : {error}")
                # break

