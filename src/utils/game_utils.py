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
from src.utils.const import MAX_MOVES_WITHOUT_CAPTURE, Soldier
from src.utils.const import GameEndReason
from enum import Enum

def show_popup(message: str, title: str = "Message", auto_close: bool = True, duration: int = 1500, modal: bool = False):
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
        option_1="OK",  # Un seul bouton par défaut
        border_width=1,  # Bordure fine
    )
    
    if auto_close:
        popup.after(duration, popup.destroy)

    if modal:
        popup.wait_window()
class GameMode(Enum):
    REPLAY = 'replay'
    GAME = 'game'
    NONE = None

class GameRunner:
    def __init__(self, store: Store):
        self.store = store
        self.logger = getLogger(__name__)
        self.moves_without_capture = 0
        self.game_mode = GameMode.NONE
        self.game_data = None
        self.agents = None
        self.is_prepared = False

    def cleanup(self, level: str = 'else'):
        """Nettoie l'état du GameRunner"""
        self.agents = None
        self.is_prepared = False
        self.moves_without_capture = 0
        # Note: game_mode and game_data are now preserved
        if level == 'full':
            self.game_data = None
            self.game_mode = None
            
    def set_mode(self, mode: str, data=None):
        """Configure le mode de jeu (replay ou nouveau jeu)"""
        self.cleanup()  # Nettoie l'état avant de changer de mode
        self.game_mode = GameMode(mode)
        # Update store with game mode
        self.store.state["game_mode"] = self.game_mode.value
        if mode == 'replay':
            self.game_data = data
            return self.initialize_replay(data)
        return True

    def can_start(self) -> bool:
        """Vérifie si le jeu peut démarrer"""
        if not self.game_mode:
            return False
            
        if self.game_mode == GameMode.REPLAY:
            return bool(self.game_data)
        return True  # Pour le mode GAME, on retourne toujours True car prepare_agents gère l'initialisation

    def prepare_agents(self) -> bool:
        """Prépare les agents pour le jeu"""
        try:
            if not self.game_mode:
                self.logger.error("Invalid game mode")
                return False

            # Pour le mode replay, on vérifie qu'on a les données nécessaires
            if self.game_mode == GameMode.REPLAY and not self.game_data:
                self.logger.error("No replay data available")
                return False

            agents_info = self.store.get_state().get("agents_info_index", {})
            

            # On initialise toujours les agents par défaut si nécessaire
            if not all(agents_info.values()):
                for soldier_value in [Soldier.RED, Soldier.BLUE]:
                    if not agents_info.get(soldier_value):
                        ai = "main_ai" if soldier_value == Soldier.RED else "random_agent"
                        agent_id = f"{ai}_{soldier_value.name}" 
                        agents_info[soldier_value] = agent_id

            def create_agent(soldier_value):
                agent_id = agents_info[soldier_value]
                agent_type = agent_id.rsplit('_', 1)[0]
                agent_module = __import__(f"src.agents.{agent_type}", fromlist=['Agent'])
                # print("module", agent_module)
                return agent_module.Agent(
                    soldier_value=soldier_value,
                    data=None if not self.game_data else self.game_data["metadata"]["agents"].get(agent_id, None)
                )
            

            agent1 = create_agent(Soldier.RED)
            agent2 = create_agent(Soldier.BLUE)
            self.store.register_agents(agent1, agent2)
            self.agents = (agent1, agent2)
            self.is_prepared = True
            return True
        except Exception as e:
            self.logger.error(f"Error preparing agents: {e}")
            return False

    def start(self):
        """Démarre le jeu si tout est prêt"""
        if not self.is_prepared and not self.prepare_agents():
            self.logger.error("Agent preparation failed")
            return False
            
        self.store.dispatch({"type": "INIT_GAME"})
                    
        def run():
            if self.game_mode == GameMode.REPLAY:
                self.replay_game(self.game_data)
            else:
                self.run_game(*self.agents)

        import threading
        game_thread = threading.Thread(target=run)
        game_thread.daemon = True
        game_thread.start()
        return True
          
    def run_game(self, agent1: BaseAgent, agent2: BaseAgent, delay: float = 0.5):
        """Run a game between two AI agents"""
       
        timeout = {"RED": False, "BLUE": False}
        winner, reason = None, None
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
                reason = GameEndReason.NO_SOLDIERS
                break
            try:

                valid_actions = board.get_valid_actions()

                valid_actions = [action for action in valid_actions if is_valid_move(action, board)]

                if not valid_actions:
                    self.logger.info(f"No valid actions for {current_agent.name}")
                    winner = opponent_agent.soldier_value
                    reason = GameEndReason.NO_VALID_MOVES
                    break
                
                if current_state["time_manager"].is_time_up(current_soldier_value):

                    msg = f"Player {current_agent.name} ran out of time. \n \nNext moves of Soldier {current_agent.soldier_value.name} will be done by random."
     
                    if not timeout[current_soldier_value.name] :
                        show_popup(msg, "Time up")
                        timeout[current_soldier_value.name] = True

                    action = random.choice(valid_actions)
                    elapsed_time = 0.0
                else:
                    board_copy = deepcopy(board)
                    
                    start_time = time.perf_counter()
                    try:
                        action = current_agent.choose_action(board=board_copy)
                    except Exception as e:
                        self.logger.error(f'Error while choosing action: {e}')
                        reason = 'crash'
                        winner = opponent_agent.soldier_value
                        # print('********', winner, reason)
                        break
                    elapsed_time = time.perf_counter() - start_time

                if not is_valid_move(action, current_state["board"]) and action not in valid_actions:
                    msg = f"{current_agent.name} made invalid move, using random"
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

               
                if self.moves_without_capture >= MAX_MOVES_WITHOUT_CAPTURE:
                    red_pieces = board.count_soldiers(Soldier.RED)
                    blue_pieces = board.count_soldiers(Soldier.BLUE)
                    
                    if red_pieces <= 3 and blue_pieces <= 3 or red_pieces == blue_pieces:
                        winner = None
                        reason = GameEndReason.DRAW_FEW_PIECES
                    else:
                        if red_pieces > blue_pieces:
                            winner = Soldier.RED
                        elif blue_pieces > red_pieces:
                            winner = Soldier.BLUE
                        reason = GameEndReason.MORE_PIECES_WINS
                    break
                if action.get("captured_soldier") is None:
                    # print(f"Move without capture - Counter: {self.moves_without_capture + 1}")
                    self.moves_without_capture += 1
                else:
                    # print("Capture detected - Resetting counter to 0")
                    self.moves_without_capture = 0
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
        total_moves_agent1 = get_move_player_count(final_state['history'], agent1.soldier_value)
        total_moves_agent2 = get_move_player_count(final_state['history'], agent2.soldier_value)
        remain_soldiers_agent1 = final_state.get("board").count_soldiers(agent1.soldier_value)
        remain_soldiers_agent2 = final_state.get("board").count_soldiers(agent2.soldier_value)
        margin = abs(remain_soldiers_agent1 - remain_soldiers_agent2)


        if winner is None:
            issue1, issue2 = 'draw', 'draw'
        elif winner == agent1.soldier_value:
            issue1, issue2 = 'win', 'loss'
        elif winner == agent2.soldier_value:
            issue1, issue2 = 'loss', 'win'
        else:
            issue1, issue2 = 'draw', 'draw'
            self.logger.error(f"Invalid winner: {winner}")

            
        if not reason:
            if winner is None:
                reason = "draw"
            elif winner == agent1.soldier_value:
                reason = "victory"
            elif winner == agent2.soldier_value:
                reason = "victory"
        agent1.conclude_game(
            issue1,
            opponent_name=agent2.name,
            number_of_moves=total_moves_agent1,
            time=time_manager.get_remaining_time(agent1.soldier_value),
            reason=reason,  # Pass 'reason' to conclude_game
            margin=(margin if issue1 == 'win' else -margin if issue1 == 'loss' else 0)
        )
        agent2.conclude_game(
            issue2,
            opponent_name=agent1.name,
            number_of_moves=total_moves_agent2,
            time=time_manager.get_remaining_time(agent2.soldier_value),
            reason=reason,  # Pass 'reason' to conclude_game   margin=(margin if issue2 == 'win' else -margin if issue2 == 'loss' else 0)
            margin=(margin if issue2 == 'win' else -margin if issue2 == 'loss' else 0)
        )        
            
        self.store.register_agents(agent1, agent2)
        # Format reason with winner color if applicable
        if isinstance(reason, GameEndReason) and winner:
            color = winner.name
            reason = reason.value.format(color=color)
            
        if not final_state.get("is_game_over"):
            # print("END game conclude_game")
            self.store.dispatch({
                "type": "END_GAME",
                "reason": reason,
                "winner": winner,
                "error": None
            })

    def initialize_replay(self, game_data: dict):
        """Initialize the store with the game data for replay"""
        try:
            metadata = game_data.get('metadata', {})
            agents_info_index = metadata.get('agents_info_index', {})

            if agents_info_index and all(isinstance(k, Soldier) for k in agents_info_index.keys()):
                self.store.state["agents_info_index"] = agents_info_index
                self.store.state["agents"] = metadata.get('agents', {})
                self.store.state["winner"] = metadata.get('winner')
                self.logger.info(f"Replay initialized with agents: {agents_info_index}")
                return game_data.get('history', [])
            else:
                self.logger.error(f"Invalid agents_info_index format: {agents_info_index}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error initializing replay: {e}")
            return None

    def replay_game(self, game_data: dict, delay: float = 1.0):
        """Replay a saved game using the history of moves"""
        
        history = self.initialize_replay(game_data)
        
        if not history:
            return
            
        try:
            # Pré-traiter les actions sans modifier les données originales
            actions = []
            for move in history:
                positions = move["pos"]
                timestamps = move.get("timestamp", [])
                captured = move.get("captured_soldier", [])
                
                # Utiliser des indices au lieu de pop()
                for i in range(len(positions) - 1):
                    action = {
                        "type": "CAPTURE_SOLDIER" if captured else "MOVE_SOLDIER",
                        "from_pos": positions[i],
                        "to_pos": positions[i + 1],
                        "soldier_value": move["soldier_value"],
                        "timestamp": timestamps[i] if timestamps else 0
                    }
                    
                    if captured:
                        action["captured_soldier"] = captured[i]
                    actions.append(action)
            
            # Reste du code inchangé pour la boucle d'exécution des actions
            for action in actions:

                while self.store.get_state().get("is_game_paused", False):
                    time.sleep(0.1)
                    
                if self.store.get_state().get("is_game_leaved", False):
                    return
                
                self.store.dispatch(action)
                
                self.store.dispatch({
                    "type": "UPDATE_TIME",
                    "soldier_value": action["soldier_value"],
                    "elapsed_time": action["timestamp"]
                })

                self.store.dispatch({
                    "type": "ADD_MOVE_TO_HISTORY",
                    "payload": {
                        "from_pos": action["from_pos"],
                        "to_pos": action["to_pos"],
                        "soldier_value": action["soldier_value"],
                        "captured_soldier": action.get("captured_soldier", None),
                        "timestamp": action["timestamp"], 
                        "capture_multiple": False
                    }
                })
                
                self.store.dispatch({"type": "CHANGE_CURRENT_SOLDIER"})
                
                time.sleep(delay)
            
            if  self.store.state.get("winner"):
                # print("END game replay_game")
                self.store.dispatch({
                    "type": "END_GAME",
                    "winner": self.store.state.get("winner"),
                    "reason": "replay_completed"
                })
                
        except Exception as e:
            self.logger.exception(f"Replay error: {e}")
            # print("END game replay_game error")
            self.store.dispatch({
                "type": "END_GAME",
                "reason": "replay_error",
                "error": str(e)
            })


