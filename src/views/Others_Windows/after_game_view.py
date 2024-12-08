import os
import customtkinter as ctk
from PIL import Image
from src.utils.audio import Sounds
from src.utils.const import  Soldier
from src.utils.logger_config import get_logger
from src.models.assets.index import Assets

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
       
        self.transient(master)
        self.sounds.game_completed()

        # Fetch winner's data from store
        state = self.store.get_state()
        winner_data = self.get_winner_data(state)
        
        # Winner's data"qs
        profile_img_path = winner_data.get("profile_img")
        team_pseudo = winner_data.get("team_pseudo")
        ai_name = winner_data.get("ai_name")
        soldier_value = winner_data.get("soldier_value")
         
        
        remaining_time = winner_data.get("remaining_time")
        remaining_pawns = winner_data.get("remaining_pawns")

        total_moves = winner_data.get("total_moves") if winner_data.get("total_moves") else len(state.get("history", []))//2

        # Display "Gagnant" title
        ctk.CTkLabel(self, text="Gagnant", font=("Helvetica", 24, "bold")).pack(pady=(20, 10))

        # Display profile picturei,ik
        self.profile_image = ctk.CTkLabel(self, text="")
        if profile_img_path:
            image = Image.open(profile_img_path)
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
        remaining_time_ms = int(remaining_time * 1000) if remaining_time else "---"
        time_label = ctk.CTkLabel(bottom_frame, text=f"Time: {remaining_time_ms:03}ms", font=("Helvetica", 12))
        time_label.grid(row=0, column=0, padx=10)

        # Display pawns remaining icon
        if soldier_value == Soldier.BLUE:
            pawns_image  = Image.open(Assets.img_blue_soldier)
        elif soldier_value == Soldier.RED:
            pawns_image = Image.open(Assets.img_red_soldier)
        else:
            pawns_image = Image.open(Assets.img_empty_soldier)

        self.pawns_photo = ctk.CTkImage(pawns_image, size=(20, 20))
        pawns_label = ctk.CTkLabel(bottom_frame, image=self.pawns_photo, text="")  
        pawns_label.grid(row=0, column=1, padx=((10, 0)))

        # Display the number of remaining pawns next to the icon
        remaining_pawns_label = ctk.CTkLabel(bottom_frame, text=f': {remaining_pawns if remaining_pawns else "---"}', font=("Helvetica", 12))
        remaining_pawns_label.grid(row=0, column=2, padx=(0, 15))

        # Restart button with icon
        restart_image_path = Assets.icon_refresh
        restart_image = Image.open(restart_image_path).resize((25, 25))
        self.restart_photo = ctk.CTkImage(restart_image, size=(25, 25))
        

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
        if self.store.get_state().get("game_mode") == 'replay':
            save_button.configure(state="disabled")


        # Add protocol for window close button (X)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grab_set()  # Rend la fenêtre modale

    def get_winner_data(self, state):
        """Extract winner data from the state"""
        winner = state.get("winner")
        if winner is None:
            # self.logger.info("No winner found in state")
            return self._get_default_winner_data()
            
        info_index = state.get("agents_info_index", {}).get(winner)
        #self.logger.info(f"info_index: {info_index}")
        winner_data = state.get("agents", {}).get(info_index, {})
        # self.logger.info(winner_data)
        
        if not winner_data:
            self.logger.warning("No winner data found")
            return self._get_default_winner_data()

        # Get the latest performance from agent stats
        performances = winner_data.get("performances", [])
        latest_time = None
        number_of_moves = 0
        if performances:
            latest_performance = performances[-1]
            latest_time = latest_performance['time']
            number_of_moves = latest_performance['number_of_moves']
            reason = latest_performance.get("reason")

        return {
            "profile_img": winner_data.get("profile_img"),
            "team_pseudo": winner_data.get("pseudo", "Unknown"),
            "ai_name": winner_data.get("name", "AI"),
            "soldier_value": winner_data.get('soldier_value'),
            "remaining_time": latest_time,
            "remaining_pawns": self.store.get_state().get("board").count_soldiers(winner_data.get('soldier_value')),
            "total_moves": number_of_moves
        }

    def _get_default_winner_data(self):
        return {
            "profile_img": Assets.kyfax_logo,
            "team_pseudo": "Aucun",
            "ai_name": "Vainqueur",
            "remaining_time": None,
            "remaining_pawns": None,
            "total_moves": None
        }

    def on_closing(self):
        """Handle window closing event properly"""
        try:
            self.grab_release()  # Relâche le focus modal
            self.master.focus_set()  # Redonne le focus à la fenêtre principale
            self.destroy()  # Détruit la fenêtre
        except Exception as e:
            print(f"Error closing AfterGameView: {e}")


