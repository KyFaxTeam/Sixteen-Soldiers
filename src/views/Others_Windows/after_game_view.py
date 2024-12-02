import os
import customtkinter as ctk
from PIL import Image
from src.utils.audio import Sounds
from src.utils.const import ASSETS_DIR, Soldier
from src.utils.logger_config import get_logger

class AfterGameView(ctk.CTkToplevel):
    def __init__(self, master, store, on_restart, on_save):
        super().__init__(master)
        self.logger = get_logger(__name__)
        self.store = store
        self.on_restart = on_restart
        self.on_save = on_save
        self.sounds = Sounds()
        self.sounds.pause()
        
        # Configure window to overshadow MainView
        self.title("Game Over")
        # Center the popup
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"400x300+{(screen_width-400)//2}+{(screen_height-300)//2}")
        # self.geometry("400x300")
        self.transient(master)
        self.grab_set()  # Block interaction with MainView
        self.sounds.game_completed()
        # self.logger.info("**************Game Over window created*************")
        # Fetch winner's data from store
        state = self.store.get_state()
        winner_data = self.get_winner_data(state)
        
        # Winner's data"qs
        profile_img_path = winner_data.get("profile_img")
        team_pseudo = winner_data.get("team_pseudo")
        ai_name = winner_data.get("ai_name")
        soldier_value = winner_data.get("soldier_value")
        if soldier_value == Soldier.BLUE:
            pawns_image_filename = "blue_soldier.png"
        else:
            pawns_image_filename = "red_soldier.png"  # Default to red if value is null or not BLUE
        remaining_time = winner_data.get("remaining_time")
        remaining_pawns = winner_data.get("remaining_pawns")

        total_moves = int(len(state.get("history", [])) / 2)

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

        # Bottom frame for time, restart button, moves and save button
        bottom_frame = ctk.CTkFrame(self, height=40)
        bottom_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its children
        bottom_frame.pack(side="bottom", pady=(20, 10), fill="x", padx=20)

        # Display remaining time
        remaining_time_ms = int(remaining_time * 1000)  
        time_label = ctk.CTkLabel(bottom_frame, text=f"Time: {remaining_time_ms:03}ms", font=("Helvetica", 12))
        time_label.grid(row=0, column=0, padx=10)

        # Display pawns remaining icon
        pawns_image_path = os.path.join(ASSETS_DIR, "images", pawns_image_filename)
        pawns_image = Image.open(pawns_image_path)
        self.pawns_photo = ctk.CTkImage(pawns_image, size=(20, 20))
        pawns_label = ctk.CTkLabel(bottom_frame, image=self.pawns_photo, text="")  
        pawns_label.grid(row=0, column=1, padx=((10, 0)))

        # Display the number of remaining pawns next to the icon
        remaining_pawns_label = ctk.CTkLabel(bottom_frame, text=f': {remaining_pawns}', font=("Helvetica", 12))
        remaining_pawns_label.grid(row=0, column=2, padx=(0, 15))

        # Restart button with icon
        try:
            restart_image_path = os.path.join(ASSETS_DIR, "images", "refresh.png")
            if os.path.exists(restart_image_path):
                restart_image = Image.open(restart_image_path).resize((25, 25))
                self.restart_photo = ctk.CTkImage(restart_image, size=(25, 25))
            else:
                self.logger.warning(f"Refresh icon not found at {restart_image_path}")
                self.restart_photo = None
        except Exception as e:
            self.logger.error(f"Failed to load restart image: {e}")
            self.restart_photo = None

        # Create restart button with or without image
        restart_button = ctk.CTkButton(
            bottom_frame, 
            image=self.restart_photo if self.restart_photo else None,
            text="Restart" if not self.restart_photo else "",
            command=on_restart,
            width=30 if self.restart_photo else 80,
            height=30
        )
        restart_button.grid(row=0, column=3, padx=(10, 25))

        # Add label for total moves made by the winner
        total_moves_label = ctk.CTkLabel(
            bottom_frame, 
            text=f"Coups: {total_moves}", 
            font=("Helvetica", 12)
        )
        total_moves_label.grid(row=0, column=4, padx=((0, 0)))

        
        # Save button
        save_button = ctk.CTkButton(bottom_frame, text="Save", command=lambda: on_save(save_button), width=50)
        save_button.grid(row=0, column=5, padx=(25, 0))


    def get_winner_data(self, state):
        """Extract winner data from the state"""
        winner = state.get("winner")
        if winner is None:
            self.logger.info("No winner found in state")
            return self._get_default_winner_data()
            
        info_index = state.get("agents_info_index", {}).get(winner)
        #self.logger.info(f"info_index: {info_index}")
        winner_data = state.get("agents", {}).get(info_index, {})
        self.logger.info(winner_data)

        if not winner_data:
            self.logger.warning("No winner data found")
            return self._get_default_winner_data()

        # Get the latest performance from agent stats
        stats = winner_data.get("stats", {})
        performances = stats.get("performances", [])
        latest_time = "00:00"
        if performances:
            latest_time = performances[-1].time  # Le temps est déjà sauvegardé par conclude_game

        return {
            "profile_img": winner_data.get("profile_img"),
            "team_pseudo": winner_data.get("pseudo", "Unknown"),
            "ai_name": winner_data.get("name", "AI"),
            "soldier_value": winner_data.get('soldier_value'),
            "remaining_time": latest_time,
            "remaining_pawns": self.get_remaining_pawns(winner)
        }

    def _get_default_winner_data(self):
        return {
            "profile_img": os.path.join("images", "kyfax_logo-removebg-preview.png"),
            "team_pseudo": "Aucun",
            "ai_name": "Vainqueur",
            "remaining_time": "---ms",
            "remaining_pawns": 0
        }


    
    def get_remaining_pawns(self, soldier_value):
        # ...existing code or new logic...
        if soldier_value:
            board = self.store.get_state().get("board")
            if board:
                soldier_count = sum(
                    1 for position, owner in board.soldiers.items()
                    if owner == soldier_value
                )
                return soldier_count
        return 0

    # def update(self, state):
    #     """Update the view when the state changes"""
    #     # ...update logic if needed...
    #     pass
