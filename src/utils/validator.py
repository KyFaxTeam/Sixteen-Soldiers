import re


def is_valid_move(board, player, from_pos, to_pos):
    """
    Validates if a piece movement is legal.
    
    Args:
        board (Board): Current game board state.
        player (Player): Player attempting the move.
        from_pos (tuple): Starting position (x, y).
        to_pos (tuple): Target position (x, y).
    
    Returns:
        bool: True if move is valid, False otherwise.
    """
    pass

def is_valid_capture(board, player, from_pos, to_pos):
    """
    Validates if a piece capture is legal.
    
    Args:
        board (Board): Current game board state.
        player (Player): Player attempting the capture.
        from_pos (tuple): Starting position (x, y).
        to_pos (tuple): Target position (x, y).
    
    Returns:
        bool: True if capture is valid, False otherwise.
    """
    pass

def is_in_bounds(pos):
    """
    Checks if a position is within the game board boundaries.
    
    Args:
        pos (tuple): Position to check (x, y).
    
    Returns:
        bool: True if position is within bounds, False otherwise.
    """
    pass

def is_adjacent(pos1, pos2):
    """
    Checks if two positions are adjacent (horizontally or vertically).
    
    Args:
        pos1 (tuple): First position (x, y).
        pos2 (tuple): Second position (x, y).
    
    Returns:
        bool: True if positions are adjacent, False otherwise.
    """
    pass

def can_make_multiple_capture(board, player, pos):
    """
    Checks if a player can make multiple captures from a given position.
    
    Args:
        board (Board): Current game board state.
        player (Player): Player to check for.
        pos (tuple): Position to check from (x, y).
    
    Returns:
        bool: True if multiple captures are possible, False otherwise.
    """
    pass

def get_valid_moves(board, player, pos):
    """
    Gets all valid moves for a piece at the given position.
    
    Args:
        board (Board): Current game board state.
        player (Player): Player whose piece to check.
        pos (tuple): Position of the piece (x, y).
    
    Returns:
        list: List of valid target positions (x, y).
    """
    pass

def get_valid_captures(board, player, pos):
    """
    Gets all valid captures for a piece at the given position.
    
    Args:
        board (Board): Current game board state.
        player (Player): Player whose piece to check.
        pos (tuple): Position of the piece (x, y).
    
    Returns:
        list: List of valid capture positions (x, y).
    """
    pass

def is_valid_algebraic_coord(coord: str):
    return re.match(r'^[a-h][0-5]$', coord)