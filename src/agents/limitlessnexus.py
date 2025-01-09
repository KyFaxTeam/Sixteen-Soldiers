
import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

# This file contains the main AI agent that you will use to play the game. It is a main class that we get if you finish your implementation of the game.
class Agent(BaseAgent):
    """AI agent that plays your choice"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Limitless Nexus" # You need to replace Your Team with your team name
        
    
    def get_opponent_soldier_value(self)-> str:
        if self.soldier_value==1:
            return "RED"
        else:
            return "BLUE"
        
        
        
        
        
        
    def is_safe(self,board:Board, move:Dict)->bool:
        """ vérifie si une positionest dangereuse
        en fonction des voisins
        """
        neighbors=board.get_neighbors(move['to_pos'])
        
        
        # teste l'existence de pions de l'aversaire dans la postion d'arrivée
       
        
        if len(neighbors[self.get_opponent_soldier_value()])!=0:         # teste l'existence de pions de l'aversaire dans la postion d'arrivée

            return False
        else:
            return True
        
        
    def choose_action(self, board: Board)-> Dict:

        """
        Choose an action from valid moves.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """
        valid_actions_list=board.get_valid_actions() 
        """
        if not valid_actions_list:
            return None # aucun mouvement possible"""
        for action in valid_actions_list:
            if action['type']=="CAPTURE_SOLDIER":
                return action
                
       
               
       # Action non capture soldier
        safe_moves=[ move for move in valid_actions_list if self.is_safe(board, move)] 
        #obtenir une action sécurisée ou un mouvement aleatoire
        if safe_moves:
            return random.choice(safe_moves)
        else:
            return random.choice(valid_actions_list)

    
    
        
        
        


