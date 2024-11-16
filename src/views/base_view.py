import customtkinter as ctk
from typing import List, Tuple, Optional

# base_view.py
class BaseView:
    """Base class for all views in the application"""
    def __init__(self, master):
        self.master = master
        # Créez un frame pour les vues qui nécessitent un conteneur
        self.frame = ctk.CTkFrame(self.master)
        self.store = None
    
    def subscribe(self, store):
        self.store = store
        store.subscribe(self.update)
    
    def update(self, state):
        pass
