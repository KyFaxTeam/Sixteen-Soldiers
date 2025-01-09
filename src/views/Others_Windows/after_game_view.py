import os
import customtkinter as ctk
from PIL import Image
from src.utils.audio import Sounds
from src.utils.const import  AGENT_AVATAR_DIR, TIMINGS, Soldier, GameEndReason
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
        
        # Winner's data"
        profile_img_path = winner_data.get("profile_img")
        team_pseudo = winner_data.get("team_pseudo")
        ai_name = winner_data.get("ai_name")
        soldier_value = winner_data.get("soldier_value")
         
        
        remaining_time = winner_data.get("remaining_time")
        remaining_pawns = winner_data.get("remaining_pawns")

        total_moves = winner_data.get("total_moves") if winner_data.get("total_moves") else len(state.get("history", []))//2

        reason = winner_data.get("reason")

        # Display "Gagnant" title
        ctk.CTkLabel(self, text="Winner", font=("Helvetica", 24, "bold")).pack(pady=(20, 10))

        # Display profile picturei,ik
        self.profile_image = ctk.CTkLabel(self, text="")
        if profile_img_path:
            image = Image.open(profile_img_path)
            self.photo = ctk.CTkImage(image, size=(100, 100))
            self.profile_image.configure(image=self.photo)
        self.profile_image.pack(pady=(0, 5))

        # Display winner's pseudo and AI name
        ctk.CTkLabel(self, text=f"{team_pseudo} - {ai_name}", font=("Helvetica", 18)).pack(pady=(0, 10))

        # reason_label = ctk.CTkLabel(
        #     self,
        #     text=f"Reason: {reason}",
        #     font=("Helvetica",14)
        # )
        # # if reason:
        # #     print(f'Reason: {reason}')
        # reason_label.place(relx=0.075, rely=0.675)

        # Reason label with "Reason" in blue
        reason_frame = ctk.CTkFrame(self, fg_color="transparent")  # Use a transparent frame to group labels
        reason_frame.place(relx=0.075, rely=0.675)
        # "Reason:" in blue
        reason_label_prefix = ctk.CTkLabel(
            reason_frame,
            text="Reason:",
            font=("Helvetica", 14),
            text_color="#7F00FF"
        )
        
        reason_label_prefix.pack(side="left")
        # The actual reason text
        reason_label_text = ctk.CTkLabel(
            reason_frame,
            text=f" {reason}",
            font=("Helvetica", 14)
        )
        reason_label_text.pack(side="left")

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
            text=f"Moves: {total_moves}",
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

    def on_closing(self):
        """Handle window closing event - just close the window"""
        try:
            self.sounds.unpause()
            self.destroy()

        except Exception as e:

            print(f"Error closing AfterGameView: {e}")

    def get_winner_data(self, state):
        """Extract winner data from the state"""
        winner = state.get("winner")
        reason = state.get("reason", "unknown")
        
        # Format the reason if it's an enum
        if isinstance(reason, GameEndReason):
            formatted_reason = reason.value
            if winner:
                formatted_reason = formatted_reason.format(color=winner.name)
        else:
            formatted_reason = str(reason)

        if reason == GameEndReason.FORFEIT: 
            info_index = state.get("agents_info_index", {}).get(winner)
            winner_data = state.get("agents", {}).get(info_index, {})
            self.profile_img = Assets.kyfax_logo
            
            extensions = ['.png', '.jpg', '.jpeg']
            for ext in extensions:
                if os.path.exists(os.path.join(AGENT_AVATAR_DIR, winner_data.get("pseudo")+ ext)):
                    self.profile_img = os.path.join(AGENT_AVATAR_DIR, winner_data.get("pseudo") + ext)
                    break
            default_data = {
                "profile_img": winner_data.get("profile_img"),
                "team_pseudo": winner_data.get("pseudo", "Unknown"),
                "ai_name": winner_data.get("name", "AI"),
                "soldier_value": winner_data.get('soldier_value'),
                "remaining_time": TIMINGS["AI_TIMEOUT"],
                "remaining_pawns": 16,
                "total_moves": 0,
                "reason": formatted_reason
        }

        if winner is None:
            # Personnaliser l'affichage selon la raison
            default_data = {
                "profile_img": Assets.kyfax_logo,
                "team_pseudo": "Draw",
                "ai_name": "",
                "soldier_value": None,
                "remaining_time": None,
                "remaining_pawns": None,
                "total_moves": len(state.get("history", [])) // 2,
                "reason": formatted_reason,
            }
            if reason == GameEndReason.DRAW_FEW_PIECES:
                default_data["team_pseudo"] = "Draw"
                default_data["ai_name"] = "Too few pieces"

            elif reason == GameEndReason.ERROR:
                default_data["team_pseudo"] = "Error"
                default_data["ai_name"] = "Invalid game"
            
            return default_data
        
        # Si on a un gagnant
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
            "total_moves": number_of_moves,
            "reason": formatted_reason 
        }

    def _get_default_winner_data(self):
        return {
            "profile_img": Assets.kyfax_logo,
            "team_pseudo": "Aucun",
            "ai_name": "Vainqueur",
            "remaining_time": None,
            "remaining_pawns": None,
            "total_moves": None,
            "reason": GameEndReason.ERROR.value  # Use enum value directly
        }



