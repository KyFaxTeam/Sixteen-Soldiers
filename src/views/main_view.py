import customtkinter as ctk
from models.sauvegarde import Sauvegarde
from views.base_view import BaseView
from views.sauvegarde_view import SauvegardeView
from .plateau_view import PlateauView
from .joueur_view import JoueurView
from .historique_view import HistoriqueView

class MainView(BaseView):
    """Main window of the application"""
    def __init__(self):
        # Configure main window
        self.window = ctk.CTk()
        self.window.title("Sixteen Soldiers")
        self.window.geometry("1200x800")
        
        # Create main layout
        self.left_panel = ctk.CTkFrame(self.window, width=300)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)
        
        self.center_panel = ctk.CTkFrame(self.window)
        self.center_panel.pack(side="left", expand=True, fill="both", padx=10, pady=10)
        
        self.right_panel = ctk.CTkFrame(self.window, width=300)
        self.right_panel.pack(side="right", fill="y", padx=10, pady=10)
        
        # Initialize sub-views
        self.joueur_view = JoueurView(self.left_panel)
        self.plateau_view = PlateauView(self.center_panel)
        self.historique_view = HistoriqueView(self.right_panel)
        
        # Initialize Sauvegarde (Store) and SauvegardeView
        #self.sauvegarde = Sauvegarde()
        #self.sauvegarde_view = SauvegardeView(self.left_panel, self.plateau_view, self.joueur_view, self.sauvegarde)
        
    def run(self):
        """Start the application"""
        self.window.mainloop()

