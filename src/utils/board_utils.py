import re

from utils.const import GAP, PADDING

class BoardUtils:
      
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
            ax, ay = coord[0], coord[1]
            return ord(ax.lower()) - ord('a'), int(ay) - 1
            
      @staticmethod
      def algebraic_to_gameboard(coord: str) -> tuple[int, int]:
            """
            Convertit une coordonnée algébrique (ex: 'a1') en coordonnée de plateau de jeu (ex: (0, 1)).
            """
            assert re.match(r'^[a-i][1-5]$', coord), "Coordinate must be a letter from a-i followed by a digit 1-5"
            ax, ay = coord[0], coord[1]
            return (ord(ax) - ord('a')) * GAP + PADDING, (int(ay) - 1)* GAP + PADDING
            