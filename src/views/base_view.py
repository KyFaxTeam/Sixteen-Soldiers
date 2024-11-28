import customtkinter as ctk


# base_view.py
class BaseView:
    """Base class for all views in the application"""

    def __init__(self, master):
        self.master = master
        self.store = None
        self.frame = ctk.CTkFrame(self.master)

    def subscribe(self, store):
        self.store = store
        store.subscribe(self.update)

    def update(self, state):
        pass
