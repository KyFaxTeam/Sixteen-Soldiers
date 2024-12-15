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
        self.name = "Les Sisters" # You need to replace Your Team with your team name
        
        
    
    
    def choose_action(self, board: Board) -> Dict:

        """
        Choose an action from valid moves.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """

    
        valid_actions = board.get_valid_actions()
        
        #print("Hello")
        #print(valid_actions, "\n")
        #positions = board.get_soldier_positions(self.soldier_value)
        #print(positions)

        decision_prise_rapide = self.prise_rapide(board=board)
        if decision_prise_rapide != None:
            return decision_prise_rapide
        else:
            return random.choice(valid_actions)
        #scores = self.simulataion(board=board)
        #max_score = max(scores)
        #indice_max = scores.index(max_score) 
        
        # return random.choice(valid_actions) # valid_actions[indice_max] You need to replace random.choice(valid_actions) with your choice of action or method to choose an action
    
    def prise_rapide(self,board: Board):
        valid_actions = board.get_valid_actions()
        capture_list = []
        for elt in valid_actions:
            if 'captured_soldier' in elt.keys():
                capture_list.append(elt)

        if capture_list == []:
            return None
        else:
            # Test de captures multiples
            for plt in capture_list:
                if board.check_multi_capture(soldier_value="RED",current_position=plt["from_pos"]):
                    
                    
                    return plt
            # Test de captures multiples Non vérifié
            retour = capture_list[0]
            
            return retour
        
            

    def evalue_jeu(self, board: Board):
        score = 0
        if self.soldier_value==Soldier.RED:
            moi = 'RED'
            adverse = 'BLUE'
        else:
            moi = 'BLUE'
            adverse = 'RED'
        positions = board.get_soldier_positions(self.soldier_value)
        print(moi ,adverse)
        
         
        for position in positions:
            voisins=board.get_neighbors( position)
            score += len(voisins[moi])
            score -= len(voisins[adverse])  
        
        return score
    
    def simulation(self,board: Board):
        valid_actions = board.get_valid_actions()
        actions = []
        for action in valid_actions:
            del action["type"]
            actions.append(action)
            
        scores = []
        for move in actions:
            board.move_soldier(move)
            
            score = self.evalue_jeu(board)
            scores.append(score)
        return scores
            
        
