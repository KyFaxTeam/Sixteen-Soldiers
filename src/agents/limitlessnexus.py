import random
import numpy as np
from typing import Dict, List, Tuple
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier
import time
import pickle
import os

class Agent(BaseAgent):

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Limitless Nexus"
        self.opponent = Soldier.BLUE if soldier_value == Soldier.RED else Soldier.RED
        self.has_made_first_move = False
        

        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.1
        self.q_table = {}
        self.load_q_table()
        
        self.piece_values = {
            'center': ['d2', 'd3', 'd4', 'e2', 'e3', 'e4'],
            'semi_center': ['c2', 'c3', 'c4', 'f2', 'f3', 'f4'],
        }

    def get_state_key(self, board: Board) -> str:
        state = []
        for pos in sorted(board.soldiers.keys()):
            state.append(str(board.soldiers[pos].value))
        return "_".join(state)

    def get_action_key(self, action: Dict) -> str:
        return f"{action['from_pos']}_{action['to_pos']}"

    def save_q_table(self):
        try:
            with open(f'q_table_{self.soldier_value.name}.pkl', 'wb') as f:
                pickle.dump(self.q_table, f)
        except Exception as e:
            print(f"Error saving Q-table: {e}")

    def load_q_table(self):
        try:
            if os.path.exists(f'q_table_{self.soldier_value.name}.pkl'):
                with open(f'q_table_{self.soldier_value.name}.pkl', 'rb') as f:
                    self.q_table = pickle.load(f)
        except Exception as e:
            print(f"Error loading Q-table: {e}")

    def get_q_value(self, state_key: str, action_key: str) -> float:
        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        if action_key not in self.q_table[state_key]:
            self.q_table[state_key][action_key] = 0.0
        return self.q_table[state_key][action_key]

    def update_q_value(self, state_key: str, action_key: str, reward: float, next_state_key: str):
        current_q = self.get_q_value(state_key, action_key)

        if next_state_key in self.q_table:
            next_max_q = max(self.q_table[next_state_key].values(), default=0)
        else:
            next_max_q = 0

        new_q = current_q + self.alpha * (reward + self.gamma * next_max_q - current_q)
        

        if state_key not in self.q_table:
            self.q_table[state_key] = {}
        self.q_table[state_key][action_key] = new_q

    def get_reward(self, board: Board, action: Dict) -> float:

        reward = 0
        

        if action['type'] == 'CAPTURE_SOLDIER':
            reward += 10
        

        if action['to_pos'] in self.piece_values['center']:
            reward += 5
        elif action['to_pos'] in self.piece_values['semi_center']:
            reward += 3
            

        board_copy = Board()
        board_copy.soldiers = board.soldiers.copy()
        if action['type'] == 'CAPTURE_SOLDIER':
            board_copy.capture_soldier(action)
        else:
            board_copy.move_soldier(action)
            
        if board_copy.is_game_over() == self.soldier_value:
            reward += 100
        elif board_copy.is_game_over() == self.opponent:
            reward -= 100
            
        my_pieces = len(board_copy.get_soldier_positions(self.soldier_value))
        opponent_pieces = len(board_copy.get_soldier_positions(self.opponent))
        reward += (my_pieces - opponent_pieces) * 5
        
        return reward

    def choose_action(self, board: Board) -> Dict:
        valid_actions = board.get_valid_actions()
        

        if self.soldier_value == Soldier.RED and board.last_action is None:
            initial_moves = [
                {'from_pos': 'd2', 'to_pos': 'e1'},
                {'from_pos': 'd4', 'to_pos': 'e5'}
            ]
            for move in initial_moves:
                matching_action = next(
                    (action for action in valid_actions 
                     if action['from_pos'] == move['from_pos'] 
                     and action['to_pos'] == move['to_pos']), 
                    None
                )
                if matching_action:
                    return matching_action


        elif self.soldier_value == Soldier.BLUE and not self.has_made_first_move:
            initial_moves = [
                {'from_pos': 'f2', 'to_pos': 'e1'},
                {'from_pos': 'f4', 'to_pos': 'e5'}
            ]
            for move in initial_moves:
                matching_action = next(
                    (action for action in valid_actions 
                     if action['from_pos'] == move['from_pos'] 
                     and action['to_pos'] == move['to_pos']), 
                    None
                )
                if matching_action:
                    self.has_made_first_move = True
                    return matching_action
            self.has_made_first_move = True


        capture_actions = [action for action in valid_actions if action['type'] == 'CAPTURE_SOLDIER']
        if len(capture_actions) == 1:
            return capture_actions[0]


        state_key = self.get_state_key(board)


        if random.random() < self.epsilon:
            # Exploration: choose random action
            chosen_action = random.choice(valid_actions)
        else:

            best_q_value = float('-inf')
            best_actions = []
            
            for action in valid_actions:
                action_key = self.get_action_key(action)
                q_value = self.get_q_value(state_key, action_key)
                
                if q_value > best_q_value:
                    best_q_value = q_value
                    best_actions = [action]
                elif q_value == best_q_value:
                    best_actions.append(action)
            
            # If Q-values aren't helpful, use Minimax
            if best_q_value == 0 or not best_actions:
                start_time = time.time()
                try:
                    best_action = random.choice(valid_actions)
                    for depth in range(1, 3):
                        _, action = self.minimax(board, depth, float('-inf'), float('inf'),
                                               True, start_time, 0.5)
                        if action:
                            best_action = action
                except TimeoutError:
                    pass
            else:
                best_action = random.choice(best_actions)
            
            chosen_action = best_action


        reward = self.get_reward(board, chosen_action)

        board_copy = Board()
        board_copy.soldiers = board.soldiers.copy()
        if chosen_action['type'] == 'CAPTURE_SOLDIER':
            board_copy.capture_soldier(chosen_action)
        else:
            board_copy.move_soldier(chosen_action)
        
        next_state_key = self.get_state_key(board_copy)
        self.update_q_value(state_key, self.get_action_key(chosen_action), reward, next_state_key)
        

        if random.random() < 0.1:
            self.save_q_table()

        return chosen_action


    def minimax(self, board: Board, depth: int, alpha: float, beta: float, 
                is_maximizing: bool, start_time: float, max_time: float) -> Tuple[float, Dict]:

        if time.time() - start_time > max_time * 0.95:
            raise TimeoutError


        if depth == 0 or board.is_game_over():
            return self.evaluate_position(board), None


        valid_actions = board.get_valid_actions()
        if not valid_actions:
            return self.evaluate_position(board), None


        valid_actions.sort(key=lambda x: 1 if x['type'] == 'CAPTURE_SOLDIER' else 0, reverse=True)

        best_action = None

        if is_maximizing:
            max_eval = float('-inf')
            for action in valid_actions:
                # Simulation du coup
                board_copy = Board()
                board_copy.soldiers = board.soldiers.copy()
                if action['type'] == 'CAPTURE_SOLDIER':
                    board_copy.capture_soldier(action)
                else:
                    board_copy.move_soldier(action)

                eval, _ = self.minimax(board_copy, depth - 1, alpha, beta, False, start_time, max_time)

                if eval > max_eval:
                    max_eval = eval
                    best_action = action

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_action
        else:
            min_eval = float('inf')
            for action in valid_actions:
                # Simulation du coup
                board_copy = Board()
                board_copy.soldiers = board.soldiers.copy()
                if action['type'] == 'CAPTURE_SOLDIER':
                    board_copy.capture_soldier(action)
                else:
                    board_copy.move_soldier(action)

                eval, _ = self.minimax(board_copy, depth - 1, alpha, beta, True, start_time, max_time)

                if eval < min_eval:
                    min_eval = eval
                    best_action = action

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_action

    def evaluate_position(self, board: Board) -> float:
        # Vérification de fin de partie
        winner = board.is_game_over()
        if winner == self.soldier_value:
            return float('inf')
        elif winner == self.opponent:
            return float('-inf')

        score = 0

        # Nombre de pièces
        my_pieces = len(board.get_soldier_positions(self.soldier_value))
        opponent_pieces = len(board.get_soldier_positions(self.opponent))
        score += (my_pieces - opponent_pieces) * 100

        # Bonus pour le contrôle du centre
        for pos in self.piece_values['center']:
            if board.get_soldier_value(pos) == self.soldier_value:
                score += 30
            elif board.get_soldier_value(pos) == self.opponent:
                score -= 30

        # Bonus pour le contrôle des positions semi-centrales
        for pos in self.piece_values['semi_center']:
            if board.get_soldier_value(pos) == self.soldier_value:
                score += 15
            elif board.get_soldier_value(pos) == self.opponent:
                score -= 15


        board.last_action = None
        my_mobility = len(board.get_valid_actions())
        score += my_mobility * 5

        # Protection des pièces
        for pos in board.get_soldier_positions(self.soldier_value):
            neighbors = board.get_neighbors(pos)
            friendly_neighbors = len(neighbors[self.soldier_value.name])
            enemy_neighbors = len(neighbors[self.opponent.name])
            score += friendly_neighbors * 10 - enemy_neighbors * 15

        return score
