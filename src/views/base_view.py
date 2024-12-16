import customtkinter as ctk


# base_view.py
class BaseView:
    """Base class for all views in the application"""

    def __init__(self, master):
        self.master = master
        self.frame = ctk.CTkFrame(self.master)
        
        # Stocker les paramètres de base pour le redimensionnement
        self._base_font_size = 12  # Taille de police de base
        self._base_padding = 10    # Padding de base
        self._min_font_size = 8    # Taille minimale de police
        self._max_font_size = 16   # Taille maximale de police

    def subscribe(self, store):
        self.store = store
        store.subscribe(self.update)

    def update(self, state):

        pass

