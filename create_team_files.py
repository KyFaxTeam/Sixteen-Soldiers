
import os
from src.tournament.tournament_manager import TournamentManager

def create_team_files():
    # Créer une instance temporaire pour accéder au mapping
    tm = TournamentManager(None)
    
    # Lire le template
    with open("src/agents/team_template.py", "r", encoding='utf-8') as f:
        template = f.read()
    
    # Créer un fichier pour chaque équipe
    for original_name, file_name in tm.teams_mapping.items():
        file_path = f"src/agents/{file_name}.py"
        
        # Ne pas écraser les fichiers existants
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding='utf-8') as f:
                team_code = template.replace("{TEAM_NAME}", original_name)
                f.write(team_code)
            

if __name__ == "__main__":
    create_team_files()