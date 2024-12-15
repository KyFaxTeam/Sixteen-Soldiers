import random
from typing import Dict, List
from src.agents.base_agent import BaseAgent
from src.models.board import Board
from src.utils.const import Soldier

class Agent(BaseAgent):
    """Agent IA qui priorise les captures simples et multiples en utilisant la méthode check_multi_capture."""

    def __init__(self, soldier_value: Soldier, data: Dict = None):
        super().__init__(soldier_value, data)
        self.name = "AI_MAU"  # Remplacez par le nom de votre équipe

    def choose_action(self, board: Board) -> Dict:
        """
        Choisit une action en fonction de la logique de capture d'un soldat ennemi,
        en priorisant les captures multiples.
        Args:
            board: État actuel du plateau de jeu
        Returns:
            L'action choisie pour le joueur (soldier_value)
        """
        valid_actions = board.get_valid_actions()

        if not valid_actions:
           
            return None  # Si aucune action n'est disponible, la partie devrait se terminer

        # Étape 1 : Vérifier les actions qui permettent de capturer un soldat ennemi
        capture_action = self.choose_capture_action(board, valid_actions)
        if capture_action:
            return capture_action

        # Étape 2 : Si aucune capture n'est possible, choisir une action aléatoire (fallback)
        return random.choice(valid_actions)

    def choose_capture_action(self, board: Board, valid_actions: List[Dict]) -> Dict:
        """
        Priorise les actions permettant de capturer un soldat ennemi.
        Une capture est possible si la position cible n'est pas un voisin immédiat de la position de départ.
        Args:
            board: État actuel du plateau de jeu
            valid_actions: Liste des actions valides
        Returns:
            Une action de capture si disponible, sinon None
        """
        # Étape 1 : Vérifier en priorité les captures multiples
        for action in valid_actions:
            from_pos = action['from_pos']
            soldier_value = board.get_soldier_value(from_pos)
            
            """# Appel de check_multi_capture pour vérifier les captures multiples
            if board.check_multi_capture(soldier_value, from_pos):
                print(f"Capture multiple détectée depuis {from_pos}")
                return action"""

        # Étape 2 : Vérifier les captures simples (par saut)
        for action in valid_actions:
            from_pos = action['from_pos']
            to_pos = action['to_pos']
            
            # Obtenir les voisins immédiats de la position de départ
            neighbors = board.get_neighbors(from_pos)

            # Vérifier si la position cible n'est pas un voisin immédiat
            if to_pos not in neighbors['EMPTY']:  # Vérifie que `to_pos` n'est pas un voisin immédiat
                
                #pour une deuxieme capture si possible
                from_pos_2=to_pos
                valides_2=board.get_valid_actions_for_position(from_pos_2)
                for action_2 in valides_2:
                    from_pos_2 = action_2['from_pos']
                    to_pos_2 = action_2['to_pos']
                    
                    neighbors_2 = board.get_neighbors(from_pos_2)
                    if to_pos_2 not in neighbors_2['EMPTY']:
                        
                        #pour une troisieme capture si possible
                        from_pos_3=to_pos_2
                        valides_3=board.get_valid_actions_for_position(from_pos_3)
                        for action_3 in valides_3:
                            from_pos_3 = action_3['from_pos']
                            to_pos_3 = action_3['to_pos']
                            neighbors_3 = board.get_neighbors(from_pos_3)
                            if to_pos_3 not in neighbors_3['EMPTY']:
                                
                                return action_3  # Retourner l'action de capture
                                
                        
                        return action_2  # Retourner l'action de capture
                    
                
                return action  # Retourner l'action de capture
            

        # Si aucune capture n'est possible, retourner None
        
        return None
