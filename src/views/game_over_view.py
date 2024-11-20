
from typing import Dict

class GameOverView:
    def __init__(self, master: any):
        self.master = master
        self.frame = ctk.CTkFrame(master)
        self.frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.winner_label = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.winner_label.pack(pady=10)
        
        self.team_label = ctk.CTkLabel(self.frame, text="", font=ctk.CTkFont(size=14))
        self.team_label.pack(pady=5)
        
        self.profile_image_label = ctk.CTkLabel(self.frame, text="")
        self.profile_image_label.pack(pady=5)
        
    def display_winner_info(self, name: str, team: str, profile: str):
        self.winner_label.configure(text=f"Winner: {name}")
        self.team_label.configure(text=f"Team: {team}")
        
        if profile:
            profile_image = ctk.CTkImage(Image.open(profile), size=(60, 60))
            self.profile_image_label.configure(image=profile_image)
        else:
            self.profile_image_label.configure(image=None)
        
    def update(self, state: Dict):
        winner_name = state.get("winner")
        if winner_name:
            winner_info = state.get("agents", {}).get(winner_name, {})
            self.display_winner_info(
                name=winner_name,
                team=winner_info.get("team_pseudo", ""),
                profile=winner_info.get("profile_img", "")
            )