import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

# This file contains the main AI agent that you will use to play the game. It is a main class that we get if you finish your implementation of the game.
class Agent(BaseAgent):
    """AI agent that plays your choice"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Claude AI" # You need to replace Your Team with your team name
        
    
    
    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action basée sur une stratégie multi-critères.
        
        Args:
            board: État actuel du plateau de jeu
        Returns:
            Action choisie parmi les actions valides
        """
        valid_actions = board.get_valid_actions()
        
        # Si aucune action n'est possible, retourner None
        if not valid_actions:
            return None
        
        # Prioriser les captures
        capture_actions = [action for action in valid_actions if action['type'] == 'CAPTURE_SOLDIER']
        if capture_actions:
            # Choisir la capture qui maximise le nombre de pièces capturées
           return max(capture_actions, key=lambda action: self._evaluate_capture(board, action))
        
        return max(valid_actions, key=lambda action: self._evaluate_move(board, action))

    def _evaluate_capture(self, board: Board, action: Dict) -> float:
        """
        Évalue l'intérêt d'une capture.
        
        Args:
            board: État du plateau
            action: Action de capture à évaluer
        Returns:
            Score de la capture (plus le score est élevé, plus la capture est intéressante)
        """
        # Bonus si la capture est proche des positions qui protègent le pion 
        defensive_positions = ['a3', 'c1', 'i3','i1', 'g1', 'g5','e1','e5']
        score = 1.0
        
        
        # Bonus supplémentaire si la capture mène à une position défensive
        if action['to_pos'] in defensive_positions:
            score += 0.6
        
        # Bonus si la capture permet d'éviter d'être capturé
        neighbors = board.get_neighbors(action['to_pos'])
        enemy_soldiers = neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
        if not enemy_soldiers:
            score += 0.3
        
        return score

    
    def _evaluate_move(self, board: Board, action: Dict) -> float:
        """Évalue l'intérêt stratégique d'un mouvement sans capture."""
        defensive_positions = ['a3', 'c1', 'i3', 'i1', 'g1', 'g5', 'e1', 'e5']
        score = 0.0

        # Pondération des critères
        move_to_defensive_positions = 0.8
        avoid_enemies_weight = -0.4
        ally_support_weight = 0.3
        free_space_weight = 0.2
        neighbors_defensive_weight = 0.2
        move_out_to_defensive_position = -0.45
        
        # Bonus si on se rapproche d'une position défensive
        if action['to_pos'] in defensive_positions:
            score += move_to_defensive_positions

        # Malus si on est entouré par beaucoup d'ennemis
        neighbors = board.get_neighbors(action['to_pos'])
        enemy_soldiers = neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
        score += avoid_enemies_weight * len(enemy_soldiers)

        # Bonus si on se rapproche d'alliés
        ally_neighbors = neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.BLUE else Soldier.RED.name]
        score += ally_support_weight * len(ally_neighbors)

        # Bonus pour se positionner dans un espace libre
        free_neighbors = neighbors[Soldier.EMPTY.name]
        score += free_space_weight * len(free_neighbors)
        
        #Bonus si l'on se rapproche d'une position défensive
        for neigh_ in  neighbors:
            if neigh_ in defensive_positions:
                score += neighbors_defensive_weight
                break   
        #Malus si l'on quitte une position défensive
        if action['from_pos'] in defensive_positions:
               score += move_out_to_defensive_position

        return score
