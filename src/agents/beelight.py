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
        self.name = "Bee Light" # You need to replace Your Team with your team name
        
    
    
    def choose_action(self, board: Board) -> Dict:
       
        valid_actions = board.get_valid_actions()
        
        # Si aucune action n'est possible, retourner None
        if not valid_actions:
            return None
        
        # Prioriser les captures
        capture_actions = [action for action in valid_actions if action['type'] == 'CAPTURE_SOLDIER']
        if capture_actions:
            # Choisir la capture qui maximise le nombre de pièces capturées
            return max(capture_actions, key=lambda action: self._evaluate_capture(board, action))
        
        # Sinon, choisir le mouvement le plus stratégique
        return max(valid_actions, key=lambda action: self._evaluate_move(board, action))

    def _evaluate_capture(self, board: Board, action: Dict) -> float:
       
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
      
        # Positions  stratégiques
        defensive_positions = ['a3', 'c1', 'i3','i1', 'g1', 'g5','e1','e5']
        score = 0.0
        
        # Bonus si on se rapproche du centre
        if action['to_pos'] in defensive_positions:
            score += 0.6
        
        # Bonus si on s'éloigne des pièces ennemies
        neighbors = board.get_neighbors(action['to_pos'])
        enemy_soldiers = neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.RED else Soldier.RED.name]
        score -= 0.05 * (len(enemy_soldiers) + 1)
        
        ally=neighbors[Soldier.BLUE.name if self.soldier_value == Soldier.BLUE else Soldier.RED.name]
        score += 0.2 * (len(ally) + 1)
        
        free=neighbors[Soldier.EMPTY.name]
        score += 0.1 * (len(free) + 1)
        # Bonus si le mouvement ouvre de nouvelles possibilités
        possible_moves_after = len(board.get_valid_actions_for_position(action['to_pos']))
        score += 0.1 * possible_moves_after
        
        return score        
        
