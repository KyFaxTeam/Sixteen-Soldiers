import time
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier




class Agent(BaseAgent):
    """AI agent with Alpha-Beta pruning and time optimization: last version."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "AIVerse"
        self.Agent1 = Agent1(soldier_value, data)
        self.Agent2 = Agent2(soldier_value, data)
        
    def choose_action(self, board: Board) -> Dict:
        """
        Choose the best action using Alpha-Beta pruning.
        Args:
            board: Current game board state
        Returns:
            The best action for the soldier_value
        """
        return self.Agent1.choose_action(board) if self.Agent1.time_used < 0.5*self.Agent1.time_budget else self.Agent2.choose_action(board)
            

    
class Agent1(BaseAgent):
    """AI agent with Alpha-Beta pruning and time optimization"""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.max_depth = 3  # Profondeur maximale initiale
        self.time_budget = 500  # Temps total alloué en millisecondes
        self.time_used = 0  # Temps utilisé par l'agent
        self.isFirstTurn = True
        self.pionSoldier = soldier_value
        self.pionEnnemy = Soldier.BLUE if soldier_value == Soldier.RED else Soldier.RED
        
        
    def first_action(self, valid_actions):
        possible_actions_set = {('d2', 'e1'), ('d4', 'e5'), ('f4', 'e5'), ('f2', 'e1')}
        for action in valid_actions:
            if (
                action.get('soldier_value') == self.pionSoldier and 
                (action.get('from_pos'), action.get('to_pos')) in possible_actions_set
            ):
                self.isFirstTurn = False
                return action
    
    def choose_action(self, board: Board) -> Dict:
        """
        Choose the best action using Alpha-Beta pruning.
        Args:
            board: Current game board state
        Returns:
            The best action for the soldier_value
        """
        if self.isFirstTurn:
            return self.first_action(board.get_valid_actions())
        
        start_time = time.time()
        best_action = None
        alpha = float("-inf")
        beta = float("inf")
        

        # Run Alpha-Beta pruning to find the best move
        for action in self.prioritize_actions(board.get_valid_actions(), board):
            board_copy = self.copy_board(board)
            self.apply_action(board_copy, action)
            score = self.alpha_beta(board_copy, self.max_depth - 1, alpha, beta, False)
            if score > alpha:
                alpha = score
                best_action = action

        self.time_used += (time.time() - start_time) * 1000
        
        return best_action

    def alpha_beta(self, board: Board, depth: int, alpha: float, beta: float, maximizing: bool) -> float:
        """
        Alpha-Beta pruning algorithm.
        """
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(maximizing, board)

        valid_actions = self.prioritize_actions(board.get_valid_actions(), board)

        if maximizing:
            max_eval = float("-inf")
            for action in valid_actions:
                board_copy = self.copy_board(board)
                self.apply_action(board_copy, action)
                eval = self.alpha_beta(board_copy, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for action in valid_actions:
                board_copy = self.copy_board(board)
                self.apply_action(board_copy, action)
                eval = self.alpha_beta(board_copy, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate_board(self, maximizing, board: Board) -> float:
        """
        Evaluate the board state.
        """
        soldier_count = board.count_soldiers(self.pionSoldier)
        ennemy_count = board.count_soldiers(self.pionEnnemy)
        if maximizing:
            score = -200 if any(next_action['soldier_value'] == self.pionEnnemy and next_action.get("type") == "CAPTURE_SOLDIER" for next_action in board.get_valid_actions()) else -1
            if soldier_count < ennemy_count:
                return soldier_count - ennemy_count - 1 + score
            if soldier_count - ennemy_count > 2:
                if board.is_multiple_capture:
                    return soldier_count - ennemy_count + 2 + score
                return soldier_count - ennemy_count + 1 + score
            return soldier_count - ennemy_count + 1 + score
        else:
            if soldier_count < ennemy_count:
                return soldier_count - ennemy_count
            if soldier_count - ennemy_count > 2:
                if board.is_multiple_capture:
                    return soldier_count - ennemy_count + 3
                return soldier_count - ennemy_count + 2
            return soldier_count - ennemy_count + 1
        

    def prioritize_actions(self, actions: list, board: Board) -> list:
        """
        Prioritize actions to explore better moves first.
        """
        return sorted(actions, key=lambda action: self.heuristic_action_value(action, board), reverse=True)
    


    def heuristic_action_value(self, action: Dict, board: Board) -> int:
        """
        Assign a heuristic value to an action.
        """
        from_pos = action['from_pos']
        to_pos = action['to_pos']
        captured = action.get('captured_soldier', None)

        value = 0
        if captured:
            value += 100
            temp_board = self.apply_action_return(board, action)
            if any(next_action.get("type") == "CAPTURE_SOLDIER"
                for next_action in temp_board.get_valid_actions()):
                value += 200
        if to_pos in board.get_neighbors(from_pos)[Soldier.EMPTY.name]:
            value -= 10  # Prefer advancing
        return value

    def apply_action(self, board: Board, action: Dict):
        """
        Apply an action to a board.
        """
        if action['type'] == 'MOVE_SOLDIER':
            board.move_soldier(action)
        elif action['type'] == 'CAPTURE_SOLDIER':
            board.capture_soldier(action)
    
    def apply_action_return(self, board: Board, action: Dict) -> Board:
        """
        Simule une action sur une copie du plateau et retourne le résultat.
        """
        temp_board = self.copy_board(board)
        if action["type"] == "MOVE_SOLDIER":
            temp_board.move_soldier(action)
        elif action["type"] == "CAPTURE_SOLDIER":
            temp_board.capture_soldier(action)
        return temp_board

    def copy_board(self, board: Board) -> Board:
        new_board = Board()
        new_board.soldiers = board.soldiers.copy()
        new_board.is_multiple_capture = board.is_multiple_capture
        return new_board


class Agent2(BaseAgent):
    """
    Agent IA défensif et opportuniste :
    - Priorise les captures multiples pour maximiser les dégâts.
    - Évite les situations où ses soldats peuvent être capturés.
    - Optimise les mouvements pour garder une position défensive.
    """

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.soldierPion = soldier_value
        self.ennemyPion = Soldier.RED if soldier_value == Soldier.BLUE else Soldier.BLUE

    def choose_action(self, board: Board) -> Dict:
        """
        Prend une décision en suivant cet ordre de priorité :
        1. Action de capture multiple.
        2. Action de capture simple.
        3. Mouvement sûr.
        """
        valid_actions = board.get_valid_actions()

        # Captures multiples
        for action in valid_actions:
            if self.can_lead_to_multiple_captures(board, action):
                return action

        # Captures simples
        for action in valid_actions:
            if action.get("type") == "CAPTURE_SOLDIER" and self.is_ennemy_multiple_capture(board, action):
                return action

        # Mouvements sûrs
        for action in valid_actions:
            if self.is_safe(board, action):
                return action
        return valid_actions[0] if valid_actions else None
    
    def is_ennemy_multiple_capture(self, board, action):
        temp_board = self.apply_action(board, action)
        for action in [action for action in temp_board.get_valid_actions() if action['type'] == 'CAPTURE_SOLDIER' and action['soldier_value'] == self.ennemyPion]:
            if self.apply_action(temp_board, action).is_multiple_capture:
                return False
        return True
    
    def can_lead_to_multiple_captures(self, board: Board, action: Dict) -> bool:
        """
        Vérifie si une action de capture peut conduire à des captures multiples.
        """
        if action["type"] != "CAPTURE_SOLDIER":
            return False

        temp_board = self.apply_action(board, action)
        tempValidAction = temp_board.get_valid_actions()
        if tempValidAction and tempValidAction[0]['soldier_value'] == self.soldierPion:
            return any(
                next_action['soldier_value'] == self.soldierPion and next_action.get("type") == "CAPTURE_SOLDIER" 
                for next_action in tempValidAction
            )

    def is_safe(self, board: Board, action: Dict) -> bool:
        """
        Vérifie si une action est sûre (ne met pas le soldat en danger de capture).
        """
        return not any(
            enemy_move.get("type") == "CAPTURE_SOLDIER"
            for enemy_move in self.apply_action(board, action).get_valid_actions()
        )

    def apply_action(self, board: Board, action: Dict) -> Board:
        """
        Simule une action sur une copie du plateau et retourne le résultat.
        """
        temp_board = self.copy_board(board)
        if action["type"] == "MOVE_SOLDIER":
            temp_board.move_soldier(action)
        elif action["type"] == "CAPTURE_SOLDIER":
            temp_board.capture_soldier(action)
        return temp_board

    def copy_board(self, board: Board) -> Board:
        """
        Crée une copie indépendante du plateau pour les simulations.
        """
        new_board = Board()
        new_board.soldiers = board.soldiers.copy()
        new_board.is_multiple_capture = board.is_multiple_capture
        return new_board
