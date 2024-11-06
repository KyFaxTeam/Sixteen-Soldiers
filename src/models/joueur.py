from dataclasses import dataclass, field
from typing import List, Optional, Dict
from .coup import Coup

@dataclass
class Joueur:
    """Représente un joueur dans le jeu Sixteen Soldiers"""
    id: str
    nom: str
    couleur: str
    pieces_restantes: int = 16
    
    statistiques: dict = field(default_factory=lambda: {
        "victoires": 0,
        "defaites": 0,
    })
    est_actif: bool = False

   
    def perdre_piece(self):
        """Décrémente le nombre de pièces restantes du joueur"""
        pass


    def conclure_partie(self):
        """Met à jour les statistiques du joueur après une victoire ou une défaite"""
        pass

    def jouer_coup(self, coup: Coup):
        """Ajoute un coup à l'historique du joueur"""
        pass

    @property
    def est_gagnant(self) -> bool:
        """Indique si le joueur a gagné la partie"""
        pass

    @property
    def adversaire(self) -> Optional['Joueur']:
        """Retourne l'adversaire du joueur"""
        pass