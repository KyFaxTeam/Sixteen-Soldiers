import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier
from src.store.store import Store

history = []

# This file contains the main AI agent that you will use to play the game. It is a main class that we get if you finish your implementation of the game.
class Agent(BaseAgent):
    """AI agent that plays your choice"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Bee Light" # You need to replace Your Team with your team name
        
    
    
    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action basée sur une stratégie multi-critères.
        
        Args:
            board: État actuel du plateau de jeu
        Returns:
            Action choisie parmi les actions valides
        """
        valid_actions = board.get_valid_actions()
        global history
        history.append(board.get_last_action())
        
        
        if len(history) < 2 :
            actions = [action for action in valid_actions if action['from_pos'] in ['d2','d4','f2','f4'] and action['to_pos'] in ['e1','e5'] ]
            if len(actions) > 0:
                return (actions[0])
    
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
        if self.soldier_value == Soldier.RED:
            defensive_positions = ['a5', 'a1','c1', 'c5']
        else:
            defensive_positions = ['i5','i1', 'g1', 'g5']
        
        score = 1.0
        
        
        # Bonus supplémentaire si la capture mène à une position défensive
        if action['to_pos'] in defensive_positions:
            score += 6
            
        avoid_enemies_weight = -10    
        # Malus si on est entouré par beaucoup d'ennemis
        neighbors = board.get_neighbors(action['to_pos'])
        enemy_soldiers = neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
        score += avoid_enemies_weight * len(enemy_soldiers)    
        
        # Bonus si la capture permet d'éviter d'être capturé
        neighbors = board.get_neighbors(action['to_pos'])
        enemy_soldiers = neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
        if not enemy_soldiers:
            score += 40
            if action['to_pos'] in ['a5', 'a1','c1', 'c5','i5','i1', 'g1', 'g5']:
                score += 20
            neighbors_ = board.get_neighbors(action['from_pos'])
            enemy_soldiers_ = neighbors_[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
            empty_ = neighbors_[Soldier.EMPTY.name]
            if enemy_soldiers_ or empty_:
                score += 80*len(enemy_soldiers_) + 80*len(empty_)
             
        else:
            score -= 20*len(enemy_soldiers)           
                    
        # Bonus si on échappe aux ennemis
            
        
        return score

    
    def _evaluate_move(self, board: Board, action: Dict) -> float:
        """Évalue l'intérêt stratégique d'un mouvement sans capture."""
        
        if self.soldier_value == Soldier.RED:
            defensive_positions = ['a5', 'a1','c1', 'c5']
        else:
            defensive_positions = ['i5','i1', 'g1', 'g5']
        score = 0.0

        # Pondération des critères
        move_to_defensive_positions = 8
        avoid_enemies_weight = -100
        ally_support_weight = 100
        free_space_weight = -1
        neighbors_defensive_weight = 2
        move_out_to_defensive_position = -4.5
        
        # Bonus si on se rapproche d'une position défensive
        if action['to_pos'] in defensive_positions:
            score += move_to_defensive_positions

        # Malus si on est entouré par beaucoup d'ennemis
        neighbors = board.get_neighbors(action['to_pos'])
        enemy_soldiers = neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
        score += avoid_enemies_weight * len(enemy_soldiers)
        
        
        if not enemy_soldiers:
            score += 40
            neighbors_ = board.get_neighbors(action['from_pos'])
            enemy_soldiers_ = neighbors_[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
            if enemy_soldiers_:
                score += 80*len(enemy_soldiers_)
            if action['to_pos'] in ['a5', 'a1','c1', 'c5','i5','i1', 'g1', 'g5']:
                score += 20 
        else:
            score -= 20*len(enemy_soldiers)           
                
            
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
