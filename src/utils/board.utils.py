class BoardUtils:
      
      @staticmethod
      def algebreCoord_to_cartesienCoord(coord: str) -> tuple[int, int]:
            
            assert isinstance(coord, str), "Coordinate muste be string"
            assert len(coord) == 2, "Coordinate muste have two character"
            
            ax, ay = coord[0], coord[1]
            
            return ord(ax), ord(ay)
            
      @staticmethod
      def algebreCoord_to_gameboardCoord(coord: str) -> tuple [int, int]:
            
            assert isinstance(coord, str), "Coordinate muste be string"
            assert len(coord) == 2, "Coordinate muste have two character"