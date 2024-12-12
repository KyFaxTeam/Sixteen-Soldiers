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
        self.max_time = 0.9  # Temps max autorisé (en secondes)
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
        for depth in range(1, 6):  # De profondeur 1 à 5
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
<<<<<<< HEAD
            board: État actuel du plateau.
            time_limit: Temps maximum alloué pour la recherche (en secondes).

        Returns:
            Une action valide sélectionnée.
        """
        root = MCTSNode(board)
        start_time = time.time()

<<<<<<< HEAD
    
        valid_actions = board.get_valid_actions()
        
        return random.choice(valid_actions) # You need to replace random.choice(valid_actions) with your choice of action or method to choose an action
        
    
=======
        # Boucle de recherche limitée par le temps
        while time.time() - start_time < time_limit * 0.9:  # Marge de sécurité de 10%
            node = self.select(root)
            reward = self.simulate(node)
            self.backpropagate(node, reward)

        # Retourner le meilleur enfant après la recherche
        return root.best_child(exploration_weight=0).action

    def select(self, node: MCTSNode) -> MCTSNode:
        """
        Sélectionne un nœud à explorer en suivant le chemin le plus prometteur.
        """
        while not node.is_terminal():
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                node = node.best_child(self.exploration_weight)
        return node

    def expand(self, node: MCTSNode) -> MCTSNode:
        """
        Étend le nœud en explorant une action non encore explorée.
        """
        action = node.untried_actions.pop()
        new_board = self.apply_action(node.board_state, action)
        child = MCTSNode(new_board, parent=node, action=action)
        node.children.append(child)
        return child

    def simulate(self, node: MCTSNode) -> float:
        """
        Effectue une simulation aléatoire depuis le nœud donné et retourne la récompense.
        """
        current_board = node.board_state.copy()
        current_player = self.soldier_value

        while not current_board.is_game_over():
            valid_actions = current_board.get_valid_actions()
            if not valid_actions:
                break
            action = random.choice(valid_actions)
            current_board = self.apply_action(current_board, action)
            current_player = self.opponent_color(current_player)

        # Évaluation du plateau après la simulation
        return self.evaluate_board(current_board, self.soldier_value)

    def backpropagate(self, node: MCTSNode, reward: float):
        """
        Met à jour les statistiques des nœuds en remontant l'arbre.
        """
        while node is not None:
            node.visits += 1
            node.total_reward += reward
            node = node.parent

    def apply_action(self, board: Board, action: Dict) -> Board:
        """
        Applique une action sur une copie du plateau et retourne le nouveau plateau.
        """
        new_board = board.copy()
        new_board.move_soldier(action)
        return new_board

    def evaluate_board(self, board: Board, player_color: Soldier) -> float:
        """
        Évalue le plateau en fonction de critères stratégiques.
        """
        my_pieces = board.count_soldiers(player_color)
        opponent_pieces = board.count_soldiers(self.opponent_color(player_color))
        
        # Opportunités de capture
        capture_actions = [a for a in board.get_valid_actions() if a['type'] == 'CAPTURE_SOLDIER']

        # Score basé sur le nombre de pièces et les opportunités de capture
        score = (my_pieces - opponent_pieces) * 10 + len(capture_actions) * 5

        return score

    def opponent_color(self, color: Soldier) -> Soldier:
        """Retourne la couleur opposée."""
        return Soldier.BLUE if color == Soldier.RED else Soldier.RED
>>>>>>> 35022fa (merge)
=======
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
>>>>>>> 7363695 (Premier push KACW)
