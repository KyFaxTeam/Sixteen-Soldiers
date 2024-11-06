from models.sauvegarde import Sauvegarde
from views.base_view import BaseView
from views.joueur_view import JoueurView
from views.plateau_view import PlateauView
import customtkinter as ctk

class SauvegardeView(BaseView):
    """Vue pour la sauvegarde et le chargement de la partie"""
    
    def __init__(self, master, plateau_view: PlateauView, joueur_view: JoueurView, sauvegarde: Sauvegarde):
        super().__init__(master)
        self.frame.pack(fill="both", padx=10, pady=10)
        
        self.plateau_view = plateau_view
        self.joueur_view = joueur_view
        self.sauvegarde = sauvegarde
        
        # S'abonner aux changements d'état pour mise à jour après chargement
        self.sauvegarde.subscribe(self.update_view)

        # Bouton pour sauvegarder la partie
        self.save_button = ctk.CTkButton(
            self.frame,
            text="Sauvegarder la Partie",
            command=self.save_game
        )
        self.save_button.pack(pady=5)

        # Bouton pour charger la partie
        self.load_button = ctk.CTkButton(
            self.frame,
            text="Charger la Partie",
            command=self.load_game
        )
        self.load_button.pack(pady=5)

    def save_game(self):
        """Appelle le reducer pour sauvegarder l'état actuel du jeu"""
        pass
       
    def load_game(self):
        """Appelle le reducer pour charger l'état du jeu"""
        pass

    def update_view(self, state):
        """Met à jour la vue après le chargement de l'état du jeu"""
        # Restaurer l'état du plateau
        pass

        # Restaurer l'état du joueur courant
        pass

        # Restaurer le score
        pass
    
        print("Vue mise à jour avec l'état chargé.")
