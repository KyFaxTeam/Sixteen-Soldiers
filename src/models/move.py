
from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Move:
    """Représente un mouvement dans le jeu de sixteen-soldiers"""
    pos: List[str]  # Liste des coordonnées [départ, arrivée]
    player_id: int
    timestamp: List[int]  # Liste des timestamps pour chaque étape du mouvement
    piece_capturee: Optional[str] = None
    capture_multiple: bool = False

    def __init__(self, pos: List[str], player_id: int, timestamp: float, 
                 piece_capturee: Optional[str] = None, capture_multiple: bool = False):

        # self.id = id
        self.pos = pos
        self.player_id = player_id
        self.timestamp = timestamp
        self.piece_capturee = piece_capturee
        self.capture_multiple = capture_multiple

    def get_start_position(self) -> str:
        """Retourne la position de départ"""
        return self.pos[0]

    def get_end_position(self) -> str:
        """Retourne la position d'arrivée"""
        return self.pos[1]

    def to_dict(self) -> Dict:
        """Convertit le mouvement en dictionnaire"""
        return {
            # 'id': self.id,
            'pos': self.pos,
            'player_id': self.player_id,
            'timestamp': self.timestamp,
            'piece_capturee': self.piece_capturee,
            'capture_multiple': self.capture_multiple
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Move':

        move = cls(
            # id=data['id'],
            pos=data['pos'],
            player_id=data['player_id'],
            piece_capturee=data.get('piece_capturee'),
            capture_multiple=data.get('capture_multiple', False), 
            timestamp=data.get('timestamp')
            
        )
        # move.timestamp = data.get('timestamp', [int(datetime.now().timestamp())])
        return move

    def __str__(self) -> str:
        """Représentation string du mouvement"""
        move_str = f"Mouvement #{self.id} : {self.get_start_position()} → {self.get_end_position()}"
        if self.piece_capturee:
            move_str += f" (Capture en {self.piece_capturee})"
        if self.capture_multiple:
            move_str += " (Capture multiple)"
        return move_str

    def is_capture(self) -> bool:
        """Vérifie si le mouvement est une capture"""
        return self.piece_capturee is not None

    def equals(self, other: 'Move') -> bool:

        return (
                # self.id == other.id and 
                self.pos == other.pos and 
                self.player_id == other.player_id and 
                self.piece_capturee == other.piece_capturee and 
                self.capture_multiple == other.capture_multiple)
    
    def is_valid_player(self, other: Dict) -> bool:
        return (
            self.player_id == other["player_id"] and
            self.pos[-1] == other["from_pos"]
        ) 