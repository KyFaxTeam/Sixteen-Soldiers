import customtkinter as ctk
from typing import List, Tuple, Optional
import math

class BaseView:
    """Base class for all views in the application"""
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master)
        self.store = None
    
    def subscribe(self, store):
        """Subscribe to store updates"""
        self.store = store
        store.subscribe(self.update)
    
    def update(self, state):
        """
        Méthode abstraite à implémenter par les sous-classes
        Args:
            state (Dict): État global du store
        """
        pass  # Changed from raise NotImplementedError to allow optional implementation
