from src.utils.const import Soldier

class BoardAction:
    @staticmethod
    def move_soldier(from_pos: str, to_pos: str, soldier_value: Soldier):
        return {
            "type": "MOVE_SOLDIER",
            "soldier_value" : soldier_value,
            "from_pos": from_pos,
            "to_pos": to_pos
        }
        
    @staticmethod
    def capture_soldier(from_pos: str, to_pos: str, captured_soldier: str,  soldier_value: Soldier):
        return {
            "type": "CAPTURE_SOLDIER",
            'soldier_value': soldier_value,
            'from_pos' : from_pos,
            'to_pos' : to_pos,
            "captured_soldier": captured_soldier,
        }
