from pathlib import Path
from src.tournament.config import TEAMS_MAPPING
ROOT_DIR = Path(__file__).parent
AGENT_DIR = ROOT_DIR / "src/agents"

def create_team_files():
    
    teams_mapping = TEAMS_MAPPING
    
    # Lire le template
    with open(AGENT_DIR / "random_agent.py", "r", encoding='utf-8') as f:
        template = f.read()
    
    # Créer un fichier pour chaque équipe
    for original_name, file_name in teams_mapping.items():
        file_path = AGENT_DIR / f"{file_name}.py"
        
        # Ne pas écraser les fichiers existants
        if not file_path.exists():
            with open(file_path, "w", encoding='utf-8') as f:
                team_code = template.replace("{TEAM_NAME}", original_name)
                f.write(team_code)

if __name__ == "__main__":
    create_team_files()