#import customtkinter as ctk
from views.base_view import BaseView
from .plateau_view import PlateauView
from .joueur_view import JoueurView
from .historique_view import HistoriqueView


class MainView(BaseView):
    def __init__(self):
        super().__init__()
        
        #self.window = ctk.CTk()
        #self.window.title("Seize Soldats")
        #self.window.geometry("1200x800")
        
        # Configuration du grid layout
        ## .....
        
        # Initialisation des sous-vues
        self.plateau_view = PlateauView(self.window)
        self.joueur_view = JoueurView(self.window)
        self.historique_view = HistoriqueView(self.window)
        
        self.setup_layout()
    
    def setup_layout(self):
        pass

    def update(self, state):
        self.plateau_view.update(state)
        self.joueur_view.update(state)
        self.historique_view.update(state)
    
    def run(self):
        self.window.mainloop()