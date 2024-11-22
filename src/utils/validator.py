from models.board import Board
from utils.const import Soldier
from utils.logger_config import get_logger

logger = get_logger(__name__)

def is_valid_move(action, board:Board) -> bool:

      # Validate that 'action' is a dictionary with required keys
      if not isinstance(action, dict):
            logger.error("Invalid action returned from AI")
            return False
      
      required_keys = ['type', 'from_pos', 'to_pos', 'soldier_value']
      for key in required_keys:
            if key not in action:
                  logger.error(f"Action missing key: {key}")
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

      return True