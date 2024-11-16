import os
from models.assets.index import Assets
import random
import customtkinter as ctk
from typing import Optional
from views.base_view import BaseView
from PIL import Image


class PlayerView(BaseView):
    def __init__(self, master: any, store: Optional[any] = None):
        super().__init__(master)
        self.store = store
        if store:
            self.subscribe(store)
            initial_state = store.get_state()
            initial_time = initial_state.get("time_manager", {}).get_remaining_time(initial_state["players"][0].id)
            initial_pieces = len([p for p in initial_state["board"].pieces if p.player_id == initial_state["players"][0].id])
        else:
            initial_time = "---"
            initial_pieces = "---"
        
        self.joueur_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=6
        )
        self.joueur_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.joueur_frame.grid_columnconfigure(0, weight=1)
        
        # Avatar container
        self.avatar_container = ctk.CTkFrame(
            self.joueur_frame,
            fg_color="transparent",
            height=80
        )
        self.avatar_container.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        self.avatar_container.grid_propagate(False)
        
        # Enhanced avatar with random image
        self.avatar_image = self.load_random_avatar()
        self.avatar = ctk.CTkLabel(
            self.avatar_container,
            text="",
            image=ctk.CTkImage(
                light_image=self.avatar_image,
                dark_image=self.avatar_image,
                size=(60, 60)
            )
        )
        self.avatar.place(relx=0.5, rely=0.5, anchor="center")
        
        # Info section
        self.info_frame = ctk.CTkFrame(
            self.joueur_frame,
            fg_color="transparent"
        )
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        
        # Stats container
        self.stats_container = ctk.CTkFrame(
            self.info_frame,
            corner_radius=6
        )
        self.stats_container.pack(fill="x", pady=5)
        
        # Timer with icon
        self.timer_frame = ctk.CTkFrame(
            self.stats_container,
            fg_color="transparent"
        )
        self.timer_frame.pack(side="left", padx=10, pady=5)
        
        self.timer_icon = ctk.CTkLabel(
            self.timer_frame,
            text="⏱️",
            font=ctk.CTkFont(size=14)
        )
        self.timer_icon.pack(side="left", padx=(0, 5))

        self.timer_label = ctk.CTkLabel(
            self.timer_frame,
            text=f"{initial_time}s",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.timer_label.pack(side="left")
        
        # Pieces with icon
        self.pieces_frame = ctk.CTkFrame(
            self.stats_container,
            fg_color="transparent"
        )
        self.pieces_frame.pack(side="right", padx=10, pady=5)
        
        self.pieces_icon = ctk.CTkLabel(
            self.pieces_frame,
            text="♟️",
            font=ctk.CTkFont(size=14)
        )
        self.pieces_icon.pack(side="left", padx=(0, 5))

        self.pieces_label = ctk.CTkLabel(
            self.pieces_frame,
            text=str(initial_pieces),
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.pieces_label.pack(side="left")
        
        # Player name
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text="Select an agent",  # Changed default text to prompt user
            font=ctk.CTkFont(size=12)
        )
        self.name_label.pack(pady=5)
        
        # Agent selection dropdown (initially hidden)
        self.agent_dropdown = None
        
        # Select button
        self.select_button = ctk.CTkButton(
            self.info_frame,
            text="Select",
            font=ctk.CTkFont(size=10),
            width=100,
            height=32,
            corner_radius=6,
            command=self.toggle_agent_dropdown
        )
        self.select_button.pack(pady=10)
        
        if store:
            self.subscribe(store)
        
    def get_agent_list(self):
        """Get list of available agents from the agents directory"""
        agents_dir = "agents"  # Adjust path as needed
        if os.path.exists(agents_dir):
            # Get all files from the agents directory, excluding __pycache__ and other hidden files
            agents = [f[:-3] for f in os.listdir(agents_dir) 
                     if f.endswith('.py') and not f.startswith('__')]
            return sorted(agents)
        return []
        
    def toggle_agent_dropdown(self):
        """Toggle the agent selection dropdown"""
        if self.agent_dropdown is None:
            # Create and show dropdown
            agents = self.get_agent_list()
            if agents:
                self.agent_dropdown = ctk.CTkOptionMenu(
                    self.info_frame,
                    values=agents,
                    width=120,
                    height=32,
                    corner_radius=6,
                    command=self.on_agent_selected
                )
                self.agent_dropdown.pack(pady=5)
                # Move the dropdown above the select button in the widget stacking order
                self.select_button.pack_forget()
                self.select_button.pack(pady=10)
        else:
            # Hide and destroy dropdown
            self.agent_dropdown.destroy()
            self.agent_dropdown = None
            
    def on_agent_selected(self, agent_name: str):
        """Handle agent selection"""
        # Update the name label with the selected agent
        self.name_label.configure(text=agent_name)
        
        # Update the store with the selected agent
        if self.store:
            self.store.dispatch({
                'type': 'SELECT_AGENT',
                'agent': agent_name,
                'joueur': {
                    'name': agent_name  # Include the name in the joueur update
                }
            })
        
        # Optionally hide the dropdown after selection
        self.toggle_agent_dropdown()

    def load_random_avatar(self):
        """Loads a random avatar from the assets/avatar directory"""
        avatar_dir = Assets.dir_avatar
        avatar_files = [f for f in os.listdir(avatar_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if avatar_files:
            random_avatar = random.choice(avatar_files)
            avatar_path = os.path.join(avatar_dir, random_avatar)
            return Image.open(avatar_path).convert('RGBA')
        else:
            fallback_image = Image.new('RGBA', (60, 60), (200, 200, 200, 255))
            return fallback_image

    def update(self, state: dict):
        """Updates the interface with new state"""
        if not state:
            return

        # Get current player information
        current_player_index = state.get('current_player_index', 0)
        players = state.get('players', [])
        
        if not players:
            return
            
        current_player = players[current_player_index]
        
        # Update timer from time manager
        if 'time_manager' in state:
            remaining_time = state['time_manager'].get_remaining_time(current_player.id)
            self.timer_label.configure(text=f"{int(remaining_time)}s")
        
        # Update pieces count from board state
        if 'board' in state:
            pieces_count = sum(1 for piece in state['board'].pieces 
                             if piece.player_id == current_player.id)
            self.pieces_label.configure(text=str(pieces_count))
        
        # Update player name if no agent selection is in progress
        if not self.agent_dropdown:
            self.name_label.configure(text=current_player.name or 'Select an agent')