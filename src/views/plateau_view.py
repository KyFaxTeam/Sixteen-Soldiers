from views.base_view import BaseView


class PlateauView(BaseView):
    def __init__(self, parent):
        super().__init__()
        # self.frame = ctk.CTkFrame(parent)
        # self.cells = []

        self.setup_board()
    
    def setup_board(self):
        pass

    def on_cell_click(self, position):
        self.store.dispatch({
            'type': 'SELECT_CELL',
            'position': position
        })
    
    def update(self, state):
        pass