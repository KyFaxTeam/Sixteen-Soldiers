import customtkinter as ctk
from src.models.assets.index import Assets
from src.store.store import Store
from src.utils.audio import Sounds 
from src.views.base_view import BaseView
from src.utils.const import EMOJIS_SIZE, THEME_PATH
from PIL import Image, ImageTk

class SettingsView(BaseView):
    """View for game settings, including speed, sound control, and dark mode"""
    def __init__(self, master, store:Store = None):
        super().__init__(master)
        self.frame = ctk.CTkFrame(self.master, corner_radius=10)
        self.store = store
        if self.store:
            self.subscribe(self.store)
        self.frame.configure(corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.sounds = Sounds()

        # Title "Settings"
        self.frame.setting = ctk.CTkImage(Image.open(Assets.setting).resize(EMOJIS_SIZE))

        self.title = ctk.CTkLabel(
            self.frame,
            image=self.frame.setting,
            text=" Settings",
            font=ctk.CTkFont(size=13, weight="bold"),
            compound="left"
        )
        self.title.pack(pady=(5, 5))

        # Speed control section
        self.speed_section = ctk.CTkFrame(self.frame, corner_radius=8)
        self.speed_section.pack(fill="x", padx=10, pady=10)

        self.speed_label = ctk.CTkLabel(
            self.speed_section,
            text="⏩ Speed",
            font=ctk.CTkFont(size=11),
            # text_color="#cccccc"
        )
        self.speed_label.pack(anchor="w", padx=10, pady=5)

        self.speed_slider = ctk.CTkSlider(
            self.speed_section, 
            from_=0.5, 
            to=2.5, 
            number_of_steps=5,
            command=self._on_speed_change,            
        )
        self.speed_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Sound control section avec boutons segmentés
        self.sound_section = ctk.CTkFrame(self.frame, corner_radius=8)
        self.sound_section.pack(fill="x", padx=10, pady=5)

        self.sound_label = ctk.CTkLabel(
            self.sound_section,
            text="🔊 Sound",
            font=ctk.CTkFont(size=11),
            # text_color="#cccccc"
        )
        self.sound_label.pack(anchor="w", padx=10, pady=5)

        # Boutons segmentés pour le contrôle du son
        self.sound_control = ctk.CTkSegmentedButton(
            self.sound_section,
            values=["On", "Off"],
            command=self._on_sound_change,
            font=ctk.CTkFont(size=8)
        )
        self.sound_control.pack(padx=15, pady=(0, 10))
        self.sound_control.set("On")  # Valeur par défaut

        # Dark Mode section
        self.theme_section = ctk.CTkFrame(self.frame, corner_radius=8)
        self.theme_section.pack(fill="x", padx=10, pady=10)

        self.theme_label = ctk.CTkLabel(
            self.theme_section,
            text="🌓 Appearance",
            font=ctk.CTkFont(size=11),
            # text_color="#cccccc"
        )
        self.theme_label.pack(anchor="w", padx=10, pady=5)

        # Boutons segmentés pour le thème
        self.theme_control = ctk.CTkSegmentedButton(
            self.theme_section,
            values=["Light", "Dark", "System"],
            command=self._on_theme_change,
            font=ctk.CTkFont(size=8)
        )
        self.theme_control.pack(padx=15, pady=(0, 10))
        self.theme_control.set("System")  # Valeur par défaut

    def _on_speed_change(self, value):
        """Gère le changement de vitesse"""
        # print(f"Speed changed to: {value}")
        self.store.game_speed.set_speed(value)


    def _on_sound_change(self, value):
        """Gère le changement de volume"""
        # print(f"Sound changed to: {value}")
        if value == "Off":
            self.sounds.pause()
        # elif value == "Low":
        #     # Volume bas
        #     pass
        elif value == "On":
            self.sounds.unpause()

    def _on_theme_change(self, value):
        """Handle theme change"""
        # print(f"Theme changed to: {value}")
        if value == "Dark":
            ctk.set_appearance_mode("dark")
            # ctk.set_default_color_theme(THEME_PATH)
        elif value == "Light":
            ctk.set_appearance_mode("light")
            # ctk.set_default_color_theme(THEME_PATH)
        else:  # System
            ctk.set_appearance_mode("system")
            value = ctk.get_appearance_mode()
            # You can set a default theme for 'system' mode if needed
        self.store.update_theme(value)


    def get_settings(self):
        """Retourne les paramètres actuels"""
        return {
            "speed": self.speed_slider.get(),
            "sound": self.sound_control.get(),
            "theme": self.theme_control.get()
        }
    def load_settings(self, settings: dict):
        
        """Charge des paramètres"""
        if "speed" in settings:
            self.speed_slider.set(settings["speed"])
        if "sound" in settings:
            self.sound_control.set(settings["sound"])
        if "theme" in settings:
            self.theme_control.set(settings["theme"])

    def update(self, state):
        """Update settings view based on the state"""
        # ...update logic if needed...