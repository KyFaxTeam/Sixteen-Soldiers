from pathlib import Path
import random

# Configuration des chemins
TOURNAMENT_DIR = Path(__file__).parent


# Liste des équipes finalistes
TEAMS = [
    "AIverse",
    "Némésis",
    "KACW",
    "Blacknight01",
    "Jolych", 
    "Mugiwara",
    "Limitless Nexus",
    "IFRI"
]

def normalize_team_name(team_name):
    """Convert team name to valid filename"""
    return team_name.lower().replace(' ', '').replace('-', '').replace('_', '')\
        .replace('é', 'e').replace('è', 'e').replace('à', 'a').replace('.', '').replace("ï", "i").replace("(", "").replace(")", "")


TEAMS_MAPPING = {team: normalize_team_name(team) for team in TEAMS}
BACK_TEAMS_MAPPING = {v: k for k, v in TEAMS_MAPPING.items()}

