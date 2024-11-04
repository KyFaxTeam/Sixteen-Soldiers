class BaseAgent:
    """
    Classe de base pour les agents IA du jeu Seize soldats.
    Fournit une interface pour les agents, leur permettant de choisir une action en fonction de l'état du plateau.
    """

    def choixAction(self, plateau, joueur):
        """
        Méthode abstraite pour choisir une action en fonction de l'état actuel du plateau et du joueur.
        
        Parameters:
            plateau (Plateau): L'état actuel du plateau de jeu.
            joueur (Joueur): Le joueur pour lequel l'action est choisie.

        Returns:
            Action: L'action choisie pour le joueur.
        """
        raise NotImplementedError("Cette méthode doit être implémentée dans les sous-classes.")
