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

        # Display "Gagnant" title
        ctk.CTkLabel(self, text="Gagnant", font=("Helvetica", 24, "bold")).pack(pady=(20, 10))

        # Display profile picture
        self.profile_image = ctk.CTkLabel(self, text="")
        if profile_img_path:
            image = Image.open(profile_img_path).resize((100, 100))
            self.photo = ImageTk.PhotoImage(image)
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
        pawns_image = Image.open("assets/images/red_soldier.png").resize((20, 20))  # Assuming icon size of 20x20 pixels
        self.pawns_photo = ImageTk.PhotoImage(pawns_image)
        pawns_label = ctk.CTkLabel(bottom_frame, image=self.pawns_photo, text="")  # Display as icon only
        pawns_label.grid(row=0, column=1, padx=((25, 0)))

        # Display the number of remaining pawns next to the icon
        remaining_pawns_label = ctk.CTkLabel(bottom_frame, text=f': {remaining_pawns}', font=("Helvetica", 12))
        remaining_pawns_label.grid(row=0, column=2, padx=(0, 15))

        # Restart button with icon
        restart_image = Image.open("assets/images/refresh.png").resize((25, 25))  # Adjust icon size as needed
        self.restart_photo = ImageTk.PhotoImage(restart_image)
        restart_button = ctk.CTkButton(bottom_frame, image=self.restart_photo, text="", command=on_restart, width=30, height=30)
        restart_button.grid(row=0, column=3, padx=(30, 25))

        # Save button
        save_button = ctk.CTkButton(bottom_frame, text="Save", command=on_save, width=50)
        save_button.grid(row=0, column=4, padx=(75, 0))
