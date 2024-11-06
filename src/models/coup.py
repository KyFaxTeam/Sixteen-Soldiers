from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class Coup:
    """Représente un coup joué dans la partie Sixteen Soldiers"""
    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    joueur_id: str
    timestamp: float
    piece_capturee: Optional[str] = None
    capture_multiple: bool = False

    def __init__(self, joueur_id: str, from_pos: tuple, to_pos: tuple):
        self.joueur_id = joueur_id
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece_capturee = None  # Position de la pièce capturée si applicable

    def to_dict(self) -> dict:
        """Convertit le coup en dictionnaire pour la sauvegarde"""
        return {
            "from_pos": self.position_depart,
            "to_pos": self.position_arrivee,
            "joueur_id": self.joueur_id,
            "timestamp": self.timestamp,
            "piece_capturee": self.piece_capturee,
            "capture_multiple": self.capture_multiple
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Coup':
        """Crée une instance de Coup à partir d'un dictionnaire"""
        return cls(**data)
