from typing import List, Optional
from typing import Tuple
import customtkinter as ctk
from views.base_view import BaseView


class PlateauView(BaseView):
    """View for the game board"""
    def __init__(self, master):
        super().__init__(master)
        self.frame.pack(expand=True, fill="both")
        
        # Canvas for drawing the board
        self.canvas = ctk.CTkCanvas(
            self.frame,
            width=600,
            height=600,
            background="white"
        )
        self.canvas.pack(expand=True)
        
        # Store board coordinates
        self.points: List[Tuple[int, int]] = []
        self.selected_point: Optional[int] = None
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        
        self._init_board()
        
    def _init_board(self):
        """Initialize the board layout"""
        # Calculate board dimensions
        width = self.canvas.winfo_reqwidth()
        height = self.canvas.winfo_reqheight()
        margin = 50
        
        # Store point coordinates and draw connections
        # This will be implemented in detail in the full view implementation
        pass
        
    def draw_piece(self, x: int, y: int, color: str):
        """Draw a game piece at the specified coordinates"""
        radius = 15
        self.canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            fill=color,
            outline="black"
        )

    def on_click(self, event):
        """Handle mouse clicks on the board"""
        # Find closest point and dispatch move action if valid
        pass

