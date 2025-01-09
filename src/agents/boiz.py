import random
import time
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier


class Agent(BaseAgent):
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "bOy"
        
        self.q_table = {}  # Q-table pour stocker les états et actions
        self.cached_actions = {}  # Cache pour accélérer les décisions
        self.alpha = 0.5  # Taux d'apprentissage
        self.gamma = 0.9  # Facteur de récompense future
        self.epsilon = 0.1  # Taux d'exploration
        self.time_limit = 0.5  # Limite de temps pour une décision (en secondes)
        self.training_completed = False  # Suivi de l'état de l'entraînement

    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action en fonction de la Q-table et de la stratégie d'exploration/exploitation.
        """
        start_time = time.perf_counter()
        valid_actions = board.get_valid_actions()

        # Vérifiez si l'état est dans le cache
        state_key = self.state_to_key(board)
        if state_key in self.cached_actions:
            return self.cached_actions[state_key]

        # Trier les actions par une évaluation heuristique
        sorted_actions = sorted(valid_actions, key=lambda a: self.evaluate_action(board, a), reverse=True)
        best_action = sorted_actions[0] if sorted_actions else random.choice(valid_actions)

        # Exploration vs exploitation
        if random.uniform(0, 1) < self.epsilon:
            best_action = random.choice(valid_actions)  # Exploration

        # Enregistrer l'action choisie dans le cache
        self.cached_actions[state_key] = best_action

        # Respecter la limite de temps
        if time.perf_counter() - start_time > self.time_limit:
            return random.choice(valid_actions)  # Retourne une action aléatoire si dépassement du temps
        return best_action

    def evaluate_action(self, board: Board, action: Dict) -> float:
        """
        Évalue la qualité d'une action en fonction de plusieurs critères.
        """
        score = 0
        if action['type'] == 'CAPTURE_SOLDIER':
            score += 20  # Prioriser les captures
            if board.check_multi_capture(self.soldier_value, action['to_pos']):
                score += 10  # Bonus pour captures multiples
        elif action['type'] == 'MOVE_SOLDIER':
            neighbors = board.get_neighbors(action['to_pos'])
            score += len(neighbors[Soldier.EMPTY.name])  # Préférer les positions connectées
        return score

    def calculate_reward(self, board: Board) -> float:
        """
        Calcule une récompense basée sur l'état du plateau après la dernière action.
        """
        last_action = board.get_last_action()
        if last_action is None:
            return -1  # Penalité si aucune action valide n'est trouvée

        reward = 0
        if last_action['type'] == 'CAPTURE_SOLDIER':
            reward += 20  # Récompense pour capturer un soldat
            if board.check_multi_capture(self.soldier_value, last_action['to_pos']):
                reward += 10  # Bonus pour captures multiples
        elif last_action['type'] == 'MOVE_SOLDIER':
            reward += 1  # Récompense pour un déplacement

        # Encouragez le contrôle des positions stratégiques (exemple : centre du plateau)
        if last_action.get("to_pos") in ['c3', 'd3', 'e3']:
            reward += 5

        return reward

    def update_q_value(self, board: Board, action: Dict, reward: float, next_board: Board) -> None:
        """
        Met à jour la Q-table avec la récompense reçue et la prédiction future.
        """
        current_state_key = self.state_to_key(board)
        next_state_key = self.state_to_key(next_board)
        
        current_q_value = self.q_table.get(current_state_key, {}).get(action['from_pos'], 0)
        max_next_q_value = max(self.q_table.get(next_state_key, {}).values(), default=0)

        # Mise à jour de la Q-value
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * max_next_q_value - current_q_value)
        self.q_table.setdefault(current_state_key, {})[action['from_pos']] = new_q_value

    def state_to_key(self, board: Board) -> str:
        """
        Convertit l'état du plateau en clé unique pour la Q-table.
        """
        return ','.join([f"{pos}:{board.get_soldier_value(pos)}" for pos in board.soldiers.keys()])

    def train(self, episodes: int = 10000):
        """
        Entraîne l'agent avec Q-learning.
        """
        for episode in range(episodes):
            board = Board()  # Réinitialiser le plateau
            done = False
            while not done:
                # Choix d'une action
                action = self.choose_action(board)

                # Simulez l'action et générez le prochain état
                next_board = board.copy()
                if action['type'] == 'MOVE_SOLDIER':
                    next_board.move_soldier(action)
                elif action['type'] == 'CAPTURE_SOLDIER':
                    next_board.capture_soldier(action)

                # Calculer la récompense et mettre à jour la Q-table
                reward = self.calculate_reward(next_board)
                self.update_q_value(board, action, reward, next_board)

                # Passez à l'état suivant
                board = next_board
                done = board.is_game_over() is not None  # Terminer si le jeu est terminé
            
            # Log après chaque épisode d'entraînement
            print(f"Episode {episode + 1}: Training completed for one game.")
        
        # Marquer l'entraînement comme terminé
        self.training_completed = True
