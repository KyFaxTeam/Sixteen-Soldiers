import re

from models.move import Move
from utils.const import GAP, PADDING

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
      def algebraic_to_gameboard(coord: str) -> tuple[int, int]:
            """
            Convertit une coordonnée algébrique (ex: 'a1') en coordonnée de plateau de jeu (ex: (0, 1)).
            """
            assert re.match(r'^[a-i][1-5]$', coord), "Coordinate must be a letter from a-i followed by a digit 1-5"

            ay, ax = coord[0], coord[1]
            return (int(ax) - 1)* GAP + PADDING, (ord(ay) - ord('a')) * GAP + PADDING
      
      @staticmethod
      def are_aligned(solderA: str, solderB: str, solderC:str) -> bool:
            """
            Vérifie si trois pions sont alignés.
            """
            
            ax, ay = BoardUtils.algebraic_to_cartesian(solderA)
            bx, by = BoardUtils.algebraic_to_cartesian(solderB)
            cx, cy = BoardUtils.algebraic_to_cartesian(solderC)

            return (ax - bx) * (by - cy) == (ay - by) * (bx - cx)
      

