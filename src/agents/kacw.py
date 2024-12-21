import random
import math
import time
from typing import Dict, Optional, List, Set
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    """AI agent using Enhanced Time-Aware Minimax with advanced evaluation"""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Enhanced Time Strategist"
        self.max_time = 0.005  # Maximum time allowed (seconds)
        self.start_time = None
        self.transposition_table = {}  # Pour stocker les positions déjà évaluées
        self.piece_square_table = self._initialize_piece_square_table()
        self.killer_moves = [[None, None] for _ in range(10)]  # Pour chaque profondeur

    def _initialize_piece_square_table(self) -> Dict[str, float]:
        """Initialize the piece-square table for position evaluation"""
        table = {}
        # Les positions centrales sont plus valorisées (autour de d2, d3, d4, e2, e3, e4)
        center_positions = {'d2': 3.0, 'd3': 3.0, 'd4': 3.0, 
                          'e2': 3.0, 'e3': 3.0, 'e4': 3.0}
        edge_value = 1.0
        
        for pos in ['a1', 'a3', 'a5', 'b2', 'b3', 'b4', 'c1', 'c2', 'c3', 'c4', 'c5',
                   'd1', 'd2', 'd3', 'd4', 'd5', 'e1', 'e2', 'e3', 'e4', 'e5',
                   'f1', 'f2', 'f3', 'f4', 'f5', 'g1', 'g2', 'g3', 'g4', 'g5',
                   'h2', 'h3', 'h4', 'i1', 'i3', 'i5']:
            table[pos] = center_positions.get(pos, edge_value)
        
        return table

    def choose_action(self, board: Board) -> Dict:
        """Chooses the best action using iterative deepening and time management"""
        self.start_time = time.perf_counter()
        valid_actions = board.get_valid_actions()
        
        if not valid_actions:
            return None
            
        # Vérifier les captures immédiates avantageuses
        smart_capture = self._find_smart_capture_sequence(board, valid_actions)
        if smart_capture:
            return smart_capture[0]  # Retourne la première capture de la séquence
        
        best_action = valid_actions[0]  # Action par défaut
        best_score = -math.inf
        depth = 1
        
        try:
            # Iterative deepening
            while time.perf_counter() - self.start_time < self.max_time * 0.8:  # Garde 85% de marge
                current_best_action, score = self._iterative_deepening_search(board, depth)
                
                if time.perf_counter() - self.start_time < self.max_time * 0.8:
                    best_action = current_best_action
                    best_score = score
                    depth += 1
                else:
                    break
                    
        except TimeoutError:
            pass
        
        return best_action

    def _iterative_deepening_search(self, board: Board, depth: int) -> tuple[Dict, float]:
        """Perform iterative deepening search"""
        valid_actions = board.get_valid_actions()
        best_action = valid_actions[0]
        alpha = -math.inf
        beta = math.inf
        
        # Trier les actions pour améliorer l'élagage
        sorted_actions = self._sort_actions(board, valid_actions, depth)
        
        for action in sorted_actions:
            if time.perf_counter() - self.start_time > self.max_time:
                raise TimeoutError
                
            board_copy = self._simulate_action(board, action)
            score = self._negamax(board_copy, depth - 1, -beta, -alpha, -1)
            score = -score
            
            if score > alpha:
                alpha = score
                best_action = action
                # Mettre à jour les killer moves
                if action['type'] != 'CAPTURE_SOLDIER':
                    self.killer_moves[depth] = [self.killer_moves[depth][1], action]
                    
        return best_action, alpha

    def _sort_actions(self, board: Board, actions: List[Dict], depth: int) -> List[Dict]:
        """Sort actions to improve alpha-beta pruning efficiency"""
        action_scores = []
        
        for action in actions:
            score = 0
            # Priorité aux captures
            if action['type'] == 'CAPTURE_SOLDIER':
                score += 1000
            
            # Killer move heuristic
            if self.killer_moves[depth] and action in self.killer_moves[depth]:
                score += 500
                
            # Position value from piece-square table
            if 'to_pos' in action:
                score += self.piece_square_table.get(action['to_pos'], 0) * 100
                
            action_scores.append((action, score))
            
        return [action for action, _ in sorted(action_scores, key=lambda x: x[1], reverse=True)]

    def _find_smart_capture_sequence(self, board: Board, valid_actions: List[Dict]) -> Optional[List[Dict]]:
        """Find the best sequence of captures"""
        capture_sequences = []
        
        for action in valid_actions:
            if action['type'] == 'CAPTURE_SOLDIER':
                sequence = []
                self._explore_capture_sequence(board, action, sequence, set())
                if sequence:
                    capture_sequences.append(sequence)
        
        if not capture_sequences:
            return None
            
        # Évaluer chaque séquence
        best_sequence = None
        best_score = -math.inf
        
        for sequence in capture_sequences:
            board_copy = board
            for action in sequence:
                board_copy = self._simulate_action(board_copy, action)
            
            score = self._evaluate_position(board_copy)
            if score > best_score:
                best_score = score
                best_sequence = sequence
                
        return best_sequence

    def _explore_capture_sequence(self, board: Board, action: Dict, sequence: List[Dict], visited: Set[str]):
        """Explore all possible capture sequences from a given position"""
        board_copy = self._simulate_action(board, action)
        sequence.append(action)
        
        # Convert position to string for visited set
        pos = action['to_pos']
        if pos in visited:
            return
        
        visited.add(pos)
        next_captures = [a for a in board_copy.get_valid_actions() if a['type'] == 'CAPTURE_SOLDIER']
        
        if not next_captures:
            return
            
        for next_action in next_captures:
            self._explore_capture_sequence(board_copy, next_action, sequence, visited.copy())

    def _negamax(self, board: Board, depth: int, alpha: float, beta: float, color: int) -> float:
        """Negamax implementation with alpha-beta pruning"""
        # Vérification du temps
        if time.perf_counter() - self.start_time > self.max_time:
            raise TimeoutError
            
        # Position hash pour la table de transposition
        board_hash = str(board.soldiers)
        
        # Lookup dans la table de transposition
        if board_hash in self.transposition_table:
            stored_depth, stored_value = self.transposition_table[board_hash]
            if stored_depth >= depth:
                return stored_value * color
                
        # Conditions de fin
        if depth == 0 or board.is_game_over() is not None:
            return self._quiescence_search(board, alpha, beta, color)
            
        value = -math.inf
        valid_actions = self._sort_actions(board, board.get_valid_actions(), depth)
        
        for action in valid_actions:
            board_copy = self._simulate_action(board, action)
            value = max(value, -self._negamax(board_copy, depth - 1, -beta, -alpha, -color))
            alpha = max(alpha, value)
            
            if alpha >= beta:
                break
                
        # Store in transposition table
        self.transposition_table[board_hash] = (depth, value)
        return value

    def _quiescence_search(self, board: Board, alpha: float, beta: float, color: int) -> float:
        """Quiescence search to handle horizon effect"""
        stand_pat = color * self._evaluate_position(board)
        
        if stand_pat >= beta:
            return beta
            
        alpha = max(alpha, stand_pat)
        
        # Ne considérer que les captures pour la quiescence
        captures = [action for action in board.get_valid_actions() if action['type'] == 'CAPTURE_SOLDIER']
        
        for action in captures:
            board_copy = self._simulate_action(board, action)
            score = -self._quiescence_search(board_copy, -beta, -alpha, -color)
            
            if score >= beta:
                return beta
            alpha = max(alpha, score)
            
        return alpha

    def _evaluate_position(self, board: Board) -> float:
        """Enhanced position evaluation"""
        # Vérifier si la partie est terminée
        game_over = board.is_game_over()
        if game_over is not None:
            if game_over == self.soldier_value:
                return 10000  # Victoire
            else:
                return -10000  # Défaite
                
        own_pieces = board.count_soldiers(self.soldier_value)
        opponent_soldier = Soldier.BLUE if self.soldier_value == Soldier.RED else Soldier.RED
        opponent_pieces = board.count_soldiers(opponent_soldier)
        
        # Valeur matérielle
        material = (own_pieces - opponent_pieces) * 20
        
        # Contrôle du centre
        center_control = self._evaluate_center_control(board)
        
        # Mobilité
        mobility = self._evaluate_mobility(board)
        
        # Structure défensive
        defense = self._evaluate_defense(board)
        
        # Menaces
        threats = self._evaluate_threats(board)
        
        # Combiner tous les facteurs
        return material + center_control + mobility + defense + threats

    def _evaluate_center_control(self, board: Board) -> float:
        """Evaluate control of central positions"""
        score = 0
        positions = board.get_soldier_positions(self.soldier_value)
        
        for pos in positions:
            score += self.piece_square_table.get(pos, 0) * 5
            
        return score

    def _evaluate_mobility(self, board: Board) -> float:
        """Evaluate piece mobility"""
        return len(board.get_valid_actions()) * 2

    def _evaluate_defense(self, board: Board) -> float:
        """Evaluate defensive structure"""
        positions = board.get_soldier_positions(self.soldier_value)
        score = 0
        
        for pos in positions:
            neighbors = board.get_neighbors(pos)
            friendly_neighbors = len(neighbors[self.soldier_value.name])
            
            # Bonus progressif pour chaque pièce amie adjacente
            if friendly_neighbors > 0:
                score += friendly_neighbors * 3
            
            # Bonus pour les formations défensives
            if friendly_neighbors >= 2:
                score += 5
            
            # Malus pour les pièces isolées
            if friendly_neighbors == 0:
                score -= 3
                
        return score

    def _evaluate_threats(self, board: Board) -> float:
        """Evaluate threatening positions and potential captures"""
        score = 0
        valid_actions = board.get_valid_actions()
        captures = [action for action in valid_actions if action['type'] == 'CAPTURE_SOLDIER']
        score += len(captures) * 5
            
        return score

    def _simulate_action(self, board: Board, action: Dict) -> Board:
        """Simulate an action and return a copy of the board"""
        board_copy = Board()
        board_copy.soldiers = board.soldiers.copy()
        
        if action['type'] == 'CAPTURE_SOLDIER':
            board_copy.capture_soldier(action)
        else:
            board_copy.move_soldier(action)
            
        return board_copy