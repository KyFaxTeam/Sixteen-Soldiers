from views.base_view import BaseView


class JoueurView(BaseView):
    def __init__(self, parent):
        super().__init__()
        # self.frame = ctk.CTkFrame(parent)
        # self.setup_ui()
    
    def setup_ui(self):
        # Info joueur et contrôles
        
        # Boutons de contrôle
        self.setup_control_buttons()
    
    def setup_control_buttons(self):
        buttons = [
            ("Annuler", lambda: self.store.dispatch({'type': 'UNDO_MOVE'})),
            ("Recommencer", lambda: self.store.dispatch({'type': 'RESET_GAME'})),
            ("Sauvegarder", lambda: self.store.dispatch({'type': 'SAVE_GAME'}))
        ]
        
        # for text, command in buttons:
        #     ctk.CTkButton(self.frame, text=text, command=command).pack(pady=5, padx=10, fill="x")
