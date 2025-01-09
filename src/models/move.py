from typing import List, Optional, Dict
from dataclasses import dataclass

from src.utils.const import Soldier

@dataclass
class Move:
    
    """Représente un mouvement dans le jeu de sixteen-soldiers"""
    pos: List[str]  # Liste des coordonnées [départ, arrivée]
    soldier_value: Soldier
    timestamp: List[int]  # Liste des timestamps pour chaque étape du mouvement
    captured_soldier: List
    capture_multiple: bool = False

    def __init__(self, pos: List[str], soldier_value: Soldier, timestamp: float, 
                 captured_soldier: List, capture_multiple: bool = False):
        self.pos = pos
        self.soldier_value = soldier_value
        self.timestamp = timestamp
        self.captured_soldier = captured_soldier
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
            'pos': self.pos,
            'soldier_value': self.soldier_value,
            'timestamp': self.timestamp,
            'captured_soldier': self.captured_soldier,
            'capture_multiple': self.capture_multiple
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Move':
        return cls(
            pos=data['pos'],
            soldier_value=data['soldier_value'],
            captured_soldier=data.get('captured_soldier'),
            capture_multiple=data.get('capture_multiple', False), 
            timestamp=data.get('timestamp')
        )

    def __str__(self) -> str:
        """Représentation string du mouvement"""
        move_str = f"Mouvement : {self.get_start_position()} → {self.get_end_position()}"
        if self.captured_soldier:
            move_str += f" (Capture en {self.captured_soldier})"
        if self.capture_multiple:
            move_str += " (Capture multiple)"
        return move_str

    def is_capture(self) -> bool:
        """Vérifie si le mouvement est une capture"""
        return self.captured_soldier is not None

    def equals(self, other: 'Move') -> bool:
        return (
            self.pos == other.pos and 
            self.soldier_value == other.soldier_value and 
            self.captured_soldier == other.captured_soldier and 
            self.capture_multiple == other.capture_multiple
        )

    def is_valid_player(self, other: Dict) -> bool:
        return (
            self.soldier_value == other["soldier_value"] and
            self.pos[-1] == other["from_pos"]
        )