import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    """Agent IA ultra-optimisé pour une stratégie offensive et défensive."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Mugiwara"

    def choose_action(self, board: Board) -> Dict:
        """Choisit une action optimale."""
        return self.evaluate_and_choose_action(board)

    def evaluate_and_choose_action(self, board: Board) -> Dict:
        """
        Évalue toutes les actions possibles et retourne la meilleure en utilisant des heuristiques claires.
        - Priorité offensive : capturer un maximum d'adversaires.
        - Défense : éviter de se placer dans des positions vulnérables.
        """
        valid_actions = board.get_valid_actions()
        if not valid_actions:
            return None

        best_action = None
        max_score = float('-inf')

        for action in valid_actions:
            score = self.evaluate_action(board, action)
            if score > max_score:
                max_score = score
                best_action = action

        return best_action

    def evaluate_action(self, board: Board, action: Dict) -> int:
        """
        Évalue une action avec une pondération basée sur des critères offensifs et défensifs.
        """
        score = 0

        my_soldier_value = action['soldier_value']
        opponent_soldier_value = Soldier.RED if my_soldier_value == Soldier.BLUE else Soldier.BLUE
        from_pos = action['from_pos']
        to_pos = action['to_pos']
        # Bonus offensif : priorité aux captures
        if action['type'] == 'CAPTURE_SOLDIER':
            score += 20  # Bonus pour capturer un adversaire
            if board.check_multi_capture(self.soldier_value, action['to_pos']):
                score += 30  # Bonus supplémentaire pour capture multiple potentielle
        # Simulation rapide pour évaluer les risques
        is_safe = self.check_if_safe(board, action)
        if not is_safe :
            score -= 25

        return score

    def simulate_action(self, board: Board, action: Dict):
        """Applique une action sur le plateau simulé sans copie inutile."""
        if action['type'] == 'CAPTURE_SOLDIER':
            board.capture_soldier(action)
        else:
            board.move_soldier(action)

    def undo_action(self, board: Board, action: Dict):
        """Annule une action pour restaurer l'état initial."""
        from_pos = action['to_pos']
        to_pos = action['from_pos']
        if action['type'] == 'CAPTURE_SOLDIER' :
            captured_pos = action['captured_soldier']
            soldier_value = action['soldier_value']
            board.move_soldier({'from_pos': from_pos, 'to_pos': to_pos, 'soldier_value': action['soldier_value']})
            opponent_soldier_value = Soldier.RED if soldier_value == Soldier.BLUE else Soldier.BLUE
            board.soldiers[captured_pos] = opponent_soldier_value
        else :
            board.move_soldier({'from_pos': from_pos, 'to_pos': to_pos, 'soldier_value': action['soldier_value']})

    def check_if_safe (self, board : Board, action : Dict) -> bool:
        simulated_board = board
        self.simulate_action(simulated_board, action)

        # Pénalité défensive : éviter d'exposer nos pièces à une capture
        opponent_actions = simulated_board.get_valid_actions()
        if any(a['type'] == 'CAPTURE_SOLDIER' for a in opponent_actions):
            # Restaurer l'état initial du plateau
            self.undo_action(simulated_board, action)
            return False
        # Restaurer l'état initial du plateau
        self.undo_action(simulated_board, action)
        return True