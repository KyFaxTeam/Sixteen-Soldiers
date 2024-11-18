class BoardAction:
    @staticmethod
    def move_soldier(from_: str, to: str, soldier: int):
        return {
            "type": "MOVE_SOLDIER",
            "soldier" : soldier,
            "from": from_,
            "to": to
        }
        
    @staticmethod
    def capture_soldier(from_: str, to: str, soldier: int, captured_soldier: str):
        return {
            "type": "CAPTURE_SOLDIER",
            'soldier': soldier,
            'from' : from_,
            'to' : to,
            "captured_soldier": captured_soldier,
        }

    @staticmethod
    def add_soldier(soldier, position):
        return {
            "type": "ADD_SOLDIER",
            "soldier": soldier,
            "position": position
        }

    @staticmethod
    def remove_soldier(soldier, position):
        return {
            "type": "REMOVE_SOLDIER",
            "soldier": soldier,
            "position": position
        }

    @staticmethod
    def reset_board():
        return {
            "type": "RESET_BOARD"
        }