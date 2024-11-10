import customtkinter as ctk
from dataclasses import dataclass

@dataclass
class ThemeColors:
    primary: str
    secondary: str
    text: str
    background: str
    surface: str
    error: str
    success: str
    warning: str
    border: str     # Added border color
    primary_hover: str  # Added primary hover color
    primary_variant: str  # Added primary variant color
    surface_variant: str  # Added surface variant color
    text_secondary: str  # Added secondary text color

# Définition des thèmes constants
LIGHT_THEME = ThemeColors(
    primary="#007AFF",
    secondary="#5856D6",
    text="#000000",
    background="#FFFFFF",
    surface="#F2F2F7",
    error="#FF3B30",
    success="#34C759",
    warning="#FF9500",
    border="#E5E5EA",     # Light theme border
    primary_hover="#005ECF",  # Light theme hover
    primary_variant="#E1EBFF",  # Light blue variant
    surface_variant="#E5E5EA",  # Light surface variant
    text_secondary="#666666"  # Light theme secondary text
)

DARK_THEME = ThemeColors(
    primary="#0A84FF",
    secondary="#5E5CE6",
    text="#FFFFFF",
    background="#000000",
    surface="#1C1C1E",
    error="#FF453A",
    success="#32D74B",
    warning="#FF9F0A",
    border="#38383A",     # Dark theme border
    primary_hover="#0070DD",  # Dark theme hover
    primary_variant="#1C3D5A",  # Dark blue variant
    surface_variant="#2C2C2E",  # Dark surface variant
    text_secondary="#8E8E93"  # Dark theme secondary text
)

class ThemeManager:
    """Gestionnaire de thème global pour l'application"""
    
    # Définition des attributs de classe
    _current_theme = DARK_THEME
    
    FONTS = {
        "heading": ("Arial", 20),
        "subheading": ("Arial", 16),
        "body": ("Arial", 14),
        "small": ("Arial", 12),
        "button": ("Arial", 13, "bold")
    }
    
    CORNER_RADIUS = {
        "button": 8,
        "frame": 10,
        "input": 6,
        "card": 6  # Added card radius
    }
    
    BORDER_WIDTH = {
        "frame": 2,
        "button": 0,
        "input": 1
    }

    @classmethod
    def setup_theme(cls):
        """Configure le thème initial de l'application"""
        cls._current_theme = DARK_THEME
        ctk.set_default_color_theme("blue")  # Thème de base customtkinter
        ctk.set_appearance_mode("dark")     # Mode dark par défaut
        # Configuration du scaling des widgets
        ctk.set_widget_scaling(1.0)


    @classmethod
    def get_color(cls, color_name: str) -> str:
        """Récupère une couleur du thème actuel"""
        return getattr(cls._current_theme, color_name)

    @classmethod
    def get_font(cls, font_name: str) -> tuple:
        """Récupère une police de caractère"""
        return cls.FONTS[font_name]

    @classmethod
    def switch_theme(cls, theme_mode: str = "light"):
        """Change le thème global de l'application"""
        cls._current_theme = LIGHT_THEME if theme_mode == "light" else DARK_THEME
        ctk.set_appearance_mode(theme_mode)