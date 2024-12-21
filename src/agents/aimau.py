import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    """Agent IA qui priorise les captures simples et multiples."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "AI_MAU/ the terminator"
        self.boole = True
        self.history = None

    def move_last_action(self, board: Board, valid_actions: List[Dict]) -> Dict:
        """Inverser l'action précédente si aucune capture n'est possible."""
        if not self.history:
            return random.choice(valid_actions)

        last_action = self.history.copy()
        last_action['from_pos'], last_action['to_pos'] = last_action['to_pos'], last_action['from_pos']

        if last_action in valid_actions:
            return last_action
        return random.choice(valid_actions)

    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action en fonction de la logique de capture d'un soldat ennemi,
        en priorisant les captures multiples.
        """
        valid_actions = board.get_valid_actions()

        if not valid_actions:
            return None  # Si aucune action n'est disponible, la partie devrait se terminer

        self.value = valid_actions[0]["soldier_value"]  # Stocker la valeur du soldat

        # Étape 1 : Vérifier les captures multiples
        capture_action = self.choose_capture_action(board, valid_actions)
        if capture_action:
            self.history = capture_action
            return capture_action

        # Étape 2 : Vérifier les captures simples (saut unique) sans risque
        simple_capture_action = self.choose_simple_capture_action(board, valid_actions)
        if simple_capture_action:
            self.history = simple_capture_action
            return simple_capture_action

        # Étape 3 : Si aucune capture n'est possible, essayer l'inversion de l'action précédente
        if self.history:
            inverted_action = self.move_last_action(board, valid_actions)
            if inverted_action:
                self.history = inverted_action
                return inverted_action

        # Étape 4 : Si aucune capture n'est possible, choisir parmi les actions sans risque
        no_risk_actions = self.get_no_risk_positions(board, valid_actions)
        if no_risk_actions:
            chosen_action = random.choice(no_risk_actions)
            self.history = chosen_action
            return chosen_action

        # Étape 5 : Si aucune action sans risque n'est disponible, choisir une action aléatoire
        return random.choice(valid_actions)

    def choose_capture_action(self, board: Board, valid_actions: List[Dict]) -> Dict:
        """
        Priorise les actions permettant de capturer un soldat ennemi.
        Une capture est possible si la position cible n'est pas un voisin immédiat de la position de départ.
        """
        # Étape 1 : Vérifier en priorité les captures multiples (jusqu'à trois niveaux)
        for action in valid_actions:
            from_pos = action['from_pos']
            to_pos = action['to_pos']

            neighbors = board.get_neighbors(from_pos)
            if to_pos not in neighbors['EMPTY']:

                # Vérifier une deuxième capture
                next_valid_actions = board.get_valid_actions_for_position(to_pos)
                for action_2 in next_valid_actions:
                    from_pos_2 = action_2['from_pos']
                    to_pos_2 = action_2['to_pos']
                    neighbors_2 = board.get_neighbors(from_pos_2)

                    if to_pos_2 not in neighbors_2['EMPTY']:

                        # Vérifier une troisième capture
                        next_valid_actions_2 = board.get_valid_actions_for_position(to_pos_2)
                        for action_3 in next_valid_actions_2:
                            from_pos_3 = action_3['from_pos']
                            to_pos_3 = action_3['to_pos']
                            neighbors_3 = board.get_neighbors(from_pos_3)

                            if to_pos_3 not in neighbors_3['EMPTY']:
                                return action_3

                        return action_2

                return action

        return None

    def choose_simple_capture_action(self, board: Board, valid_actions: List[Dict]) -> Dict:
        """
        Choisir une capture simple qui ne met pas l'agent en danger.
        """
        for action in valid_actions:
            from_pos = action['from_pos']
            to_pos = action['to_pos']

            neighbors = board.get_neighbors(from_pos)
            if to_pos not in neighbors['EMPTY']:
                return action

        return None

    def get_no_risk_positions(self, board: Board, valid_actions: List[Dict]) -> List[Dict]:
        """Récupère les actions qui mènent à des positions sans risque"""
        no_risk_positions = []
        for action in valid_actions:
            from_pos = action['from_pos']
            to_pos = action['to_pos']
            neighbors = board.get_neighbors(to_pos)
            is_safe = True
            for neighbor_pos in neighbors:
                neighbor_value = board.get_soldier_value(neighbor_pos)
                if neighbor_value is not None and neighbor_value != board.get_soldier_value(from_pos):
                    is_safe = False
                    break
            if is_safe:
                no_risk_positions.append(action)
        return no_risk_positions
