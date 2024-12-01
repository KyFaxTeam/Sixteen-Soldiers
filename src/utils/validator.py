from src.models.board import Board
from src.utils.board_utils import BoardUtils
from src.utils.const import Soldier
from src.utils.logger_config import get_logger

logger = get_logger(__name__)

def is_valid_move(action, board:Board) -> bool:
      # try:
      #     # Validate that 'action' is a dictionary with required keys
          if not isinstance(action, dict):
                logger.error(f"Invalid action type: {type(action)}, expected dict")
                return False
          
          required_keys = ['type', 'from_pos', 'to_pos', 'soldier_value']
          for key in required_keys:
                if key not in action:
                      logger.error(f"Action missing required key: {key}. Action: {action}")
                      return False
                
          # Validate move type
          if action['type'] not in ['MOVE_SOLDIER', 'CAPTURE_SOLDIER']:
                logger.error("Invalid move type")
                return False
          
          # Validate positions exist on board
          if action['from_pos'] not in board.soldiers or action['to_pos'] not in board.soldiers:
                logger.error("Invalid positions in action")
                return False

          # Validate soldier ownership
          if board.soldiers[action['from_pos']] != action['soldier_value']:
                logger.error("Soldier not present at the from_pos position")
                return False

          # Validate destination is empty
          if board.soldiers[action['to_pos']] != Soldier.EMPTY:
                logger.error("Destination position is not empty")
                return False
          
          # Validate positions are valid algebraic notation
          for pos in [action['from_pos'], action['to_pos']]:
                if not BoardUtils.is_valid_algebraic(pos):
                      logger.error("Invalid position")
                      return False
          
          # Validate move action
          if action['type'] == 'MOVE_SOLDIER':
                if action['from_pos'] not in board.battle_field[action['to_pos']]:
                      logger.error("Invalid move position")
                      return False
          
          # Validate capture action
          if action['type'] == 'CAPTURE_SOLDIER':
                if 'captured_soldier' not in action:
                      logger.error("Missing captured_soldier in capture action")
                      return False
                      
                captured_soldier = action['captured_soldier']
                if not BoardUtils.is_valid_algebraic(captured_soldier):
                      logger.error("Invalid captured_soldier position")
                      return False

                if board.soldiers[action['captured_soldier']] == Soldier.EMPTY:
                      logger.error("No soldier to capture at the captured_soldier position")
                      return False
                
                if board.soldiers[action['captured_soldier']] == action['soldier_value']:
                      logger.error("Cannot capture your own soldier")
                      return False
                
                if not BoardUtils.are_aligned(action['from_pos'], action['to_pos'], action['captured_soldier']):
                      logger.error(f"Soldiers not aligned: from={action['from_pos']}, to={action['to_pos']}, captured={captured_soldier}")
                      return False
          
          return True

      # except Exception as e:
      #     logger.exception(f"Validation error: {str(e)}")
      #     return False