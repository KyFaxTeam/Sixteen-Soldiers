import os  # Import os module for path operations
import customtkinter as ctk
from PIL import Image
from views.base_view import BaseView
from utils.const import ASSETS_DIR  # Import ASSETS_DIR

class AfterGameView(ctk.CTkToplevel):
    def __init__(self, master, store, on_restart, on_save):
        super().__init__(master)
        self.store = store
        self.on_restart = on_restart
        self.on_save = on_save
        if self.store:
            self.subscribe(self.store)
        
        # Configure window to overshadow MainView
        self.title("Game Over")
        self.geometry("400x300")
        self.transient(master)
        self.grab_set()  # Block interaction with MainView

        # Fetch winner's data from store
        state = self.store.get_state()
        winner_data = self.get_winner_data(state)
        
        # Winner's data
        profile_img_path = winner_data.get("profile_img")
        team_pseudo = winner_data.get("team_pseudo", "Unknown")
        ai_name = winner_data.get("ai_name", "AI")
        remaining_time = winner_data.get("remaining_time", "00:00")
        remaining_pawns = winner_data.get("remaining_pawns", 0)

        # Display "Gagnant" title
        ctk.CTkLabel(self, text="Gagnant", font=("Helvetica", 24, "bold")).pack(pady=(20, 10))

        # Display profile picture
        self.profile_image = ctk.CTkLabel(self, text="")
        if profile_img_path:
            # Use os.path.join to construct the full path
            profile_img_full_path = os.path.join(ASSETS_DIR, profile_img_path)
            image = Image.open(profile_img_full_path)
            self.photo = ctk.CTkImage(image, size=(100, 100))
            self.profile_image.configure(image=self.photo)
        self.profile_image.pack(pady=(0, 5))

        # Display winner's pseudo and AI name
        ctk.CTkLabel(self, text=f"{team_pseudo} - {ai_name}", font=("Helvetica", 18)).pack(pady=(0, 10))

        # Bottom frame for time, restart button, and save button
        bottom_frame = ctk.CTkFrame(self, height=40)
        bottom_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its children
        bottom_frame.pack(side="bottom", pady=(20, 10), fill="x", padx=20)

        # Display remaining time
        time_label = ctk.CTkLabel(bottom_frame, text=f"Time: {remaining_time}", font=("Helvetica", 12))
        time_label.grid(row=0, column=0, padx=10)

        # Display pawns remaining icon
        pawns_image_path = os.path.join(ASSETS_DIR, "images", "red_soldier.png")
        pawns_image = Image.open(pawns_image_path)
        self.pawns_photo = ctk.CTkImage(pawns_image, size=(20, 20))
        pawns_label = ctk.CTkLabel(bottom_frame, image=self.pawns_photo, text="")  # Display as icon only
        pawns_label.grid(row=0, column=1, padx=((25, 0)))

        # Display the number of remaining pawns next to the icon
        remaining_pawns_label = ctk.CTkLabel(bottom_frame, text=f': {remaining_pawns}', font=("Helvetica", 12))
        remaining_pawns_label.grid(row=0, column=2, padx=(0, 15))

        # Restart button with icon
        restart_image_path = os.path.join(ASSETS_DIR, "images", "refresh.png")
        restart_image = Image.open(restart_image_path).resize((25, 25))  # Adjust icon size as needed
        self.restart_photo = ctk.CTkImage(restart_image, size=(25, 25))
        restart_button = ctk.CTkButton(bottom_frame, image=self.restart_photo, text="", command=on_restart, width=30, height=30)
        restart_button.grid(row=0, column=3, padx=(30, 25))

        # Save button
        save_button = ctk.CTkButton(bottom_frame, text="Save", command=on_save, width=50)
        save_button.grid(row=0, column=4, padx=(75, 0))

    def subscribe(self, store):
        self.store = store
        store.subscribe(self.update)

    def get_winner_data(self, state):
        """Extract winner data from the state"""
        winner_agent_id = state.get("winner")
        if winner_agent_id is None:
            return self._get_default_winner_data()
            
        agents = state.get("agents", {})
        winner_data = agents.get(winner_agent_id)
        
        if not winner_data:
            return self._get_default_winner_data()
        
        return {
            "profile_img": winner_data["profile_img"],
            "team_pseudo": winner_data["team_pseudo"],
            "ai_name": winner_data["name"],
            "remaining_time": self.get_remaining_time(winner_data["player_id"]),
            "remaining_pawns": self.get_remaining_pawns(winner_data["player_id"])
        }

    def _get_default_winner_data(self):
        return {
            "profile_img": os.path.join("images", "kyfax_logo-removebg-preview.png"),
            "team_pseudo": "Unknown",
            "ai_name": "AI",
            "remaining_time": "00:00",
            "remaining_pawns": 0
        }

    def get_remaining_time(self, player_id):
        # ...existing code or new logic...
        if player_id:
            time_manager = self.store.get_state().get("time_manager")
            if time_manager:
                return time_manager.get_remaining_time(player_id)
        return "00:00"
    
    def get_remaining_pawns(self, player_id):
        # ...existing code or new logic...
        if player_id:
            board = self.store.get_state().get("board")
            if board:
                soldier_count = sum(
                    1 for position, owner in board.soldiers.items()
                    if owner == player_id
                )
                return soldier_count
        return 0

    def update(self, state):
        """Update the view when the state changes"""
        # ...update logic if needed...
        pass
