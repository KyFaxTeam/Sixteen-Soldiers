from utils.theme import ThemeManager
import customtkinter as ctk
from typing import Optional
from views.base_view import BaseView
from PIL import Image, ImageDraw, ImageOps

class PlayerView(BaseView):
    def __init__(self, master: any, store: Optional[any] = None):
        super().__init__(master)
        self.store = store
        
        # Configure main frame
        self.frame.configure(fg_color=ThemeManager.get_color("background"))
        
        # Player card frame
        self.joueur_frame = ctk.CTkFrame(
            self.frame,
            corner_radius=ThemeManager.CORNER_RADIUS["frame"],
            fg_color=ThemeManager.get_color("surface"),
            border_width=ThemeManager.BORDER_WIDTH["frame"],
            border_color=ThemeManager.get_color("border")
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
        
        # Enhanced avatar
        self.avatar = ctk.CTkLabel(
            self.avatar_container,
            text="",
            image=ctk.CTkImage(
                light_image=self.create_enhanced_avatar(ThemeManager.get_color("surface")),
                dark_image=self.create_enhanced_avatar(ThemeManager.get_color("background")),
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
        
        # Stats container (Timer and Pieces)
        self.stats_container = ctk.CTkFrame(
            self.info_frame,
            fg_color=ThemeManager.get_color("surface_variant"),
            corner_radius=ThemeManager.CORNER_RADIUS["card"]
        )
        self.stats_container.pack(fill="x", pady=5)
        
        # Timer with icon (using emoji as placeholder)
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
            font=ThemeManager.get_font("heading"),
            text_color=ThemeManager.get_color("text")
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
            font=ThemeManager.get_font("heading"),
            text_color=ThemeManager.get_color("text")
        )
        self.pieces_label.pack(side="left")
        
        # Player name with enhanced style
        self.name_label = ctk.CTkLabel(
            self.info_frame,
            text="Pseudo",
            font=ThemeManager.get_font("subheading"),
            text_color=ThemeManager.get_color("text_secondary")
        )
        self.name_label.pack(pady=5)
        
        # Enhanced select button
        self.select_button = ctk.CTkButton(
            self.info_frame,
            text="Select",
            font=ThemeManager.get_font("button"),
            width=100,
            height=32,
            fg_color=ThemeManager.get_color("primary"),
            hover_color=ThemeManager.get_color("primary_hover"),
            corner_radius=ThemeManager.CORNER_RADIUS["button"]
        )
        self.select_button.pack(pady=10)

    def create_enhanced_avatar(self, bg_color: str):
        """Creates an enhanced avatar with better styling"""
        img = Image.new('RGB', (120, 120), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Outer circle (subtle glow)
        draw.ellipse([10, 10, 110, 110], 
                    fill=ThemeManager.get_color("primary_variant"))
        
        # Inner circle (main avatar)
        draw.ellipse([15, 15, 105, 105], 
                    fill=bg_color,
                    outline=ThemeManager.get_color("primary"),
                    width=3)
        
        # Add simple face outline
        draw.ellipse([45, 35, 75, 65],  # Head
                    outline=ThemeManager.get_color("text"),
                    width=2)
        draw.arc([35, 55, 85, 85],  # Smile
                180, 0,
                fill=ThemeManager.get_color("text"),
                width=2)
        
        return ImageOps.contain(img, (60, 60))
        
    def update(self, state: dict):
        """Updates the interface with new state"""
        if self.store:
            joueur = state.get('joueur', {})
            self.timer_label.configure(text=f"{joueur.get('timer', 0)}s")
            self.pieces_label.configure(text=str(joueur.get('pieces', 0)))
            self.name_label.configure(text=joueur.get('name', 'Pseudo'))
            
    def update_theme(self):
        """Updates colors and styles on theme change"""
        self.frame.configure(fg_color=ThemeManager.get_color("background"))
        self.joueur_frame.configure(
            fg_color=ThemeManager.get_color("surface"),
            border_color=ThemeManager.get_color("border")
        )
        
        self.stats_container.configure(
            fg_color=ThemeManager.get_color("surface_variant")
        )
        
        self.avatar.configure(
            image=ctk.CTkImage(
                light_image=self.create_enhanced_avatar(ThemeManager.get_color("surface")),
                dark_image=self.create_enhanced_avatar(ThemeManager.get_color("background")),
                size=(60, 60)
            )
        )
        
        for label in [self.timer_label, self.pieces_label]:
            label.configure(text_color=ThemeManager.get_color("text"))
        
        self.name_label.configure(text_color=ThemeManager.get_color("text_secondary"))
        
        self.select_button.configure(
            fg_color=ThemeManager.get_color("primary"),
            hover_color=ThemeManager.get_color("primary_hover")
        )