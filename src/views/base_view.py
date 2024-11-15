import customtkinter as ctk
from typing import List, Tuple, Optional

class BaseView:
    """Base class for all views in the application"""
    def __init__(self, master):
        self.frame = ctk.CTkFrame(master)
        self.store = None
    
    def subscribe(self, store):
        self.store = store
        store.subscribe(self.update)
    
    def update(self, state):
        pass
