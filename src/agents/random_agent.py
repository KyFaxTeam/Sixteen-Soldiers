from agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    """
    Agent IA jouant des coups aléatoires, hérite de BaseAgent.
    """

    def choixAction(self, plateau, joueur):
        """
        Choisit une action aléatoire parmi les mouvements et captures valides pour le joueur.

        Parameters:
            plateau (Plateau): L'état actuel du plateau de jeu.
            joueur (Joueur): Le joueur pour lequel l'action est choisie.

        Returns:
            Action: L'action choisie aléatoirement pour le joueur.
        """
