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
        if self.soldier_value==Soldier.RED:
            self.moi = 'RED'
            self.adverse = 'BLUE'
        else:
            self.moi = 'BLUE'
            self.adverse = 'RED'
        
    
    
    def choose_action(self, board: Board) -> Dict:

        """
        Choose an action from valid moves.
        Args:
            board: Current game board state
        Returns:
            Chosen valid action for the soldier_value
        """

    
        valid_actions = board.get_valid_actions()
        
        positions = board.get_soldier_positions(self.soldier_value)
        

        decision_prise_rapide = self.prise_rapide(board=board)
        if decision_prise_rapide != None:
            return decision_prise_rapide
        else:
            scores = self.simulation(board=board)
            max_score = max(scores)
            indice_max = scores.index(max_score)
            return valid_actions[indice_max]
        #scores = self.simulation(board=board)
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
                if board.check_multi_capture(soldier_value=self.moi,current_position=plt["from_pos"]):
                    return plt
            # Test de captures multiples Non vérifié
            retour = capture_list[0]
            
            return retour
        
            

    def evalue_jeu(self, board: Board):
        score = 0
        positions = board.get_soldier_positions(self.soldier_value)
        
        for position in positions:
            voisins=board.get_neighbors( position)
            score += (len(voisins[self.moi])*256)
            score -= (len(voisins[self.adverse])*256) 
            
        position_score = {"a1":0,"a3":2,"a5":0,"b2":2,"b3":4,
                          "b4":2,"c1":0,"c2":2,"c3":8,"c4":2,
                          "c5":0,"d1":2,"d2":8,"d3":8,"d4":8,
                          "d5":2,"e1":2,"e2":8,"e3":8,"e4":8,
                          "e5":2,"f1":2,"f2":8,"f3":8,"f4":8,
                          "f5":2,"g1":0,"g2":2,"g3":8,"g4":2,
                          "g5":0,"h2":2,"h3":4,"h4":2,"i1":0,
                          "i3":2,"i5":0
                          }
        # score nombre de rouge et nombre de blue
        for position in positions:
            voisins=board.get_neighbors( position)
            score += (len(voisins[self.moi])*256)
            score -= (len(voisins[self.adverse])*256)
        
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
            
    def nouveau_board(board,mouvement):
        board.move_soldier(mouvement)
        return board
    def minimax(self,board:Board,position,deep,maximisingPlayer):
        if deep == 0 or board.is_game_over():
            return self.evalue_jeu(board=board) 
        
        if maximisingPlayer:
            maxEval = -9999999999
            for mouvement in board.get_valid_actions_for_position(position):
                evaluation = self.minimax(board=board,position=mouvement,deep= deep-1,maximisingPlayer=False)
                maxEval = max(maxEval,evaluation)
            return maxEval
        
        else:
            minEval = 9999999999
            for mouvement in board.get_valid_actions_for_position(position):
                evaluation = self.minimax(board=board,position=mouvement,deep= deep-1,maximisingPlayer=True)
                minEval = max(minEval,evaluation)
            return minEval
        
