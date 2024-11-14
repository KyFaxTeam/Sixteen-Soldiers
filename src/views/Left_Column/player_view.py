import os
from models.assets.index import Assets
import random
# Removed ThemeManager import
# from utils.theme_manager import ThemeManager
import customtkinter as ctk
from typing import Optional
from views.base_view import BaseView
from PIL import Image

class PlayerView(BaseView):
    def __init__(self, master: any, store: Optional[any] = None):
        super().__init__(master)
        self.store = store
        
        # Optional: Configure frame without ThemeManager
        # self.frame.configure(fg_color=ThemeManager.theme["CTkFrame"]["fg_color"])
        # If you don't need to set fg_color explicitly, you can remove the line

        self.joueur_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=6  # Set corner_radius directly
        )
        self.joueur_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Configure grid weights
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
        
        # Info section with better spacing
        self.info_frame = ctk.CTkFrame(
            self.joueur_frame,
            fg_color="transparent"
        )
        self.info_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        
        # Stats container without custom color
        self.stats_container = ctk.CTkFrame(
            self.info_frame,
            corner_radius=6  # Set corner_radius directly
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
            font=("Arial", 14)
        )
        self.timer_icon.pack(side="left", padx=(0, 5))

        self.timer_label = ctk.CTkLabel(
            self.timer_frame,
            text="120s",
            font=("Poppins", 14, "bold")  # Set font directly
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
            font=("Arial", 14)
        )
        self.pieces_icon.pack(side="left", padx=(0, 5))

        self.pieces_label = ctk.CTkLabel(
            self.pieces_frame,
            text="13",
            font=("Poppins", 14, "bold")  # Set font directly
        )
        self.pieces_label.pack(side="left")
        
        # Player name
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text="Pseudo",
            font=("Poppins", 12)  # Set font directly
        )
        self.name_label.pack(pady=5)
        
        # Select button
        self.select_button = ctk.CTkButton(
            self.info_frame,
            text="Select",
            font=("Poppins", 10),  # Set font directly
            width=100,
            height=32,
            corner_radius=6  # Set corner_radius directly
        )
        self.select_button.pack(pady=10)
        
    def load_random_avatar(self):
        """Loads a random avatar from the assets/avatar directory"""
        avatar_dir = Assets.dir_avatar
        avatar_files = [f for f in os.listdir(avatar_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if avatar_files:
            random_avatar = random.choice(avatar_files)
            avatar_path = os.path.join(avatar_dir, random_avatar)
            return Image.open(avatar_path).convert('RGBA')
        else:
            # Fallback if no images are found
            fallback_image = Image.new('RGBA', (60, 60), (200, 200, 200, 255))  # Gray placeholder
            return fallback_image

    def update(self, state: dict):
        """Updates the interface with new state"""
        if self.store:
            joueur = state.get('joueur', {})
            self.timer_label.configure(text=f"{joueur.get('timer', 0)}s")
            self.pieces_label.configure(text=str(joueur.get('pieces', 0)))
            self.name_label.configure(text=joueur.get('name', 'Pseudo'))
            
    # Removed the update_theme_colors method