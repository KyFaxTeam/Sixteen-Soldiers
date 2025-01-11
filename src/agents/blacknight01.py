import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    """Agent IA pour jouer au jeu 16 Soldats"""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "StrategicAI"

    def choose_action(self, board: Board) -> Dict:
        """
        Choisit le déplacement idéal en tenant compte des mouvements adverses.
        
        Args:
            board: État actuel du plateau de jeu.
            
        Returns:
            Une action valide choisie pour minimiser les risques et maximiser les opportunités.
        """
        valid_actions = board.get_valid_actions()  # Actions valides pour l'IA
        best_action = None
        best_score = float('-inf')

        for action in valid_actions:
            # Simuler le plateau après cette action
            simulated_board = self.simulate_action(board, action)

            # Évaluer les réponses de l'adversaire
            opponent_actions = simulated_board.get_valid_actions()
            worst_case_score = float('inf')

            for opponent_action in opponent_actions:
                # Simuler le plateau après la réponse de l'adversaire
                opponent_simulated_board = self.simulate_action(simulated_board, opponent_action)

                # Évaluer l'état du plateau après la réponse
                current_score = self.evaluate_board(opponent_simulated_board, self.soldier_value)
                worst_case_score = min(worst_case_score, current_score)

            # Maximiser le score minimum (logique mini-max)
            if worst_case_score > best_score:
                best_score = worst_case_score
                best_action = action

        return best_action

    def simulate_action(self, board: Board, action: Dict) -> Board:
        """
        Simule un plateau après une action donnée.
        
        Args:
            board: L'état actuel du plateau.
            action: L'action à simuler.
            
        Returns:
            Une copie simulée du plateau après l'action.
        """
        simulated_board = Board()
        simulated_board.soldiers = board.soldiers.copy()
        if action['type'] == 'MOVE':
            simulated_board.move_soldier(action)
        elif action['type'] == 'CAPTURE_SOLDIER':
            simulated_board.capture_soldier(action)
        return simulated_board

    def evaluate_board(self, board: Board, soldier_value: Soldier) -> int:
        """
        Évalue un plateau pour un joueur donné.
        
        Args:
            board: L'état du plateau à évaluer.
            soldier_value: Le joueur pour lequel évaluer (RED ou BLUE).
            
        Returns:
            Un score qui reflète les avantages et les risques pour le joueur.
        """
        my_soldiers = board.count_soldiers(soldier_value)
        opponent_soldiers = board.count_soldiers(Soldier.RED if soldier_value == Soldier.BLUE else Soldier.BLUE)

        # Comptabilise les opportunités offensives et défensives
        attack_opportunities = len(self.get_attack_actions(board.get_valid_actions(), board))
        defensive_strength = len(self.get_defensive_actions(board.get_valid_actions(), board))

        # Calcul du score
        return (my_soldiers * 10) + (attack_opportunities * 7) - (opponent_soldiers * 10) - (defensive_strength * 5)

    def get_attack_actions(self, valid_actions: List[Dict], board: Board) -> List[Dict]:
        """
        Filtre les actions d'attaque (captures).
        
        Args:
            valid_actions: Liste des actions valides.
            board: Plateau actuel.
            
        Returns:
            Liste des actions qui permettent des captures.
        """
        return [action for action in valid_actions if action['type'] == 'CAPTURE_SOLDIER']

    def get_defensive_actions(self, valid_actions: List[Dict], board: Board) -> List[Dict]:
        """
        Filtre les actions défensives (éviter d'exposer ses soldats).
        
        Args:
            valid_actions: Liste des actions valides.
            board: Plateau actuel.
            
        Returns:
            Liste des actions qui réduisent les expositions aux captures adverses.
        """
        defensive_actions = []
        for action in valid_actions:
            simulated_board = self.simulate_action(board, action)
            opponent_actions = simulated_board.get_valid_actions()
            if all(opponent_action['type'] != 'CAPTURE_SOLDIER' for opponent_action in opponent_actions):
                defensive_actions.append(action)
        return defensive_actions
