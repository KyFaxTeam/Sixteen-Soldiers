import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    """Agent IA avancée avec stratégie de pièges améliorée, évaluation et logique de priorisation pour défense et attaque."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "JoLyCh"

    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action parmi les options valides selon les priorités suivantes :
        1. Pièges pour captures successives avantageuses.
        2. Meilleure capture sécurisée.
        3. Meilleur mouvement défensif sûr.
        4. Mouvement stratégique sans donner d'opportunités à l'adversaire.
        """
        valid_actions = board.get_valid_actions()
        if not valid_actions:
            raise ValueError("Aucune action valide disponible, vérifiez l'état du jeu.")

        # Pièges pour captures successives
        trap_action = self.find_sacrificial_trap(board, valid_actions)
        if trap_action:
            return trap_action

        # Meilleure capture sécurisée
        best_attack = self.best_move_attack(board, valid_actions)
        if best_attack:
            return best_attack

        # Rechercher des actions sûres
        safe_actions = [action for action in valid_actions if self.is_safe(board, action)]
        if safe_actions:
            return random.choice(safe_actions)

        # Si aucun des mouvements stratégiques n'est trouvé, évalue un mouvement sécurisé
        best_strategic_move = self.best_strategic_move(board, valid_actions)
        return best_strategic_move if best_strategic_move else random.choice(valid_actions)

    def find_sacrificial_trap(self, board: Board, actions: list) -> Dict:
        """Cherche des pièges pour captures successives avantageuses."""
        for action in actions:
            if action["type"] == "CAPTURE_SOLDIER" and self.is_safe_after_capture(board, action):
                # Simule la capture et vérifie les captures successives
                board.move_soldier(action)
                opponent_actions = board.get_valid_actions()
                if not any(
                    opp_action["type"] == "CAPTURE_SOLDIER" for opp_action in opponent_actions
                ):
                    # Évalue les chaînes de captures et annule le mouvement
                    self_capture_chain = any(
                        agent_followup["type"] == "CAPTURE_SOLDIER" for agent_followup in board.get_valid_actions()
                    )
                    board.move_soldier({
                        "type": "MOVE_SOLDIER",
                        "soldier_value": action["soldier_value"],
                        "from_pos": action["to_pos"],
                        "to_pos": action["from_pos"],
                    })
                    if self_capture_chain:
                        return action
                board.move_soldier({
                    "type": "MOVE_SOLDIER",
                    "soldier_value": action["soldier_value"],
                    "from_pos": action["to_pos"],
                    "to_pos": action["from_pos"],
                })
        return None

    def best_move_attack(self, board: Board, actions: list) -> Dict:
        """Retourne la meilleure capture sécurisée après vérification."""
        valid_attacks = [action for action in actions if action["type"] == "CAPTURE_SOLDIER"]
        if not valid_attacks:
            return None
        
        best_attack = max(valid_attacks, key=lambda action: self.evaluate_attack(board, action), default=None)
        return best_attack

    def evaluate_attack(self, board: Board, action: Dict) -> float:
        """Évalue si la capture est sécurisée après l'action."""
        if action["type"] == "CAPTURE_SOLDIER" and self.is_safe_after_capture(board, action):
            return 2.0  # Bonus pour les captures sécurisées
        return 0.0

    def best_strategic_move(self, board: Board, actions: list) -> Dict:
        """Évalue et retourne le mouvement stratégique sans offrir d'opportunités à l'adversaire."""
        def evaluate_move(action: Dict) -> float:
            # Simule le mouvement et évalue la réponse de l'adversaire
            board.move_soldier(action)
            opponent_actions = board.get_valid_actions()
            board.move_soldier({
                "type": "MOVE_SOLDIER",
                "soldier_value": action["soldier_value"],
                "from_pos": action["to_pos"],
                "to_pos": action["from_pos"]
            })

            # Vérifie si l'adversaire a des opportunités de capture
            can_attack = any(opp_action["type"] == "CAPTURE_SOLDIER" for opp_action in opponent_actions)
            return -1.0 if can_attack else 1.0  # Pénalise si l'adversaire peut capturer

        return max(actions, key=evaluate_move, default=None)

    def is_safe_after_capture(self, board: Board, capture_action: Dict) -> bool:
        """Vérifie si la capture ne mène pas à une capture successive."""
        board.move_soldier(capture_action)
        opponent_actions = board.get_valid_actions()
        can_be_captured = any(action["type"] == "CAPTURE_SOLDIER" for action in opponent_actions)
        board.move_soldier({
            "type": "MOVE_SOLDIER",
            "soldier_value": capture_action["soldier_value"],
            "from_pos": capture_action["to_pos"],
            "to_pos": capture_action["from_pos"]
        })
        return not can_be_captured

    def is_safe(self, board: Board, action: Dict) -> bool:
        """
        Vérifie si une action de type MOVE_SOLDIER est sûre (c'est-à-dire ne conduit pas à une capture par l'adversaire).
        """
        if action["type"] != "MOVE_SOLDIER":
            return True  # Les autres types d'actions ne sont pas considérés comme dangereuses

        # Simule le mouvement
        board.move_soldier(action)
        is_dangerous = any(
            adversary_action.get("type") == "CAPTURE_SOLDIER"
            for adversary_action in board.get_valid_actions()
        )
        # Annule le mouvement simulé
        board.move_soldier({
            "type": "MOVE_SOLDIER",
            "soldier_value": action["soldier_value"],
            "from_pos": action["to_pos"],
            "to_pos": action["from_pos"]
        })
        return not is_dangerous
