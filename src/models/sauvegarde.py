import os
import json
from datetime import datetime
from typing import Tuple, List
from .coup import Coup

class Sauvegarde:
    """Gère la sauvegarde et le chargement des parties de Sixteen Soldiers"""
    
    def __init__(self, nom_fichier: str):
        # Obtenir le chemin de base du projet, deux niveaux au-dessus de ce fichier
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        # Construire le chemin complet vers le dossier data/sauvegardes
        self.nom_fichier = os.path.join(base_dir, 'data', 'sauvegardes', nom_fichier)
        self.metadata = {
            "date_creation": datetime.now().isoformat(),
            "version": "1.0"
        }

    def sauvegarder_partie(self, etat_plateau: dict, historique_coups: List[Coup]) -> bool:
        """Sauvegarde l'état actuel de la partie"""
        try:
            donnees = {
                "metadata": self.metadata,
                "etat_plateau": etat_plateau,
                "historique_coups": [coup.to_dict() for coup in historique_coups]
            }

            # Création du dossier s'il n'existe pas encore
            os.makedirs(os.path.dirname(self.nom_fichier), exist_ok=True)

            # Écriture des données dans le fichier
            with open(self.nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False

    @classmethod
    def charger_partie(cls, nom_fichier: str) -> Tuple[dict, List[Coup]]:
        """Charge une partie sauvegardée"""
        try:
            # Obtenir le chemin de base du projet pour localiser le fichier de sauvegarde
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
            chemin_fichier = os.path.join(base_dir, 'data', 'sauvegardes', nom_fichier)

            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                donnees = json.load(f)

            historique_coups = [
                Coup.from_dict(coup_dict)
                for coup_dict in donnees["historique_coups"]
            ]

            return donnees["etat_plateau"], historique_coups
        except Exception as e:
            print(f"Erreur lors du chargement: {e}")
            return None, None
