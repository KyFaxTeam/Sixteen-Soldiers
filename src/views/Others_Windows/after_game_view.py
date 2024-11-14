import customtkinter as ctk
from PIL import Image, ImageTk

class AfterGameView(ctk.CTkToplevel):
    def __init__(self, master, winner_data, on_restart, on_save):
        super().__init__(master)
        
        # Configure window to overshadow MainView
        self.title("Game Over")
        self.geometry("400x300")
        self.transient(master)
        self.grab_set()  # Block interaction with MainView

        # Winner's data
        profile_img_path = winner_data.get("profile_img")
        team_pseudo = winner_data.get("team_pseudo", "Unknown")
        ai_name = winner_data.get("ai_name", "AI")
        remaining_time = winner_data.get("remaining_time", "00:00")
        remaining_pawns = winner_data.get("remaining_pawns", 0)

        # Display profile picture
        self.profile_image = ctk.CTkLabel(self, text="")
        if profile_img_path:
            image = Image.open(profile_img_path).resize((80, 80))
            self.photo = ImageTk.PhotoImage(image)
            self.profile_image.configure(image=self.photo)
        self.profile_image.pack(pady=10)

        # Display winner details
        ctk.CTkLabel(self, text="Gagnant", font=("Helvetica", 18, "bold")).pack(pady=5)
        ctk.CTkLabel(self, text=f"{team_pseudo} - {ai_name}", font=("Helvetica", 14)).pack()

        # Display time and pawns left
        ctk.CTkLabel(self, text=f"Time: {remaining_time}").pack(pady=5)
        ctk.CTkLabel(self, text=f"Pawns Remaining: {remaining_pawns}").pack(pady=5)

        # Restart and Save buttons
        ctk.CTkButton(self, text="Restart", command=on_restart).pack(side="left", padx=10, pady=20)
        ctk.CTkButton(self, text="Save", command=on_save).pack(side="right", padx=10, pady=20)
