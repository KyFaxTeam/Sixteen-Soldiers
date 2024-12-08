import random
import math
import time
from typing import Dict, Optional
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    """AI agent using Time-Aware Minimax with Alpha-Beta Pruning for Sholo Guti"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Time Strategist"
        self.max_time = 1  # Temps max autorisé (en secondes)
        self.start_time = None
    
    def choose_action(self, board: Board) -> Dict:
        """
        Chooses the best action with time constraint
        """
        valid_actions = board.get_valid_actions()
        
        # Priorité aux captures
        capture_actions = [action for action in valid_actions if action['type'] == 'CAPTURE_SOLDIER']
        if capture_actions:
            return random.choice(capture_actions)
        
        # Initialiser le temps
        self.start_time = time.perf_counter()
        
        # Essayer différentes profondeurs de recherche
        for depth in range(1, 10):
            best_action = self._time_constrained_minimax(board, depth)
            
            # Si un temps limite est dépassé, retourner l'action trouvée
            if best_action is not None:
                return best_action
        
        # Fallback si aucune action n'a été trouvée
        return random.choice(valid_actions)
    
    def _time_constrained_minimax(self, board: Board, depth: int) -> Optional[Dict]:
        """
        Minimax avec contrainte de temps
        
        Args:
            board: État du plateau
            depth: Profondeur de recherche
        
        Returns:
            Meilleure action ou None si temps dépassé
        """
        valid_actions = board.get_valid_actions()
        
        best_score = -math.inf
        best_action = None
        alpha = -math.inf
        beta = math.inf
        
        for action in valid_actions:
            # Vérifier le temps écoulé
            if time.perf_counter() - self.start_time > self.max_time:
                return best_action
            
            # Simuler l'action
            board_copy = board
            if action['type'] == 'CAPTURE_SOLDIER':
                board_copy.capture_soldier(action)
            else:
                board_copy.move_soldier(action)
            
            # Évaluer le score du prochain coup
            score = self._minimax(
                board_copy, 
                depth - 1, 
                False,  
                alpha, 
                beta, 
                self.soldier_value
            )
            
            # Mettre à jour le meilleur score et la meilleure action
            if score > best_score:
                best_score = score
                best_action = action
            
            # Mise à jour alpha
            alpha = max(alpha, best_score)
        
        return best_action
    
    def _minimax(self, 
                 board: Board, 
                 depth: int, 
                 is_maximizing: bool, 
                 alpha: float, 
                 beta: float, 
                 maximizing_soldier: Soldier) -> float:
        """
        Version optimisée de Minimax avec contrainte de temps
        """
        # Vérifier le temps écoulé
        if time.perf_counter() - self.start_time > self.max_time:
            return 0
        
        # Conditions de fin de récursion
        game_over = board.is_game_over()
        if depth == 0 or game_over is not None:
            return self._evaluate_board(board, maximizing_soldier)
        
        # Déterminer le soldat actuel
        current_soldier = Soldier.RED if is_maximizing else Soldier.BLUE
        valid_actions = board.get_valid_actions()
        
        if is_maximizing:
            max_eval = -math.inf
            for action in valid_actions:
                # Vérifier le temps
                if time.perf_counter() - self.start_time > self.max_time:
                    return max_eval
                
                # Simuler l'action
                board_copy = board
                if action['type'] == 'CAPTURE_SOLDIER':
                    board_copy.capture_soldier(action)
                else:
                    board_copy.move_soldier(action)
                
                # Évaluation récursive
                eval_score = self._minimax(
                    board_copy, 
                    depth - 1, 
                    False, 
                    alpha, 
                    beta, 
                    maximizing_soldier
                )
                
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                # Élagage alpha-bêta
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for action in valid_actions:
                # Vérifier le temps
                if time.perf_counter() - self.start_time > self.max_time:
                    return min_eval
                
                # Simuler l'action
                board_copy = board
                if action['type'] == 'CAPTURE_SOLDIER':
                    board_copy.capture_soldier(action)
                else:
                    board_copy.move_soldier(action)
                
                # Évaluation récursive
                eval_score = self._minimax(
                    board_copy, 
                    depth - 1, 
                    True, 
                    alpha, 
                    beta, 
                    maximizing_soldier
                )
                
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Élagage alpha-bêta
                if beta <= alpha:
                    break
            return min_eval
    
    def _evaluate_board(self, board: Board, maximizing_soldier: Soldier) -> float:
        """Fonction d'évaluation du plateau"""
        own_pieces = board.count_soldiers(maximizing_soldier)
        opponent_pieces = board.count_soldiers(
            Soldier.BLUE if maximizing_soldier == Soldier.RED else Soldier.RED
        )
        
        # Bonus pour les captures
        last_action = board.get_last_action()
        capture_bonus = 10 if last_action and last_action['type'] == 'CAPTURE_SOLDIER' else 0
        
        return (own_pieces - opponent_pieces) * 10 + capture_bonus