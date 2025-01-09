import re
from typing import Dict, List

from src.actions.board_actions import BoardAction
from src.models.move import Move
from src.utils.const import  PADDING, Soldier

class BoardUtils:
      
      @staticmethod
      def is_valid_algebraic(coord: str) -> bool:
            """
            Vérifie si une coordonnée algébrique est valide.
            """
            return re.match(r'^[a-i][1-5]$', coord) is not None
      
      @staticmethod
      def cartesien_to_algebraic(coord: tuple[int, int]) -> str:
            """
            Convertit une coordonnée cartésienne (ex: (0, 1)) en coordonnée algébrique (ex: 'a1').
            """
            x, y = coord
            return chr(x + ord('a')) + str(y + 1)
      
      @staticmethod
      def algebraic_to_cartesian(coord: str) -> tuple[int, int]:
            """
            Convertit une coordonnée algébrique (ex: 'a1') en coordonnée cartésienne (ex: (0, 1)).
            """
            assert re.match(r'^[a-i][1-5]$', coord), "Coordinate must be a letter from a-i followed by a digit 1-5"
            ay, ax = coord[0], coord[1]
            return int(ax) - 1, ord(ay) - ord('a')
            
      @staticmethod
      def algebraic_to_gameboard(coord: str, gap: int) -> tuple[int, int]:
            """
            Convertit une coordonnée algébrique (ex: 'a1') en coordonnée de plateau de jeu (ex: (0, 1)).
            """
            assert re.match(r'^[a-i][1-5]$', coord), "Coordinate must be a letter from a-i followed by a digit 1-5"

            ay, ax = coord[0], coord[1]
            return (int(ax) - 1)* gap + PADDING, (ord(ay) - ord('a')) * gap + PADDING
      
      @staticmethod
      def are_aligned(solderA: str, solderB: str, solderC:str) -> bool:
            """
            Vérifie si trois pions sont alignés.
            """
            
            ax, ay = BoardUtils.algebraic_to_cartesian(solderA)
            bx, by = BoardUtils.algebraic_to_cartesian(solderB)
            cx, cy = BoardUtils.algebraic_to_cartesian(solderC)

            return (ax - bx) * (by - cy) == (ay - by) * (bx - cx)
      
      @staticmethod
      def get_actions_soldier(battle_field, soldiers, soldier_value: Soldier, last_position: str) -> List[Dict]:
      
        
        valid_actions = []
        opponent = Soldier.BLUE if soldier_value == Soldier.RED else Soldier.RED

        # If it's a capture continuation, restrict to capture moves only
        if last_position: 
            capture_actions = BoardUtils.find_continued_captures(
                  battle_field,
                  soldiers,
                soldier_value, 
                last_position
            )
            return capture_actions if capture_actions else []
        
        # Find empty positions
        empty_positions = [
            pos for pos, occupant in soldiers.items() 
            if occupant == Soldier.EMPTY
        ]

        # For each empty position
        for empty_pos in empty_positions:
            
            for neighbor in battle_field[empty_pos]:
                current_piece = soldiers[neighbor]
                
                # Simple move
                if current_piece == soldier_value:
                    valid_actions.append(BoardAction.move_soldier(
                        from_pos=neighbor,
                        to_pos=empty_pos,
                        soldier_value=soldier_value
                    ))
                # Possible capture
                elif current_piece == opponent:
                    # Check pieces that can capture
                    capture_positions = [
                        pos for pos in battle_field[neighbor]
                        if soldiers[pos] == soldier_value
                    ]
                    
                    # Add to_pos to all possible captures
                    for from_pos in capture_positions:
                        if BoardUtils.are_aligned(empty_pos, neighbor, from_pos):
                            valid_actions.append(BoardAction.capture_soldier(
                                from_pos=from_pos,
                                to_pos=empty_pos,
                                soldier_value=soldier_value,
                                captured_soldier=neighbor
                            ))
        # Return only actions validated by is_valid_move in validator.py
        return valid_actions

      @staticmethod
      def find_continued_captures(battle_field, soldiers, soldier_value: Soldier, last_position, just_know: bool = False) -> List[Dict] | bool:
            """
            Find all possible continued captures from the last position.
            Used for multi-capture sequences.
            """
            continued_captures = []
            opponent = Soldier.BLUE if soldier_value == Soldier.RED else Soldier.RED
            
            # Explore all adjacent empty positions
            empty_positions = [
                  pos for pos, occupant in soldiers.items() 
                  if occupant == Soldier.EMPTY
            ]

            for neighbor in battle_field[last_position]: 
                  current_piece = soldiers[neighbor]

                  # Check if it's an opponent's piece
                  if current_piece == opponent: 
                  # Find potential aligned capture positions
                        capture_positions = [
                              empty_pos for empty_pos in battle_field[neighbor]
                              if (empty_pos in empty_positions and BoardUtils.are_aligned(empty_pos, neighbor, last_position))
                        ]
                        
                        if just_know and capture_positions : 
                              return True
                                    
                        # Add consecutive capture actions
                        for empty_pos in capture_positions:
                              continued_captures.append(BoardAction.capture_soldier(
                                    from_pos=last_position,
                                    to_pos=empty_pos,
                                    soldier_value=soldier_value,
                                    captured_soldier=neighbor
                              ))
                  
            return continued_captures
      
            

