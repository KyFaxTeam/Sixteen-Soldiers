import random
from typing import Dict
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier
from copy import deepcopy

# This file contains the main AI agent that you will use to play the game. It is a main class that we get if you finish your implementation of the game.
class Agent(BaseAgent):
    """AI agent that plays your choice"""
    
    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "Your Team" # You need to replace Your Team with your team name
        
    
    
    def choose_action(self, board: Board) -> Dict:

        """
        Choose an action from valid moves.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """

      
        valid_actions = board.get_valid_actions()
        liste_indice_capture=[index for index, action in enumerate(valid_actions) if action.get('type') == 'CAPTURE_SOLDIER']
        safe_indice=[]
        for i in range (0,len(valid_actions)) :
            if valid_actions[i]['type']=='MOVE_SOLDIER':
                board.move_soldier(valid_actions[i])
                if any(action.get('type') == 'CAPTURE_SOLDIER' for action in  board.get_valid_actions())==False:
                    safe_indice.append(i)
                board.move_soldier({'type': 'MOVE_SOLDIER', 'soldier_value':valid_actions[i]['soldier_value'], 'from_pos': valid_actions[i]['to_pos'], 'to_pos':valid_actions[i]['from_pos']})
        #print(valid_actions)
        if len(liste_indice_capture)!=0:
            #print("liste capture",liste_indice_capture)
            return (valid_actions[random.choice(liste_indice_capture)]) # You need to replace random.choice(valid_actions) with your choice of action or method to choose an action
        elif len(safe_indice)!=0:
            #print("safe",safe_indice)
            return (valid_actions[random.choice(safe_indice)])
        else:
            return random.choice(valid_actions)
    
