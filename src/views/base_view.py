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
        """Update view based on new state"""
        raise NotImplementedError("Subclasses must implement update method")
