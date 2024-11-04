def move_piece(piece, from_position, to_position):
    return {
        "type": "MOVE_PIECE",
        "piece": piece,
        "from_position": from_position,
        "to_position": to_position
    }

def capture_piece(captured_piece, capturing_piece, position):
    return {
        "type": "CAPTURE_PIECE",
        "captured_piece": captured_piece,
        "capturing_piece": capturing_piece,
        "position": position
    }

def add_piece(piece, position):
    return {
        "type": "ADD_PIECE",
        "piece": piece,
        "position": position
    }

def remove_piece(piece, position):
    return {
        "type": "REMOVE_PIECE",
        "piece": piece,
        "position": position
    }

def reset_board():
    return {
        "type": "RESET_BOARD"
    }