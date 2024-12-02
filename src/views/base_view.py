import customtkinter as ctk


# base_view.py
class BaseView:
    """Base class for all views in the application"""

    def __init__(self, master):
        self.master = master
        self.store = None
        self.frame = ctk.CTkFrame(self.master)
        
        # Stocker les paramètres de base pour le redimensionnement
        self._base_font_size = 12  # Taille de police de base
        self._base_padding = 10    # Padding de base
        self._min_font_size = 8    # Taille minimale de police
        self._max_font_size = 16   # Taille maximale de police

    def subscribe(self, store):
        self.store = store
        store.subscribe(self.update)

    def update(self, state):
        pass

    def adjust_ui(self, font_size=None, padding=None):
        """
        Méthode générique pour ajuster l'interface utilisateur.
        Peut être surchargée par les classes enfants pour des ajustements spécifiques.
        
        :param font_size: Taille de police à appliquer
        :param padding: Padding à appliquer
        """
        # Valider et ajuster la taille de police
        if font_size is not None:
            font_size = max(self._min_font_size, 
                            min(font_size, self._max_font_size))
        else:
            font_size = self._base_font_size

        # Valider et ajuster le padding
        if padding is not None:
            padding = max(5, padding)  # Padding minimal de 5
        else:
            padding = self._base_padding

        # Méthode pour ajuster récursivement les widgets enfants
        def adjust_children(parent, font_size, padding):
            for widget in parent.winfo_children():
                # Ajuster les polices pour différents types de widgets
                if isinstance(widget, (ctk.CTkLabel, ctk.CTkButton, ctk.CTkEntry)):
                    try:
                        widget.configure(font=("", font_size))
                    except Exception:
                        pass

                # Ajuster le padding si possible
                try:
                    widget.configure(padx=padding//2, pady=padding//2)
                except Exception:
                    pass

                # Récursivité pour les conteneurs
                if hasattr(widget, 'winfo_children'):
                    adjust_children(widget, font_size, padding)

        # Appliquer les ajustements aux enfants du frame
        adjust_children(self.frame, font_size, padding)

        # Méthode à surcharger dans les classes enfants pour des ajustements spécifiques
        self._specific_ui_adjustments(font_size, padding)

    def _specific_ui_adjustments(self, font_size, padding):
        """
        Méthode à surcharger dans les classes enfantes pour des ajustements spécifiques.
        Par défaut, elle ne fait rien.
        """
        pass