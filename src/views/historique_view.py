from views.base_view import BaseView


class HistoriqueView(BaseView):
    def __init__(self, parent):
        super().__init__()
        # self.frame = ctk.CTkFrame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        pass
    
    def update(self, state):
        pass
