import os
from pathlib import Path
from src.tournament.tournament_manager import TournamentManager

ROOT_DIR = Path(__file__).parent
AGENT_DIR = ROOT_DIR / "src/agents"

def create_team_files():
    # Créer une instance temporaire pour accéder au mapping
    tm = TournamentManager(None)
    
    # Lire le template
    with open(AGENT_DIR / "random_agent.py", "r", encoding='utf-8') as f:
        template = f.read()
    
    # Créer un fichier pour chaque équipe
    for original_name, file_name in tm.teams_mapping.items():
        file_path = AGENT_DIR / f"{file_name}.py"
        
        # Ne pas écraser les fichiers existants
        if not file_path.exists():
            with open(file_path, "w", encoding='utf-8') as f:
                team_code = template.replace("{TEAM_NAME}", original_name)
                f.write(team_code)

if __name__ == "__main__":
    create_team_files()