import logging
import customtkinter as ctk
from src.store.store import Store
from src.utils.const import Soldier
from src.views.base_view import BaseView
from src.views.Left_Column.player_view import PlayerView
logger = logging.getLogger(__name__)

class PlayersColumn(BaseView):
    def __init__(self, master: any, store: Store):
        super().__init__(master)
        self.store = store
        self.frame = ctk.CTkFrame(self.master)
        # self.frame.configure(fg_color="transparent")
        
        # Créez un conteneur principal qui utilisera grid
        self.main_container = ctk.CTkFrame(self.frame)
        self.main_container.pack(expand=True, fill="both")
        
        # Configure grid weights pour le main_container
        self.main_container.grid_rowconfigure(0, weight=40)
        self.main_container.grid_rowconfigure(1, weight=30)
        self.main_container.grid_rowconfigure(2, weight=40)
        self.main_container.grid_columnconfigure(0, weight=1)

        # Player 1
        self.player1 = PlayerView(self.main_container, soldier_value=Soldier.RED, store=store)
        self.player1.frame.grid(row=0, column=0, sticky="nsew", pady=(0, 0), padx=(0, 0))

        # VS Label container
        self.vs_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.vs_container.grid(row=1, column=0, sticky="nsew", pady=20)
        
        self.vs_label = ctk.CTkLabel(
            self.vs_container,
            text="VS",
            font=ctk.CTkFont(size=16, family="Tahoma", weight="bold")
        )
        self.vs_label.pack(expand = True)

        # Player 2
        self.player2 = PlayerView(self.main_container, soldier_value=Soldier.BLUE, store=store)
        self.player2.frame.grid(row=2, column=0, sticky="nsew", pady=(0, 0))

    def update(self, state: dict):

        """Update both players with new state"""
        self.player1.update(state)
        self.player2.update(state)