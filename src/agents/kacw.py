import random
import math
import time
from typing import Dict, Optional, List, Set
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    """AI agent using Enhanced Time-Aware Minimax with advanced evaluation, 
    prenant en compte la géométrie spécifique du plateau pour détecter et pénaliser 
    les centres de losange inoccupés."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "I'm - the - atomic, boom 😎👌🔥"
        self.max_time = 0.0044  # temps max (secondes)
        self.start_time = None
        self.transposition_table = {}  # Mémorisation des évaluations de positions
        self.piece_square_table = self._initialize_piece_square_table()
        self.killer_moves = [[None, None] for _ in range(10)]  # Pour chaque profondeur

    def _initialize_piece_square_table(self) -> Dict[str, Dict[Soldier, float]]:
        """Initialise des valeurs par case spécifiques pour Rouge / Bleu."""
        table = {}
        
        # Zones centrales pour Rouge
        red_center = {'d2': 3.0, 'd3': 3.0, 'd4': 3.0, 'e2': 3.0, 'e3': 3.0, 'e4': 3.0}
        # Zones centrales pour Bleu
        blue_center = {'f2': 3.0, 'f3': 3.0, 'f4': 3.0, 'g2': 3.0, 'g3': 3.0, 'g4': 3.0}
        
        # Valeurs défensives pour Rouge
        red_defensive = {'c1': 2.0, 'c2': 2.0, 'c3': 2.5,
                         'd1': 2.0, 'd2': 2.5, 'd3': 2.5}
        # Valeurs défensives pour Bleu
        blue_defensive = {
            'g2': 3.0, 'g3': 3.5, 'g4': 3.0,
            'h2': 3.0, 'h3': 3.5, 'h4': 3.0,
            'i1': 2.5, 'i3': 2.5, 'i5': 2.5
        }

        # Positions présentes sur le plateau
        all_positions = [
            'a1','a3','a5',
            'b2','b3','b4',
            'c1','c2','c3','c4','c5',
            'd1','d2','d3','d4','d5',
            'e1','e2','e3','e4','e5',
            'f1','f2','f3','f4','f5',
            'g1','g2','g3','g4','g5',
            'h2','h3','h4',
            'i1','i3','i5'
        ]
        
        for pos in all_positions:
            table[pos] = {
                Soldier.RED: (red_center.get(pos, 1.0) + red_defensive.get(pos, 0.0)),
                Soldier.BLUE: (blue_center.get(pos, 1.0) + blue_defensive.get(pos, 0.0))
            }

        return table

    def choose_action(self, board: Board) -> Dict:
        """Choisit la meilleure action en utilisant une recherche approfondie 
        limitée par le temps (max_time)."""
        self.start_time = time.perf_counter()
        valid_actions = board.get_valid_actions()
        if not valid_actions:
            return None

        # Recherche de captures multiples immédiates
        smart_capture = self._find_smart_capture_sequence(board, valid_actions)
        if smart_capture:
            return smart_capture[0]

        # Pour les pièces bleues, privilégier les actions 'safe'
        if self.soldier_value == Soldier.BLUE:
            safe_actions = []
            for action in valid_actions:
                board_copy = self._simulate_action(board, action)
                opponent_captures = [
                    a for a in board_copy.get_valid_actions()
                    if a['type'] == 'CAPTURE_SOLDIER']
                # Si aucune capture adverse après ce coup:
                if not opponent_captures:
                    safe_actions.append(action)
            if safe_actions:
                valid_actions = safe_actions

        best_action = valid_actions[0]
        best_score = -math.inf
        depth = 1

        try:
            # Recherche itérative tant que le temps n’est pas écoulé
            while time.perf_counter() - self.start_time < self.max_time * 0.8:
                current_best_action, score = self._iterative_deepening_search(board, depth)
                
                # Vérifie encore le temps avant de valider
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
        """Applique un Negamax avec gestion alpha-beta, en augmentant progressivement la profondeur."""
        valid_actions = board.get_valid_actions()
        best_action = valid_actions[0]
        alpha = -math.inf
        beta = math.inf
        
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
                if action['type'] != 'CAPTURE_SOLDIER':
                    self.killer_moves[depth] = [self.killer_moves[depth][1], action]
        
        return best_action, alpha

    def _sort_actions(self, board: Board, actions: List[Dict], depth: int) -> List[Dict]:
        """Trie les actions en améliorant l'efficacité de l'élagage alpha-beta et en pénalisant les captures risquées."""
        opponent_soldier = Soldier.BLUE if self.soldier_value == Soldier.RED else Soldier.RED
        action_scores = []
        
        for action in actions:
            score = 0
            
            # Priorité pour les captures
            if action['type'] == 'CAPTURE_SOLDIER':
                score += 1500
                
                # Vérifier si le pion capturant est soutenu
                if not self._is_supported(board, action):
                    # Pénalité sévère pour capturer sans soutien
                    score -= 2000
            
            # Killer move
            if self.killer_moves[depth] and action in self.killer_moves[depth]:
                score += 500
            
            # Bonus de position
            if 'to_pos' in action:
                to_pos = action['to_pos']
                if to_pos in self.piece_square_table:
                    score += self.piece_square_table[to_pos][self.soldier_value] * 100
            
            # Vérification de la sécurité après coup
            board_copy = self._simulate_action(board, action)
            opponent_actions = board_copy.get_valid_actions()
            for oa in opponent_actions:
                if oa['type'] == 'CAPTURE_SOLDIER' and oa.get('soldier_value') == opponent_soldier:
                    if oa['to_pos'] == action['to_pos']:
                        score -= 1000
                        break
            
            action_scores.append((action, score))
        
        # Tri décroissant
        return [act for act, _ in sorted(action_scores, key=lambda x: x[1], reverse=True)]

    def _is_defensive_formation_ready(self, board: Board) -> bool:
        """
        Vérifie la présence d’une formation défensive solide (ex. un losange ou un 
        triangle de pions couvrant le 'centre'). Retourne True si la formation 
        est jugée satisfaisante, False sinon.
        """
        # À implémenter selon vos règles précises (ex. on vérifie plusieurs positions clés).
        # Exemple minimal:
        positions = board.get_soldier_positions(self.soldier_value)
        # Supposons qu’on exige au moins 3 pions en 'triangle' autour de 'd2'
        # (sentence illustrative, adapter la logique réelle):
        required_positions = {'c1', 'c3', 'd2'}
        return required_positions.issubset(positions)

    def _find_smart_capture_sequence(self, board: Board, valid_actions: List[Dict]) -> Optional[List[Dict]]:
        """Détecte et construit la séquence de captures multiples la plus avantageuse."""
        capture_sequences = []
        for action in valid_actions:
            if action['type'] == 'CAPTURE_SOLDIER':
                sequence = []
                self._explore_capture_sequence(board, action, sequence, set())
                if sequence:
                    capture_sequences.append(sequence)
        
        if not capture_sequences:
            return None
        
        best_sequence = None
        best_score = -math.inf
        
        # Évalue chaque séquence de captures
        for sequence in capture_sequences:
            temp_board = board
            for step in sequence:
                temp_board = self._simulate_action(temp_board, step)
            seq_score = self._evaluate_position(temp_board)
            if seq_score > best_score:
                best_score = seq_score
                best_sequence = sequence
        
        return best_sequence

    def _explore_capture_sequence(self, board: Board, action: Dict, sequence: List[Dict], visited: Set[str]):
        """Recherche récursive de captures successives depuis une action initiale."""
        board_copy = self._simulate_action(board, action)
        sequence.append(action)
        
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
        """Implémentation de Negamax avec coupure alpha-beta."""
        if time.perf_counter() - self.start_time > self.max_time:
            raise TimeoutError
        
        board_hash = str(board.soldiers)
        # Table de transposition
        if board_hash in self.transposition_table:
            stored_depth, stored_value = self.transposition_table[board_hash]
            if stored_depth >= depth:
                return stored_value * color

        # Condition de fin
        if depth == 0 or board.is_game_over() is not None:
            return self._quiescence_search(board, alpha, beta, color)
        
        value = -math.inf
        valid_actions = self._sort_actions(board, board.get_valid_actions(), depth)
        
        for action in valid_actions:
            board_copy = self._simulate_action(board, action)
            sub_value = -self._negamax(board_copy, depth - 1, -beta, -alpha, -color)
            value = max(value, sub_value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        
        self.transposition_table[board_hash] = (depth, value)
        return value

    def _quiescence_search(self, board: Board, alpha: float, beta: float, color: int) -> float:
        """Recherche de quiescence pour limiter l'effet horizon."""
        stand_pat = color * self._evaluate_position(board)
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)
        
        captures = [a for a in board.get_valid_actions() if a['type'] == 'CAPTURE_SOLDIER']
        for action in captures:
            board_copy = self._simulate_action(board, action)
            score = -self._quiescence_search(board_copy, -beta, -alpha, -color)
            if score >= beta:
                return beta
            alpha = max(alpha, score)
        return alpha

    def _evaluate_position(self, board: Board) -> float:
        """Évalue la position courante en tenant compte, entre autres, des formations losange."""
        game_over = board.is_game_over()
        if game_over is not None:
            return 10000 if game_over == self.soldier_value else -10000
        
        own_pieces = board.count_soldiers(self.soldier_value)
        opponent = Soldier.BLUE if self.soldier_value == Soldier.RED else Soldier.RED
        opponent_pieces = board.count_soldiers(opponent)

        # Score matériel basé sur la différence de pièces
        material = (own_pieces - opponent_pieces) * 20
        center_control = self._evaluate_center_control(board)
        mobility = self._evaluate_mobility(board)
        defense = self._evaluate_defense(board)
        threats = self._evaluate_threats(board)
        
        defensive_bonus = 0
        if self.soldier_value == Soldier.BLUE:
            defensive_bonus = self._evaluate_defensive_formation(board) * 2

        # Pénalité losange : on détecte les centres vides entourés de 4 pièces adverses
        diamond_penalty = self._detect_diamond_formation(board)

        return (material + center_control + mobility 
                + defense + threats + defensive_bonus 
                + diamond_penalty)

    def _evaluate_center_control(self, board: Board) -> float:
        """Évalue le contrôle des cases centrales."""
        score = 0
        positions = board.get_soldier_positions(self.soldier_value)
        
        for pos in positions:
            if pos in self.piece_square_table:
                score += self.piece_square_table[pos][self.soldier_value] * 5
        return score

    def _evaluate_mobility(self, board: Board) -> float:
        """Évalue le nombre de coups disponibles, avec bonus défensif pour Bleu."""
        valid_moves = board.get_valid_actions()
        mobility_score = len(valid_moves) * 2

        if self.soldier_value == Soldier.BLUE:
            defensive_positions = {'f4','f5','g3','g4','g5','h2','h3','h4'}
            def_moves = sum(1 for act in valid_moves if act.get('to_pos') in defensive_positions)
            mobility_score += def_moves * 1.5
        return mobility_score

    def _evaluate_defense(self, board: Board) -> float:
        """Évalue la densité de soldats amis dans les zones défensives."""
        score = 0
        positions = board.get_soldier_positions(self.soldier_value)

        if self.soldier_value == Soldier.BLUE:
            defensive_zone = {'f4','f5','g3','g4','g5','h2','h3','h4'}
        else:
            defensive_zone = {'c1','c2','c3','d1','d2','d3'}
        
        for pos in positions:
            neighbors = board.get_neighbors(pos)
            friendly_neighbors = len(neighbors[self.soldier_value.name])
            
            # Bonus dans la zone défensive
            if pos in defensive_zone:
                if friendly_neighbors > 0:
                    score += friendly_neighbors * 4
                if friendly_neighbors >= 2:
                    score += 7
            else:
                if friendly_neighbors > 0:
                    score += friendly_neighbors * 2
                if friendly_neighbors >= 2:
                    score += 4
            
            # Pénalité pièces isolées
            if friendly_neighbors == 0:
                score -= 2 if pos in defensive_zone else 3
        
        return score

    def _evaluate_defensive_formation(self, board: Board) -> float:
        """Évalue la formation défensive de Bleu dans des positions clés."""
        if self.soldier_value != Soldier.BLUE:
            return 0
        
        score = 0
        key_positions = {'g2','g3','g4','h2','h3','h4'}
        positions = board.get_soldier_positions(self.soldier_value)
        
        for pos in positions:
            if pos in key_positions:
                score += 3
            neighbors = board.get_neighbors(pos)
            friendly_neighbors = len(neighbors[self.soldier_value.name])
            if pos in key_positions and friendly_neighbors >= 2:
                score += 4
        return score

    def _evaluate_threats(self, board: Board) -> float:
        """Évalue la prise d'initiative et les pièces vulnérables."""
        score = 0
        valid_actions = board.get_valid_actions()
        captures = [a for a in valid_actions if a['type'] == 'CAPTURE_SOLDIER']
        score += len(captures) * 5

        if self.soldier_value == Soldier.BLUE:
            defensive_zone = {'f4','f5','g3','g4','g5','h2','h3','h4'}
            own_positions = board.get_soldier_positions(self.soldier_value)
            for pos in own_positions:
                neighbors = board.get_neighbors(pos)
                empty_neighbors = neighbors[Soldier.EMPTY.name]
                opponent_neighbors = neighbors[Soldier.RED.name]
                # Pièce vulnérable si un adversaire voisin et case vide pour capture
                if opponent_neighbors and empty_neighbors:
                    score -= 15
                    if pos in defensive_zone:
                        score -= 10
            # Bonus si on capture dans la zone défensive
            def_caps = sum(1 for act in captures if act.get('to_pos') in defensive_zone)
            score += def_caps * 8
        else:
            # Pièces rouges : on pénalise la présence de pions bleus vulnérables
            opponent_positions = board.get_soldier_positions(Soldier.BLUE)
            for pos in opponent_positions:
                neighbors = board.get_neighbors(pos)
                if (len(neighbors[self.soldier_value.name]) > 0 
                        and len(neighbors[Soldier.EMPTY.name]) > 0):
                    score -= 2

        return score

    def _simulate_action(self, board: Board, action: Dict) -> Board:
        """Retourne un nouveau plateau après simulation de l’action."""
        board_copy = Board()
        board_copy.soldiers = board.soldiers.copy()
        if action['type'] == 'CAPTURE_SOLDIER':
            board_copy.capture_soldier(action)
        else:
            board_copy.move_soldier(action)
        return board_copy

    # -------------------------------------------------------------------
    # Détection de centres de losange inoccupés, en tenant compte du plateau
    # -------------------------------------------------------------------
    def _detect_diamond_formation(self, board: Board) -> float:
        """
        Parcourt toutes les cases du plateau : si la case est vide (Soldier.EMPTY) 
        et qu'elle possède exactement 4 voisins appartement à l'agent, alors
        on inflige une pénalité (e.g. -50).
        """

        penalty = 0.0

        for center_pos in board.battle_field:
            # Si le centre est vide
            if board.soldiers.get(center_pos) == Soldier.EMPTY:
                # Vérifier le nombre de voisins alliés
                allies_around = board.get_neighbors(center_pos)[self.soldier_value.name]
                # S’il y a exactement 4 pièces alliés autour, c’est un losange
                if len(allies_around) == 4:
                    penalty -= 50
        return penalty

    def _is_supported(self, board: Board, action: Dict) -> bool:
        """
        Vérifie si le pion allié qui effectue la capture est soutenu par au moins un autre pion allié.
        """
        to_pos = action.get('to_pos')
        if not to_pos:
            return False
        
        neighbors = board.get_neighbors(to_pos)[self.soldier_value.name]
        for neighbor in neighbors:
            if board.soldiers.get(neighbor) == self.soldier_value:
                return True
        return False