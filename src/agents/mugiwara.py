import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier
import copy

class Agent(BaseAgent):
    """AI agent that plays your choice"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Mugiwara"  # Replace "Your Team" with your team name
        
    def choose_action(self, board: Board) -> Dict:
        """
        Choose an action from valid moves based on simulation and safety.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """
        valid_actions = board.get_valid_actions()
        safe_actions = []
        best_action = None

        for action in valid_actions:
            # Faire une copie superficielle du plateau pour chaque simulation
            simulated_board = copy.deepcopy(board)
            
            # Appliquer l'action sur le plateau simulé
            if action['type'] == 'CAPTURE_SOLDIER':
                simulated_board.capture_soldier(action)
            else:
                simulated_board.move_soldier(action)
            
            # Vérifier les actions de l'adversaire sur le plateau simulé
            opponent_actions = simulated_board.get_valid_actions()
            is_safe = all(a['type'] != 'CAPTURE_SOLDIER' for a in opponent_actions)

            # Si l'action est "safe", l'ajouter à la liste
            if is_safe:
                if action['type'] == 'CAPTURE_SOLDIER':
                    # Priorité immédiate pour une capture "safe"
                    return action
                safe_actions.append(action)

        # Si aucune action prioritaire, choisir aléatoirement parmi les actions "safe"
        if safe_actions:
            best_action = random.choice(safe_actions)
        else:
            # Si aucune action "safe", choisir une action aléatoire
            best_action = random.choice(valid_actions)

        return best_action