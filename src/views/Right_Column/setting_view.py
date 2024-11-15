import customtkinter as ctk
from utils.audio import Sounds 
from views.base_view import BaseView
from utils.const import THEME_PATH

class SettingsView(BaseView):
    """View for game settings, including speed, sound control, and dark mode"""
    def __init__(self, master):
        super().__init__(master)
        self.frame.configure(corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.sounds = Sounds()

        # Title "Settings"
        self.title = ctk.CTkLabel(
            self.frame,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.title.pack(pady=(5, 5))

        # Speed control section
        self.speed_section = ctk.CTkFrame(self.frame, corner_radius=8)
        self.speed_section.pack(fill="x", padx=10, pady=10)

        self.speed_label = ctk.CTkLabel(
            self.speed_section,
            text="⏩ Speed",
            font=ctk.CTkFont(size=11),
            text_color="#cccccc"
        )
        self.speed_label.pack(anchor="w", padx=10, pady=5)

        self.speed_slider = ctk.CTkSlider(
            self.speed_section, 
            from_=0, 
            to=1, 
            number_of_steps=5,
            command=self._on_speed_change
        )
        self.speed_slider.pack(fill="x", padx=15, pady=(0, 10))

        # Sound control section avec boutons segmentés
        self.sound_section = ctk.CTkFrame(self.frame, corner_radius=8)
        self.sound_section.pack(fill="x", padx=10, pady=5)

        self.sound_label = ctk.CTkLabel(
            self.sound_section,
            text="🔊 Sound",
            font=ctk.CTkFont(size=11),
            text_color="#cccccc"
        )
        self.sound_label.pack(anchor="w", padx=10, pady=5)

        # Boutons segmentés pour le contrôle du son
        self.sound_control = ctk.CTkSegmentedButton(
            self.sound_section,
            values=["Off", "On"],
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
            text_color="#cccccc"
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
        speed_value = round(value, 2)
        print(f"Speed changed to: {speed_value}")
        # TODO: Implémenter la logique de changement de vitesse

    def _on_sound_change(self, value):
        """Gère le changement de volume"""
        print(f"Sound changed to: {value}")
        if value == "Off":
            self.sounds.pause()
        # elif value == "Low":
        #     # Volume bas
        #     pass
        elif value == "On":
            self.sounds.unpause()

    def _on_theme_change(self, value):
        """Handle theme change"""
        print(f"Theme changed to: {value}")
        if value == "Dark":
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme(THEME_PATH)
        elif value == "Light":
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme(THEME_PATH)
        else:  # System
            ctk.set_appearance_mode("system")
            # You can set a default theme for 'system' mode if needed

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
