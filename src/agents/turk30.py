import time
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class NeuralNetwork:
    """Réseau de neurones pour évaluer les positions."""
    def predict(self, board_state):
        valid_actions = board_state.get_valid_actions()
        if not valid_actions:
            return [], 0  # Aucun mouvement possible
        policy = [1 / len(valid_actions) for _ in valid_actions]  # Politique uniforme
        value = self.evaluate_board(board_state)
        return policy, value

    def evaluate_board(self, board):
        """Évaluation basée sur centralité, captures et menaces."""
        my_pieces = board.get_pieces(board.soldier_value)
        opponent_pieces = board.get_pieces(board.get_opponent_soldier(board.soldier_value))
        score = 0

        # Avantage matériel
        score += (len(my_pieces) - len(opponent_pieces)) * 10

        # Positionnement stratégique
        for piece in my_pieces:
            if board.is_central_position(piece):
                score += 2  # Priorité à la centralité
            if board.is_defensive_position(piece):
                score += 1  # Défense

        # Menaces et captures possibles
        score += self.evaluate_captures(board)
        score -= self.evaluate_threats(board)

        return score / 100  # Normalisation

    def evaluate_captures(self, board):
        """Priorise les captures multiples."""
        captures = 0
        for action in board.get_valid_actions():
            new_board = board.copy()
            new_board.play_action(action, board.soldier_value)
            captures += len(new_board.get_captures(board.soldier_value))
        return captures * 15  # Récompense pour captures

    def evaluate_threats(self, board):
        """Punit les actions menant à des captures multiples par l'adversaire."""
        threats = 0
        opponent = board.get_opponent_soldier(board.soldier_value)
        for action in board.get_valid_actions():
            new_board = board.copy()
            new_board.play_action(action, opponent)
            threats += len(new_board.get_captures(opponent))
        return threats * 20


class MCTSNode:
    """Noeud pour Monte Carlo Tree Search."""
    def __init__(self, board: Board, parent=None, prior=0.0):
        self.board = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.total_value = 0
        self.prior = prior
        self.action = None

    def is_fully_expanded(self):
        return len(self.children) == len(self.board.get_valid_actions())

    def best_child(self, exploration_weight=1.4):
        if not self.children:
            return None
        return max(
            self.children,
            key=lambda child: child.total_value / (child.visits + 1e-5) + exploration_weight * child.prior
        )


class Agent(BaseAgent):
    """IA combinant MCTS, Minimax Alpha-Bêta, et réseau neuronal."""
    def __init__(self, soldier_value: Soldier, data: Dict = None, time_limit: float = 0.5, depth: int = 3):
        super().__init__(soldier_value, data)
        self.name = "Turk_3.0"
        self.neural_net = NeuralNetwork()
        self.time_limit = time_limit  # Temps pour MCTS
        self.depth = depth  # Profondeur de recherche pour minimax

    def choose_action(self, board: Board) -> Dict:
        """Choisit le meilleur coup en utilisant MCTS et évaluation heuristique."""
        if not board.get_valid_actions():
            return None  # Aucun coup valide possible

        start_time = time.time()
        root = MCTSNode(board)
        policy, _ = self.neural_net.predict(board)

        # Initialisation des enfants
        for action, prob in zip(board.get_valid_actions(), policy):
            child_board = board.copy()
            child_board.play_action(action, self.soldier_value)
            node = MCTSNode(child_board, root, prob)
            node.action = action
            root.children.append(node)

        # MCTS avec limite de temps
        while time.time() - start_time < self.time_limit:
            node = root
            while node.is_fully_expanded():
                node = node.best_child()

            self.expand_node(node)
            value = self.evaluate_position(node.board)
            self.backpropagate(node, value)

        # Retourne le meilleur coup
        best_node = root.best_child(exploration_weight=0.0)
        if best_node is None:
            return None  # Aucun coup valide
        return best_node.action

    def expand_node(self, node):
        """Ajoute des enfants au noeud."""
        policy, _ = self.neural_net.predict(node.board)
        for action, prob in zip(node.board.get_valid_actions(), policy):
            child_board = node.board.copy()
            child_board.play_action(action, self.soldier_value)
            new_node = MCTSNode(child_board, node, prob)
            new_node.action = action
            node.children.append(new_node)

    def backpropagate(self, node, value):
        """Rétro-propagation des valeurs."""
        while node:
            node.visits += 1
            node.total_value += value
            node = node.parent

    def evaluate_position(self, board: Board) -> float:
        """Évalue la position du plateau."""
        captures = board.get_captures(self.soldier_value)
        opponent_captures = board.get_captures(board.get_opponent_soldier(self.soldier_value))
        return len(captures) * 10 - len(opponent_captures) * 15
